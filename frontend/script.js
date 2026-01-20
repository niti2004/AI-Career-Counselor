// Tab switching functionality
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const tabName = this.getAttribute('data-tab');
        switchTab(tabName);
    });
});

function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
}

// Check AI Status on page load
window.addEventListener('load', async function() {
    try {
        const response = await fetch('http://127.0.0.1:5000/ai-status');
        const data = await response.json();
        const statusElement = document.getElementById('aiStatus');
        
        if (data.features.personalized_guidance.providers && data.features.personalized_guidance.providers.length > 0) {
            const providers = data.features.personalized_guidance.providers.map(p => p.name).join(' + ');
            statusElement.innerHTML = `✅ AI Features Active (${providers})`;
            statusElement.style.color = '#4caf50';
        } else {
            statusElement.innerHTML = '⚠️ AI Features: Set GEMINI_API_KEY or OPENAI_API_KEY to enable guidance';
            statusElement.style.color = '#ff9800';
        }
    } catch (error) {
        console.error('Error checking AI status:', error);
    }
});

// ========== TAB 1: Career Search ==========
document.getElementById('careerForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const career = document.getElementById('career').value;
    const level = document.getElementById('level').value;
    const resultDiv = document.getElementById('careerResult');

    resultDiv.innerHTML = '<p class="loading">⏳ Analyzing career path...</p>';

    try {
        const response = await fetch('http://127.0.0.1:5000/career', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ career: career, level: level })
        });

        if (response.ok) {
            const data = await response.json();
            if (data.status === 'success') {
                displayCareerGuidance(data);
            } else if (data.status === 'unknown') {
                displayUnknownCareer(data);
            }
        } else {
            resultDiv.innerHTML = '<p class="error">❌ Error: Unable to get guidance. Please try again.</p>';
        }
    } catch (error) {
        resultDiv.innerHTML = '<p class="error">❌ Error: Could not connect to the server.</p>';
        console.error('Error:', error);
    }
});

// ========== TAB 2: Recommend by Skills ==========
document.getElementById('skillForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const skillInput = document.getElementById('skillInput').value;
    const skills = skillInput.split(',').map(s => s.trim()).filter(s => s);
    const resultDiv = document.getElementById('recommendResult');

    if (skills.length === 0) {
        resultDiv.innerHTML = '<p class="error">❌ Please enter at least one skill</p>';
        return;
    }

    resultDiv.innerHTML = '<p class="loading">⏳ Finding matching careers...</p>';

    try {
        const response = await fetch('http://127.0.0.1:5000/recommend', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ skills: skills })
        });

        if (response.ok) {
            const data = await response.json();
            displaySkillRecommendations(data);
        } else {
            resultDiv.innerHTML = '<p class="error">❌ Error getting recommendations</p>';
        }
    } catch (error) {
        resultDiv.innerHTML = '<p class="error">❌ Error: Could not connect to server</p>';
    }
});

// ========== TAB 3: Skill Gap Analysis ==========
document.getElementById('gapForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const career = document.getElementById('gapCareer').value;
    const skillInput = document.getElementById('gapSkills').value;
    const skills = skillInput ? skillInput.split(',').map(s => s.trim()).filter(s => s) : [];
    const resultDiv = document.getElementById('gapResult');

    resultDiv.innerHTML = '<p class="loading">⏳ Analyzing skill gap...</p>';

    try {
        const response = await fetch('http://127.0.0.1:5000/skill-gap', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ career: career, skills: skills })
        });

        if (response.ok) {
            const data = await response.json();
            displaySkillGap(data);
        } else {
            resultDiv.innerHTML = '<p class="error">❌ Error analyzing skill gap</p>';
        }
    } catch (error) {
        resultDiv.innerHTML = '<p class="error">❌ Error: Could not connect to server</p>';
    }
});

// ========== TAB 4: Compare Careers ==========
document.getElementById('compareForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const careers = [
        document.getElementById('career1').value,
        document.getElementById('career2').value,
        document.getElementById('career3').value
    ].filter(c => c);
    
    const resultDiv = document.getElementById('compareResult');
    resultDiv.innerHTML = '<p class="loading">⏳ Comparing careers...</p>';

    try {
        const response = await fetch('http://127.0.0.1:5000/compare', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ careers: careers })
        });

        if (response.ok) {
            const data = await response.json();
            displayComparison(data);
        } else {
            resultDiv.innerHTML = '<p class="error">❌ Error comparing careers</p>';
        }
    } catch (error) {
        resultDiv.innerHTML = '<p class="error">❌ Could not connect to server</p>';
    }
});

