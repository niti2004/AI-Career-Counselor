from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from .career_data import CAREER_DB

import pickle
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# Attempt to load TF-IDF index built by `backend/onet_importer.py`
_VEC_PATH = Path(__file__).parent / 'CAREER_DB_onet.vec.pkl'
_IDX_PATH = Path(__file__).parent / 'CAREER_DB_onet.idx.pkl'
_MATRIX_PATH = Path(__file__).parent / 'CAREER_DB_onet.matrix.npz'

_TFIDF_VEC = None
_TFIDF_MATRIX = None
_TFIDF_TITLES = None

def _try_load_index():
    global _TFIDF_VEC, _TFIDF_MATRIX, _TFIDF_TITLES
    if _TFIDF_VEC is not None:
        return True
    try:
        if _VEC_PATH.exists() and _IDX_PATH.exists() and _MATRIX_PATH.exists():
            with open(_VEC_PATH, 'rb') as f:
                _TFIDF_VEC = pickle.load(f)
            with open(_IDX_PATH, 'rb') as f:
                meta = pickle.load(f)
                _TFIDF_TITLES = meta.get('titles', [])
            from scipy.sparse import load_npz
            _TFIDF_MATRIX = load_npz(str(_MATRIX_PATH))
            return True
    except Exception:
        _TFIDF_VEC = None
        _TFIDF_MATRIX = None
        _TFIDF_TITLES = None
    return False


def find_best_career_match(user_input):
    """Find best career using TF‑IDF semantic search if available, else fuzzy match.

    Returns (career_key, confidence_percent)
    """
    user_input = user_input.lower().strip()

    # Try semantic TF-IDF search first
    if _try_load_index() and _TFIDF_VEC is not None and _TFIDF_MATRIX is not None:
        try:
            q = _TFIDF_VEC.transform([user_input])
            sims = cosine_similarity(q, _TFIDF_MATRIX).flatten()
            best_idx = int(np.argmax(sims))
            best_score = float(sims[best_idx])
            best_title = _TFIDF_TITLES[best_idx]
            # convert to percentage
            pct = round(best_score * 100, 1)
            # if score is reasonably strong, return
            if best_score >= 0.15:
                return best_title, pct
        except Exception:
            pass

    # Fallback to fuzzy matching on CAREER_DB keys
    careers = list(CAREER_DB.keys())
    best_match = process.extractOne(user_input, careers, scorer=fuzz.token_set_ratio)
    if best_match:
        career_name, score = best_match
        if score >= 70:
            return career_name, score

    return None, 0


def get_career_similarity(career1, career2):
    """
    Calculate similarity between two careers based on skills overlap.
    
    Args:
        career1: First career name
        career2: Second career name
    
    Returns:
        float: Similarity score (0-1)
    """
    if career1 not in CAREER_DB or career2 not in CAREER_DB:
        return 0
    
    skills1 = set(CAREER_DB[career1]["skills"])
    skills2 = set(CAREER_DB[career2]["skills"])
    
    if len(skills1.union(skills2)) == 0:
        return 0
    
    intersection = len(skills1.intersection(skills2))
    union = len(skills1.union(skills2))
    
    return intersection / union


def find_similar_careers(career_name, top_n=3):
    """
    Find similar careers based on skill overlap.
    
    Args:
        career_name: Target career name
        top_n: Number of similar careers to return
    
    Returns:
        list: List of (career_name, similarity_score) tuples
    """
    if career_name not in CAREER_DB:
        return []
    
    similarities = []
    for other_career in CAREER_DB.keys():
        if other_career != career_name:
            score = get_career_similarity(career_name, other_career)
            similarities.append((other_career, score))
    
    # Sort by similarity and return top N
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_n]
