import { useState, useRef } from "react";
import { analyzePhishingEmail } from "./api/phishing.js";
import { analyzeURL } from "./api/urlRisk.js";

// -- UTILS --
function getThreatLevel(pct) {
  if (pct >= 70) return "danger";
  if (pct >= 40) return "suspicious";
  return "safe";
}

const THREAT_LABELS = { danger: "PHISHING", suspicious: "SUSPICIOUS", safe: "SAFE" };
const URL_THREAT_LABELS = { danger: "HIGH RISK", suspicious: "MEDIUM RISK", safe: "LOW RISK" };

function ThreatGauge({ value, max = 100, level }) {
  const radius = 45;
  const circumference = 2 * Math.PI * radius;
  const pct = Math.min(Math.max(value / max, 0), 1);
  const strokeDashoffset = circumference * (1 - pct);
  const colorMap = { safe: "#10b981", suspicious: "#f59e0b", danger: "#ef4444" };
  const color = colorMap[level] || "#9ca3af";
  return (
    <div className="gauge-container">
      <svg width="110" height="110" viewBox="0 0 110 110">
        <circle cx="55" cy="55" r={radius} fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="8" />
        <circle cx="55" cy="55" r={radius} fill="none" stroke={color} strokeWidth="8"
          strokeLinecap="round" strokeDasharray={circumference} strokeDashoffset={strokeDashoffset}
          transform="rotate(-90 55 55)" style={{ transition: "stroke-dashoffset 0.6s ease" }} />
        <text x="55" y="55" textAnchor="middle" dominantBaseline="middle" fill={color} fontSize="1.5rem" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <div className="gauge-details">
        <h4>Threat Score</h4>
        <div className={`threat-badge bg-${level}`}>{level === 'safe' && max !== 100 ? 'LEGITIMATE' : (max===100 ? URL_THREAT_LABELS[level] : THREAT_LABELS[level])}</div>
      </div>
    </div>
  );
}

const FRIENDLY_MAP = {
  account: "Account-related language", verify: "Verification request", verification: "Identity verification",
  password: "Credential request", suspended: "Suspension threat", click: "Call-to-action urgency",
  immediately: "Urgency language", urgent: "Urgency language", login: "Login request",
  secure: "False security claim", update: "Account update request", bank: "Banking reference",
  paypal: "Payment service reference",
};

function getFriendlyLabel(feature) {
  const lower = feature.toLowerCase();
  for (const [key, label] of Object.entries(FRIENDLY_MAP)) {
    if (lower.includes(key)) return label;
  }
  return `Suspicious pattern: "${feature}"`;
}

