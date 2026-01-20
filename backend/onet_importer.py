import os
import argparse
import json
import pickle
import re
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def extract_text(row, cols):
    parts = []
    for c in cols:
        v = row.get(c)
        if pd.isna(v):
            continue
        parts.append(str(v))
    return " \n ".join(parts)


def simple_extract_skills(text, top_n=8):
    # crude skill extraction: take frequent noun-like tokens (words >3 chars)
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9+#]+", text)
    tokens = [t for t in tokens if len(t) > 3]
    freq = {}
    for t in tokens:
        t_low = t.lower()
        freq[t_low] = freq.get(t_low, 0) + 1
    items = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    skills = [w.title() for w, _ in items[:top_n]]
    return skills


def build_onet_db(input_csv, out_json, build_index=True):
    df = pd.read_csv(input_csv, dtype=str)
    # heuristic column selection
    cols = list(df.columns)
    title_col = None
    desc_col = None
    task_col = None
    for c in cols:
        cl = c.lower()
        if 'title' in cl and title_col is None:
            title_col = c
        if 'description' in cl and desc_col is None:
            desc_col = c
        if 'task' in cl and task_col is None:
            task_col = c

    if title_col is None:
        raise RuntimeError(f"No title-like column found in {input_csv}; columns: {cols}")

    career_db = {}
    texts = []
    titles = []

    for _, row in df.iterrows():
        title = str(row[title_col]).strip()
        key = title.lower()
        text = extract_text(row, [title_col, desc_col, task_col])
        skills = simple_extract_skills(text)

        career_db[key] = {
            "roadmap": [],
            "skills": skills,
            "resources": [],
            "market": text[:500],
            "future": "",
            "source_title": title
        }

        texts.append(text)
        titles.append(key)

    # write JSON
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(career_db, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(career_db)} careers to {out_json}")

    if build_index:
        from scipy import sparse

        vec = TfidfVectorizer(ngram_range=(1,2), max_features=20000)
        X = vec.fit_transform(texts)
        idx_path = Path(out_json).with_suffix('.idx.pkl')
        vec_path = Path(out_json).with_suffix('.vec.pkl')
        matrix_path = Path(out_json).with_suffix('.matrix.npz')
        with open(idx_path, 'wb') as f:
            pickle.dump({'titles': titles, 'matrix_shape': X.shape}, f)
        with open(vec_path, 'wb') as f:
            pickle.dump(vec, f)
        sparse.save_npz(matrix_path, X)
        print(f"Built TF-IDF index ({X.shape}) and saved to {idx_path} / {vec_path} / {matrix_path}")


def main():
    parser = argparse.ArgumentParser(description='Import O*NET occupations CSV into CAREER_DB JSON and build index')
    parser.add_argument('--input', '-i', default='data/onet/occupations.csv', help='Path to O*NET occupations CSV')
    parser.add_argument('--output', '-o', default='backend/CAREER_DB_onet.json', help='Output JSON path')
    parser.add_argument('--no-index', action='store_true', help='Skip building TF-IDF index')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Input file not found: {args.input}")
        print("Please download an O*NET occupations CSV (Occupation Data) and place it at the path above.")
        return

    build_onet_db(args.input, args.output, build_index=not args.no_index)


if __name__ == '__main__':
    main()
