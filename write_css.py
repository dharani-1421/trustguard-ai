import os

CSS_CONTENT = """
:root {
  color-scheme: dark;
  --bg: #030712;
  --bg-elevated: #111827;
  --bg-panel: #1f2937;
  --bg-input: #374151;
  --border: #374151;
  --border-light: #4b5563;
  --text: #f9fafb;
  --muted: #9ca3af;
  --accent: #0ea5e9; /* Light blue */
  --accent-hover: #0284c7;
  --cyan: #06b6d4;
  --danger: #ef4444; 
  --danger-bg: rgba(239, 68, 68, 0.1);
  --suspicious: #f59e0b; 
  --suspicious-bg: rgba(245, 158, 11, 0.1);
  --safe: #10b981;
  --safe-bg: rgba(16, 185, 129, 0.1);
  --font: "Inter", "Segoe UI", system-ui, sans-serif;
  --mono: "JetBrains Mono", "Cascadia Code", monospace;
  --radius: 12px;
}

* {
  box-sizing: border-box;
}

html, body, #root {
  margin: 0;
  padding: 0;
  min-height: 100%;
  font-family: var(--font);
  background-color: var(--bg);
  color: var(--text);
  line-height: 1.5;
  scroll-behavior: smooth;
}

.page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

h1, h2, h3, h4, h5, h6 {
  margin: 0;
  font-weight: 600;
  letter-spacing: -0.025em;
}

p { margin: 0 0 1rem; }

/* NAVBAR */
.navbar {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(17, 24, 39, 0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.brand svg {
  width: 28px;
  height: 28px;
  color: var(--cyan);
}

.brand h1 {
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: 0;
  color: white;
}
.brand span {
  color: var(--cyan);
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-links a {
  color: var(--muted);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: color 0.15s;
}

.nav-links a:hover {
  color: var(--text);
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--safe);
  background: rgba(16, 185, 129, 0.1);
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.status-dot {
  width: 8px;
  height: 8px;
  background-color: var(--safe);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--safe);
}

/* HERO SECTION */
.hero {
  padding: 5rem 2rem;
  text-align: center;
  background: radial-gradient(circle at center, rgba(6, 182, 212, 0.1) 0%, transparent 60%);
}

.hero-subtitle {
  color: var(--cyan);
  font-weight: 600;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 1rem;
}

.hero h2 {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  background: linear-gradient(to right, #fff, #9ca3af);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-text {
  color: var(--muted);
  font-size: 1.1rem;
  max-width: 600px;
  margin: 0 auto 3rem;
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  border: none;
}

.btn-primary {
  background: var(--cyan);
  color: #000;
}

.btn-primary:hover {
  background: #0891b2;
}

.btn-secondary {
  background: var(--bg-panel);
  color: var(--text);
  border: 1px solid var(--border);
}

.btn-secondary:hover {
  background: var(--border);
}

/* METRICS OVERVIEW */
.metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  padding: 0 2rem 4rem;
  max-width: 1200px;
  margin: -2rem auto 0;
}

.metric-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.5rem;
  text-align: center;
}

.metric-card.glass {
  background: rgba(17, 24, 39, 0.6);
  backdrop-filter: blur(8px);
}

.metric-title {
  color: var(--muted);
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text);
}

.metric-value.highlight {
  color: var(--cyan);
}

/* CONTENT LAYOUT */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  width: 100%;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: white;
}

.section-desc {
  color: var(--muted);
  margin-bottom: 2rem;
}

/* GRID LAYOUT */
.split-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 4rem;
}

@media (max-width: 900px) {
  .split-layout {
    grid-template-columns: 1fr;
  }
}

/* PANELS */
.panel {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
}

.panel-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: rgba(6, 182, 212, 0.1);
  color: var(--cyan);
  border-radius: 8px;
}

.panel-header h3 {
  font-size: 1.1rem;
  margin: 0;
}

/* FORMS */
.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--muted);
  margin-bottom: 0.5rem;
}

.form-group input,
.form-group textarea {
  width: 100%;
  background: var(--bg-input);
  border: 1px solid var(--border-light);
  color: var(--text);
  border-radius: 6px;
  padding: 0.75rem 1rem;
  font-family: inherit;
  font-size: 0.95rem;
  transition: all 0.2s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--cyan);
  box-shadow: 0 0 0 2px rgba(6, 182, 212, 0.2);
}

/* DEMO BUTTON */
.demo-btn {
  font-size: 0.8rem;
  color: var(--cyan);
  background: transparent;
  border: 1px solid rgba(6, 182, 212, 0.3);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  float: right;
  transition: all 0.2s;
}

.demo-btn:hover {
  background: rgba(6, 182, 212, 0.1);
}

/* RESULTS */
.result-box {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
}

.gauge-container {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.gauge-details h4 {
  font-size: 0.85rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.25rem;
}

.gauge-details p {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
}

.threat-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  margin-top: 0.5rem;
}

.bg-danger { background: var(--danger-bg); color: var(--danger); border: 1px solid rgba(239, 68, 68, 0.2); }
.bg-suspicious { background: var(--suspicious-bg); color: var(--suspicious); border: 1px solid rgba(245, 158, 11, 0.2); }
.bg-safe { background: var(--safe-bg); color: var(--safe); border: 1px solid rgba(16, 185, 129, 0.2); }

/* EXPLAINABILITY */
.explain-card {
  background: var(--bg-panel);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 1.5rem;
}

.explain-header {
  background: rgba(0, 0, 0, 0.2);
  padding: 0.75rem 1rem;
  font-size: 0.9rem;
  font-weight: 600;
  border-bottom: 1px solid var(--border);
}

.indicator-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.indicator-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border-light);
  font-size: 0.9rem;
}

.indicator-item:last-child {
  border-bottom: none;
}

.indicator-name {
  font-family: var(--mono);
  color: var(--cyan);
}

.indicator-val {
  font-weight: 600;
}
.indicator-val.val-red { color: var(--danger); }
.indicator-val.val-green { color: var(--safe); }

/* RECOMMENDATIONS */
.rec-card {
  background: var(--bg-panel);
  border-left: 4px solid var(--suspicious);
  border-radius: 4px 8px 8px 4px;
  padding: 1rem;
}
.rec-card.rec-danger { border-left-color: var(--danger); }
.rec-card.rec-safe { border-left-color: var(--safe); }

.rec-title {
  font-size: 0.85rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.75rem;
  font-weight: 700;
}

.rec-list {
  margin: 0;
  padding-left: 1.25rem;
  font-size: 0.9rem;
}

.rec-list li {
  margin-bottom: 0.25rem;
}

/* UNIFIED VERDICT */
.unified-verdict {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 2rem;
  text-align: center;
  margin-bottom: 4rem;
}

.unified-verdict h2 {
  font-size: 1.25rem;
  color: var(--muted);
  margin-bottom: 1rem;
}

.verdict-box {
  display: inline-block;
  padding: 1rem 3rem;
  border-radius: 12px;
  background: var(--bg-panel);
  border: 1px solid var(--border-light);
  margin-bottom: 1rem;
}

.verdict-box h3 {
  font-size: 2rem;
  margin: 0;
}

.verdict-desc {
  max-width: 600px;
  margin: 0 auto;
  color: var(--muted);
}

/* HOW IT WORKS / TECH STACK */
.flow-diagram {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
  background: var(--bg-elevated);
  padding: 2rem;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  margin-bottom: 2rem;
}

.flow-step {
  background: var(--bg-panel);
  border: 1px solid var(--border-light);
  padding: 1rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  text-align: center;
  min-width: 250px;
}

.flow-arrow {
  color: var(--cyan);
  font-size: 1.5rem;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 4rem;
}

.tech-card {
  background: var(--bg-elevated);
  padding: 1.5rem;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  text-align: center;
}

.tech-card h4 {
  color: var(--cyan);
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.tech-card p {
  color: var(--muted);
  font-size: 0.9rem;
  margin: 0;
}

/* FOOTER */
.footer {
  margin-top: auto;
  border-top: 1px solid var(--border);
  padding: 2rem;
  text-align: center;
  color: var(--muted);
  font-size: 0.85rem;
  background: var(--bg-elevated);
}

.callout {
  padding: 1rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: var(--danger);
  border-radius: 8px;
  margin-top: 1rem;
  font-size: 0.9rem;
}
.callout strong {
  display: block;
  margin-bottom: 0.25rem;
}

.loader {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--cyan);
  font-weight: 600;
  margin-top: 1rem;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(6, 182, 212, 0.3);
  border-top-color: var(--cyan);
  border-radius: 50%;
  animation: spin 1s infinite linear;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

@media (max-width: 768px) {
  .nav-links { display: none; }
  .status-indicator { display: none; }
  .hero h2 { font-size: 2rem; }
}
"""

with open(r"C:\TRUSTGUARD-AI\frontend\src\styles.css", "w", encoding="utf-8") as f:
    f.write(CSS_CONTENT)
    
print("styles.css created successfully")