export default function App() {
  const [sender, setSender] = useState("");
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");

  const [phishingResult, setPhishingResult] = useState(null);
  const [phishingLoading, setPhishingLoading] = useState(false);
  const [phishingError, setPhishingError] = useState("");

  const [url, setUrl] = useState("");
  const [urlResult, setUrlResult] = useState(null);
  const [urlLoading, setUrlLoading] = useState(false);
  const [urlError, setUrlError] = useState("");

  // Last completed analysis for Unified Verdict
  const [lastAnalysis, setLastAnalysis] = useState(null); // { type: 'email'|'url', result, level }

  const emailPanelRef = useRef(null);
  const urlPanelRef = useRef(null);
  const verdictRef = useRef(null);

  const fillDemoEmail = () => {
    setSender("security@example.com");
    setSubject("URGENT: Your account will be suspended");
    setBody("Your account will be suspended within 24 hours.\nClick the link below immediately to verify your password and prevent account closure.\nFailure to verify your account will result in permanent suspension.");
  };

  const fillDemoUrl = () => {
    setUrl("http://secure-login-verify-account.example.com/password/update");
  };

  async function handleAnalyzeEmail(e) {
    e.preventDefault();
    setPhishingError("");
    setPhishingResult(null);
    if (!subject.trim() && !body.trim()) {
      setPhishingError("Please enter an email subject or body.");
      return;
    }
    setPhishingLoading(true);
    try {
      const data = await analyzePhishingEmail({ sender, subject, body });
      setPhishingResult(data);
      const pct = parseFloat((data.probability_phishing * 100).toFixed(2));
      const level = getThreatLevel(pct);
      setLastAnalysis({ type: 'email', result: data, level });
      setTimeout(() => verdictRef.current?.scrollIntoView(), 200);
    } catch (err) {
      setPhishingError(err.message || "TrustGuard AI could not reach the analysis service. Please verify that the backend is running.");
    } finally {
      setPhishingLoading(false);
    }
  }

  async function handleAnalyzeURL(e) {
    if (e) e.preventDefault();
    setUrlError("");
    setUrlResult(null);
    if (!url.trim()) { setUrlError("Please enter a URL."); return; }
    setUrlLoading(true);
    try {
      const data = await analyzeURL(url);
      setUrlResult(data);
      const level = getThreatLevel(data.risk_score);
      setLastAnalysis({ type: 'url', result: data, level });
      setTimeout(() => verdictRef.current?.scrollIntoView(), 200);
    } catch (err) {
      setUrlError(err.message || "TrustGuard AI could not reach the analysis service. Please verify that the backend is running.");
    } finally {
      setUrlLoading(false);
    }
  }

  return (
    <div className="page">
      <nav className="navbar">
        <div className="brand">
          <svg viewBox="0 0 24 24" fill="none" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="currentColor"/>
            <path d="M9 12l2 2 4-4" stroke="currentColor"/>
          </svg>
          <h1>TRUSTGUARD <span>AI</span></h1>
        </div>
        <div className="nav-links">
          <a href="#dashboard">Dashboard</a>
          <a href="#email-analysis">Email Analysis</a>
          <a href="#url-analysis">URL Analysis</a>
          <a href="#how-it-works">How It Works</a>
        </div>
        <div className="status-indicator">
          <div className="status-dot"/>
          AI Detection Engine Online
        </div>
      </nav>

      <section className="hero" id="dashboard">
        <p className="hero-subtitle">Adaptive AI for Cyber Threat Detection & Digital Trust</p>
        <h2>Detect threats before<br/>they become incidents.</h2>
        <p className="hero-text">
          TrustGuard analyzes suspicious emails and URLs using machine-learning-assisted and rule-based security analysis. Make informed security decisions with explainable indicators.
        </p>
        <div className="hero-actions">
          <button className="btn btn-primary" onClick={() => emailPanelRef.current?.scrollIntoView()}>Analyze Email</button>
          <button className="btn btn-secondary" onClick={() => urlPanelRef.current?.scrollIntoView()}>Analyze URL</button>
        </div>
      </section>

      <section className="metrics">
        <div className="metric-card glass">
          <div className="metric-title">Detection Modules</div>
          <div className="metric-value">2</div>
        </div>
        <div className="metric-card glass">
          <div className="metric-title">AI Email Engine</div>
          <div className="metric-value highlight">TF-IDF + LR</div>
        </div>
        <div className="metric-card glass">
          <div className="metric-title">URL Security Engine</div>
          <div className="metric-value highlight">Pattern + HTTPS</div>
        </div>
        <div className="metric-card glass">
          <div className="metric-title">Explainability</div>
          <div className="metric-value" style={{color: "var(--safe)"}}>Enabled</div>
        </div>
      </section>

      <div className="container split-layout">
        {/* EMAIL ------------- */}
        <section className="panel" id="email-analysis" ref={emailPanelRef}>
          <div className="panel-header">
            <div className="panel-icon">&#9993;</div>
            <div>
              <h3>Email Threat Analysis</h3>
              <p className="section-desc" style={{marginBottom:0, fontSize:'0.85rem'}}>Detect phishing via natural language processing.</p>
            </div>
            <button className="demo-btn" type="button" onClick={fillDemoEmail} style={{marginLeft:'auto'}}>Load Demo</button>
          </div>
          
          <form onSubmit={handleAnalyzeEmail} style={{ flexGrow: 1 }}>
            <div className="form-group">
              <label>Sender</label>
              <input type="text" value={sender} onChange={e=>setSender(e.target.value)} placeholder="security@example.com" />
            </div>
            <div className="form-group">
              <label>Subject</label>
              <input type="text" value={subject} onChange={e=>setSubject(e.target.value)} placeholder="Action Required" />
            </div>
            <div className="form-group">
              <label>Email Body</label>
              <textarea rows="6" value={body} onChange={e=>setBody(e.target.value)} placeholder="Paste email content..." />
            </div>
            <button type="submit" className="btn btn-primary" style={{width:'100%'}} disabled={phishingLoading}>
              {phishingLoading ? "Analyzing threat indicators..." : "Analyze Email"}
            </button>
            {phishingLoading && (
              <div className="loader"><div className="spinner"/> Analyzing threat indicators...</div>
            )}
            {phishingError && (
              <div className="callout"><strong>API Error</strong>{phishingError}</div>
            )}
          </form>

          {phishingResult && (
            <div className="result-box">
              {(() => {
                const pct = parseFloat((phishingResult.probability_phishing * 100).toFixed(2));
                const level = getThreatLevel(pct);
                return (
                  <>
                    <ThreatGauge value={pct} max={100} level={level} />
                    
                    <div className="explain-card">
                      <div className="explain-header">Why was this flagged?</div>
                      {phishingResult.explanation && phishingResult.explanation.length > 0 ? (
                        <ul className="indicator-list">
                          {phishingResult.explanation.map(item => (
                            <li key={item.feature} className="indicator-item">
                              <div>
                                <div style={{fontWeight:600}}>{getFriendlyLabel(item.feature)}</div>
                                <div className="indicator-name" style={{fontSize:'0.8rem'}}>"{item.feature}"</div>
                              </div>
                              <div className={`indicator-val ${item.contribution_to_phishing > 0 ? 'val-red' : 'val-green'}`}>
                                {item.contribution_to_phishing > 0 ? '+' : ''}{item.contribution_to_phishing.toFixed(2)}
                              </div>
                            </li>
                          ))}
                        </ul>
                      ) : (
                        <div style={{padding:'1rem', fontSize:'0.9rem', color:'var(--muted)'}}>No strong indicators identified.</div>
                      )}
                    </div>

                    <div className={`rec-card rec-${level}`}>
                      <div className="rec-title">Security Interpretation & Recommendation</div>
                      {level === 'safe' ? (
                        <ul className="rec-list">
                          <li>No strong phishing indicators were identified by the current model.</li>
                          <li>Continue following normal security practices.</li>
                          <li>Verify unexpected requests before acting.</li>
                        </ul>
                      ) : (
                        <ul className="rec-list">
                          <li>Multiple phishing-associated language patterns were detected.</li>
                          <li>Do not click suspicious links.</li>
                          <li>Avoid sharing credentials or personal details.</li>
                          <li>Access the official website directly.</li>
                          <li>Report suspicious messages to your IT team.</li>
                        </ul>
                      )}
                    </div>
                  </>
                );
              })()}
            </div>
          )}
        </section>

        {/* URL ------------- */}
        <section className="panel" id="url-analysis" ref={urlPanelRef}>
          <div className="panel-header">
            <div className="panel-icon">&#128279;</div>
            <div>
              <h3>URL Risk Analysis</h3>
              <p className="section-desc" style={{marginBottom:0, fontSize:'0.85rem'}}>Detect risk patterns in suspicious links.</p>
            </div>
            <button className="demo-btn" type="button" onClick={fillDemoUrl} style={{marginLeft:'auto'}}>Load Demo</button>
          </div>
          
          <form onSubmit={handleAnalyzeURL}>
            <div className="form-group">
              <label>Target URL</label>
              <input type="text" value={url} onChange={e=>setUrl(e.target.value)} placeholder="https://..." />
            </div>
            <button type="submit" className="btn btn-primary" style={{width:'100%'}} disabled={urlLoading}>
              {urlLoading ? "Analyzing threat indicators..." : "Analyze URL"}
            </button>
            {urlLoading && (
              <div className="loader"><div className="spinner"/> Analyzing threat indicators...</div>
            )}
            {urlError && (
              <div className="callout"><strong>API Error</strong>{urlError}</div>
            )}
          </form>

          {urlResult && (
            <div className="result-box">
              {(() => {
                const level = getThreatLevel(urlResult.risk_score);
                return (
                  <>
                    <ThreatGauge value={urlResult.risk_score} max={100} level={level} />
                    
                    <div className="explain-card">
                      <div className="explain-header">Why is this URL suspicious?</div>
                      <ul className="indicator-list">
                        <li className="indicator-item">
                          <div>
                            <div style={{fontWeight:600}}>Connection Security</div>
                            <div className="indicator-name" style={{fontSize:'0.8rem'}}>"{urlResult.hostname}"</div>
                          </div>
                          <div className={`indicator-val ${urlResult.https ? 'val-green' : 'val-red'}`}>
                            {urlResult.https ? 'HTTPS Enabled' : 'No HTTPS'}
                          </div>
                        </li>
                        {urlResult.keyword_indicators.map(kw => (
                          <li key={kw} className="indicator-item">
                            <div>
                              <div style={{fontWeight:600}}>Suspicious Keyword Pattern</div>
                              <div className="indicator-name" style={{fontSize:'0.8rem'}}>"{kw}"</div>
                            </div>
                            <div className="indicator-val val-red">Identified</div>
                          </li>
                        ))}
                        {urlResult.keyword_indicators.length === 0 && (
                          <li className="indicator-item">
                            <div style={{color:'var(--muted)'}}>No suspicious keyword patterns found in URL.</div>
                          </li>
                        )}
                      </ul>
                    </div>

                    <div className={`rec-card rec-${level}`}>
                      <div className="rec-title">Security Recommendation</div>
                      {level === 'safe' ? (
                        <ul className="rec-list">
                          <li>No major risk indicators detected.</li>
                          <li>Always verify the domain matches the official website.</li>
                          <li>Prefer navigating to sites manually rather than via links.</li>
                        </ul>
                      ) : (
                        <ul className="rec-list">
                          <li>Review the sender and context before interacting.</li>
                          <li>Avoid entering credentials on this site.</li>
                          <li>Verify the domain name carefully for typos.</li>
                          <li>Do not download unknown files.</li>
                        </ul>
                      )}
                    </div>
                  </>
                );
              })()}
            </div>
          )}
        </section>
      </div>

      {lastAnalysis && (
        <div className="container" ref={verdictRef}>
          <div className="unified-verdict">
            <h2>TrustGuard Security Verdict</h2>
            <div className="verdict-box" style={{borderColor: lastAnalysis.level === 'safe' ? 'var(--safe)' : lastAnalysis.level === 'suspicious' ? 'var(--suspicious)' : 'var(--danger)'}}>
              <h3 style={{color: lastAnalysis.level === 'safe' ? 'var(--safe)' : lastAnalysis.level === 'suspicious' ? 'var(--suspicious)' : 'var(--danger)'}}>
                {lastAnalysis.level === 'safe' ? 'LOW RISK' : 'THREAT DETECTED'}
              </h3>
            </div>
            <p className="verdict-desc">
              {lastAnalysis.level === 'safe' 
                ? "The provided information does not strongly correlate with malicious activity based on current rules. However, always remain vigilant and verify sources independently." 
                : "The provided information contains indicators highly correlated with malicious activity. Proceed with extreme caution and do not disclose sensitive information."}
            </p>
          </div>
        </div>
      )}

      <div className="container" id="how-it-works">
        <h2 className="section-title">How TrustGuard Works</h2>
        <p className="section-desc">A transparent view into our detection pipeline.</p>
        
        <div className="split-layout" style={{marginBottom: '2rem'}}>
          <div className="flow-diagram">
            <h4>Email Pipeline</h4>
            <div className="flow-step">Email Input</div>
            <div className="flow-arrow">&#8595;</div>
            <div className="flow-step">Text Preprocessing</div>
            <div className="flow-arrow">&#8595;</div>
            <div className="flow-step">TF-IDF Extraction</div>
            <div className="flow-arrow">&#8595;</div>
            <div className="flow-step">Logistic Regression</div>
            <div className="flow-arrow">&#8595;</div>
            <div className="flow-step">Phishing Probability</div>
          </div>
          <div className="flow-diagram">
            <h4>URL Pipeline</h4>
            <div className="flow-step">URL Input</div>
            <div className="flow-arrow">&#8595;</div>
            <div className="flow-step">URL Parsing</div>
            <div className="flow-arrow">&#8595;</div>
            <div className="flow-step">HTTPS &amp; Pattern Validation</div>
            <div className="flow-arrow">&#8595;</div>
            <div className="flow-step">Risk Score Allocation</div>
            <div className="flow-arrow">&#8595;</div>
            <div className="flow-step">Risk Level Verdict</div>
          </div>
        </div>
      </div>
      
      <div className="container">
        <h2 className="section-title">Tech Stack</h2>
        <p className="section-desc">Built for performance, modularity, and rapid threat evaluation.</p>
        <div className="tech-grid">
          <div className="tech-card">
            <h4>Frontend</h4>
            <p>React + Vite</p>
          </div>
          <div className="tech-card">
            <h4>Backend</h4>
            <p>FastAPI + Python</p>
          </div>
          <div className="tech-card">
            <h4>Machine Learning</h4>
            <p>TF-IDF + Logistic Regression</p>
          </div>
          <div className="tech-card">
            <h4>Security Analysis</h4>
            <p>URL parsing + HTTPS + Suspicious pattern analysis</p>
          </div>
          <div className="tech-card">
            <h4>Explainability</h4>
            <p>Top feature contributions</p>
          </div>
        </div>
      </div>

      <footer className="footer">
        <h3>TrustGuard AI</h3>
        <p>Adaptive AI for Cyber Threat Detection & Digital Trust</p>
        <p style={{marginTop: '1rem', color: 'var(--border-light)'}}>
          Defensive research prototype. No real credentials.<br/>
          No offensive tooling. No invented accuracy metrics.<br/>
          Built for cybersecurity innovation and defensive research.
        </p>
      </footer>
    </div>
  );
}