// ========== TAB 5: Browse Careers with NLP ==========
async function searchCareers() {
    const keyword = document.getElementById('searchKeyword').value;
    const resultDiv = document.getElementById('browseResult');
    
    if (!keyword || keyword.trim().length === 0) {
        resultDiv.innerHTML = '<p class="info">💡 Try searching for: engineer, data, design, cloud, mobile, ai, or any role name</p>';
        return;
    }
    
    resultDiv.innerHTML = '<p class="loading">🔍 Searching with NLP... (finding semantic matches)</p>';
    
    try {
        const response = await fetch('http://127.0.0.1:5000/onet/search', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ keyword })
        });
        const data = await response.json();
        
        if (data.status === 'error') {
            resultDiv.innerHTML = `<p class="error">❌ ${data.message}</p>`;
            return;
        }
        
        if (data.total === 0) {
            resultDiv.innerHTML = `<p class="error">❌ No careers found for "${keyword}". Try: engineer, data, design, manager, developer</p>`;
            return;
        }
        
        let html = `<div class="search-results-header">
            <p>Found <strong>${data.total}</strong> matching career${data.total !== 1 ? 's' : ''} for "<strong>${keyword}</strong>"</p>
            <small>Powered by NLP semantic search - TF-IDF similarity scoring</small>
        </div><div class="careers-grid">`;
        
        data.results.forEach((career, idx) => {
            const matchLabel = career.match_score ? `<span class="match-badge">${career.match_score} match</span>` : '';
            html += `
                <div class="career-card" onclick="viewCareerDetail('${career.name}')">
                    <div class="card-header">
                        <h4>${career.name}</h4>
                        ${matchLabel}
                    </div>
                    <p class="description">${career.description}</p>
                    <div class="card-footer">
                        <span class="salary">💰 From $${(career.salary_entry || 0).toLocaleString()}</span>
                        ${career.job_outlook ? `<span class="outlook">📊 ${career.job_outlook}</span>` : ''}
                    </div>
                    <div class="skills-inline">
                        ${(career.skills || []).slice(0, 3).map(s => `<span class="skill-tag-small">${s}</span>`).join('')}
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        resultDiv.innerHTML = html;
    } catch (error) {
        console.error(error);
        resultDiv.innerHTML = '<p class="error">❌ Error searching careers. Please try again.</p>';
    }
}

function viewCareerDetail(careerName) {
    alert(`Career: ${careerName}\n\nClick on the career card to learn more. Use the Compare tab to compare this career with others!`);
}

// ========== Display Functions ==========

function displayCareerGuidance(data) {
    const resultDiv = document.getElementById('careerResult');
    
    let html = `
        <div class="guidance-card">
            <div class="career-header">
                <div>
                    <h2>${data.career}</h2>
                    ${data.match_confidence < 100 ? `<small>✓ Match confidence: ${data.match_confidence}%</small>` : ''}
                </div>
                <span class="level-badge">${data.level}</span>
            </div>
            
            <div class="focus-section">
                <strong>📌 Your Focus:</strong>
                <p>${data.focus}</p>
            </div>

            <div class="roadmap-section">
                <strong>🗺️ Learning Roadmap:</strong>
                <ol class="roadmap-list">
                    ${data.roadmap.map(step => `<li>${step}</li>`).join('')}
                </ol>
            </div>

            <div class="skills-section">
                <strong>🛠️ Key Skills to Develop:</strong>
                <div class="skills-tags">
                    ${data.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
                </div>
            </div>

            <div class="market-section">
                <strong>💼 Market Insights:</strong>
                <p>${data.market}</p>
            </div>

            <div class="future-section">
                <strong>🚀 Future Outlook:</strong>
                <p>${data.future}</p>
            </div>

            <div class="resources-section">
                <strong>📚 Recommended Resources:</strong>
                <ul class="resources-list">
                    ${data.resources.map(resource => {
                        if (typeof resource === 'object' && resource.url) {
                            return `<li><a href="${resource.url}" target="_blank" rel="noopener noreferrer">${resource.name}</a></li>`;
                        } else {
                            return `<li>${typeof resource === 'string' ? resource : (resource.name || 'Resource')}</li>`;
                        }
                    }).join('')}
                </ul>
            </div>

            <div class="tips-section">
                <strong>💡 Tips for ${data.level}s:</strong>
                <ul class="tips-list">
                    ${data.tips.map(tip => `<li>${tip}</li>`).join('')}
                </ul>
            </div>

            ${data.ai_personalized_guidance ? `
                <div class="ai-section">
                    <strong>🤖 AI-Powered Personalized Guidance:</strong>
                    <div class="ai-content">${data.ai_personalized_guidance.replace(/\n/g, '<br>')}</div>
                </div>
            ` : ''}

            ${data.similar_careers && data.similar_careers.length > 0 ? `
                <div class="similar-careers-section">
                    <strong>🔗 Similar Careers You Might Like:</strong>
                    <div class="similar-careers">
                        ${data.similar_careers.map(c => `
                            <div class="similar-career-card">
                                <p>${c.career}</p>
                                <small>${c.similarity} similar</small>
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : ''}
        </div>
    `;
    
    resultDiv.innerHTML = html;
}

function displayUnknownCareer(data) {
    const resultDiv = document.getElementById('careerResult');
    
    let html = `
        <div class="guidance-card unknown-career">
            <h2>🤔 ${data.career}</h2>
            <p class="message">${data.message}</p>
            <p class="suggestion"><strong>Suggestion:</strong> ${data.suggestion}</p>
            
            <div class="tips-section">
                <strong>💡 How to Explore:</strong>
                <ul class="tips-list">
                    ${data.tips.map(tip => `<li>${tip}</li>`).join('')}
                </ul>
            </div>
        </div>
    `;
    
    resultDiv.innerHTML = html;
}

function displayComparison(data) {
    const resultDiv = document.getElementById('compareResult');
    
    if (data.status !== 'success') {
        resultDiv.innerHTML = `<p class="error">❌ ${data.message}</p>`;
        return;
    }

    let html = '<div class="comparison-container">';
    html += '<div class="comparison-section"><h3>💰 Salary Ranges</h3><div class="comparison-grid">';
    data.careers.forEach(career => {
        const sal = career.salary;
        html += `<div class="comparison-item"><h4>${career.name}</h4><p>Entry: $${(sal.entry || 0).toLocaleString()}</p><p>Mid: $${(sal.mid || 0).toLocaleString()}</p><p>Senior: $${(sal.senior || 0).toLocaleString()}</p></div>`;
    });
    html += '</div></div>';
    
    html += '<div class="comparison-section"><h3>🛠️ Key Skills</h3><div class="comparison-grid">';
    data.careers.forEach(career => {
        html += `<div class="comparison-item"><h4>${career.name}</h4><div class="skills-tags">${career.skills.slice(0, 5).map(s => `<span class="skill-tag">${s}</span>`).join('')}</div></div>`;
    });
    html += '</div></div>';
    
    html += '<div class="comparison-section"><h3>📊 Job Outlook</h3><div class="comparison-grid">';
    data.careers.forEach(career => {
        html += `<div class="comparison-item"><h4>${career.name}</h4><p>${career.job_outlook}</p></div>`;
    });
    html += '</div></div></div>';
    resultDiv.innerHTML = html;
}

function displaySkillRecommendations(data) {
    const resultDiv = document.getElementById('recommendResult');
    
    if (data.status !== 'success') {
        resultDiv.innerHTML = `<p class="error">❌ ${data.message}</p>`;
        return;
    }

    let html = `
        <div class="recommendation-card">
            <h3>🎯 Careers Matching Your Skills</h3>
            <p class="intro">Based on your skills: <strong>${data.input_skills.join(', ')}</strong></p>
            
            <div class="recommendations-list">
    `;

    data.recommendations.forEach((rec, index) => {
        html += `
            <div class="recommendation-item">
                <div class="rec-header">
                    <h4>${index + 1}. ${rec.career}</h4>
                    <span class="match-badge">${rec.match_score} Match</span>
                </div>
                ${rec.matching_skills.length > 0 ? `
                    <p><strong>Your Matching Skills:</strong> ${rec.matching_skills.join(', ')}</p>
                ` : ''}
                <p><strong>Skills to Learn:</strong> ${rec.skills_to_learn} additional skill${rec.skills_to_learn !== 1 ? 's' : ''}</p>
            </div>
        `;
    });

    html += `
            </div>
        </div>
    `;
    
    resultDiv.innerHTML = html;
}

function displaySkillGap(data) {
    const resultDiv = document.getElementById('gapResult');
    
    if (data.status !== 'success') {
        resultDiv.innerHTML = `<p class="error">❌ ${data.message}</p>`;
        return;
    }

    let html = `
        <div class="gap-card">
            <div class="gap-header">
                <h3>${data.career}</h3>
                <div class="progress-container">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${data.skill_match_percentage}%"></div>
                    </div>
                    <span class="progress-text">${data.skill_match_percentage}% Complete</span>
                </div>
            </div>

            <div class="gap-summary">
                ${data.analysis_summary}
            </div>

            ${data.matching_skills.length > 0 ? `
                <div class="matching-skills">
                    <strong>✅ Skills You Have:</strong>
                    <div class="skills-tags">
                        ${data.matching_skills.map(skill => `<span class="skill-tag green">${skill}</span>`).join('')}
                    </div>
                </div>
            ` : ''}

            ${data.missing_skills.length > 0 ? `
                <div class="missing-skills">
                    <strong>📚 Skills to Learn:</strong>
                    <div class="skills-tags">
                        ${data.missing_skills.map(skill => `<span class="skill-tag red">${skill}</span>`).join('')}
                    </div>
                </div>
            ` : ''}
        </div>
    `;
    
    resultDiv.innerHTML = html;
}
