
content = r"""import { useState, useRef } from "react";
import { analyzePhishingEmail } from "./api/phishing.js";
import { analyzeURL } from "./api/urlRisk.js";

function extractUrls(text) {
  if (!text) return [];
  const matches = text.match(/https?:\/\/[^\s"'<>]+/g) || [];
  return [...new Set(matches)];
}

function getThreatLevel(pct) {
  if (pct >= 70) return "danger";
  if (pct >= 40) return "suspicious";
  return "safe";
}

const THREAT_LABELS = { danger: "PHISHING", suspicious: "SUSPICIOUS", safe: "SAFE" };
const URL_THREAT_LABELS = { danger: "HIGH RISK", suspicious: "MEDIUM RISK", safe: "LOW RISK" };

function ThreatGauge({ value, max = 100, level }) {
  const radius = 52;
  const circumference = 2 * Math.PI * radius;
  const pct = Math.min(Math.max(value / max, 0), 1);
  const strokeDashoffset = circumference * (1 - pct);
  const colorMap = { safe: "#3ee0c6", suspicious: "#f0b429", danger: "#f07178" };
  const color = colorMap[level] || "#9aabc4";
  return (
    <div className="threat-gauge">
      <svg width="130" height="130" viewBox="0 0 130 130">
        <circle cx="65" cy="65" r={radius} fill="none" stroke="#243049" strokeWidth="10" />
        <circle cx="65" cy="65" r={radius} fill="none" stroke={color} strokeWidth="10"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          transform="rotate(-90 65 65)"
          style={{ transition: "stroke-dashoffset 0.6s ease, stroke 0.4s ease" }} />
        <text x="65" y="60" textAnchor="middle" dominantBaseline="middle"
          className="gauge-score" fill={color}>
          {Math.round(value)}
        </text>
        <text x="65" y="78" textAnchor="middle" dominantBaseline="middle"
          className="gauge-unit" fill="#9aabc4">
          / {max}
        </text>
      </svg>
    </div>
  );
}

const FRIENDLY_MAP = {
  account: "Account-related language detected",
  verify: "Verification request detected",
  verification: "Identity verification language detected",
  password: "Credential-related wording detected",
  suspended: "Account suspension threat detected",
  click: "Call-to-action urgency detected",
  immediately: "Urgency language detected",
  urgent: "Urgency language detected",
  login: "Login-related language detected",
  secure: "False security claim language detected",
  update: "Account update request detected",
  confirm: "Confirmation request detected",
  bank: "Banking-related language detected",
};

function getFriendlyLabel(feature) {
  const lower = feature.toLowerCase();
  for (const [key, label] of Object.entries(FRIENDLY_MAP)) {
    if (lower.includes(key)) return label;
  }
  return `Suspicious pattern: "${feature}"`;
}

function ExplainEmail({ explanation }) {
  if (!explanation || explanation.length === 0) return null;
  return (
    <div className="explain-section">
      <p className="section-title">Why TrustGuard flagged this email</p>
      <ul className="explain-list">
        {explanation.map((item) => (
          <li key={item.feature} className="explain-item">
            <span className="explain-bullet">&#9888;</span>
            <span className="explain-text">
              <span className="explain-label">{getFriendlyLabel(item.feature)}</span>
              <span className="explain-feature">Indicator: &quot;{item.feature}&quot;</span>
            </span>
            <span className={`chip chip--${item.contribution_to_phishing > 0 ? "danger" : "ok"}`}>
              {item.contribution_to_phishing > 0 ? "+" : ""}{item.contribution_to_phishing.toFixed(3)}
            </span>
          </li>
        ))}
      </ul>
      <p className="explain-disclaimer">
        These indicators are linguistic patterns and do not prove an email is malicious.
      </p>
    </div>
  );
}

function ExplainUrl({ result }) {
  const { https, hostname, keyword_indicators } = result;
  const allClear = keyword_indicators.length === 0 && https && hostname;
  return (
    <div className="explain-section">
      <p className="section-title">Why this URL is flagged</p>
      <ul className="explain-list">
        {!https && (
          <li className="explain-item">
            <span className="explain-bullet">&#9888;</span>
            <span className="explain-text">
              <span className="explain-label">No HTTPS detected</span>
              <span className="explain-feature">Connection is not encrypted (+15 pts)</span>
            </span>
            <span className="chip chip--danger">Risk</span>
          </li>
        )}
        {!hostname && (
          <li className="explain-item">
            <span className="explain-bullet">&#9888;</span>
            <span className="explain-text">
              <span className="explain-label">No valid hostname found</span>
              <span className="explain-feature">URL may be malformed (+30 pts)</span>
            </span>
            <span className="chip chip--danger">Risk</span>
          </li>
        )}
        {keyword_indicators.map((kw) => (
          <li key={kw} className="explain-item">
            <span className="explain-bullet">&#9888;</span>
            <span className="explain-text">
              <span className="explain-label">Suspicious keyword in URL</span>
              <span className="explain-feature">Keyword: &quot;{kw}&quot; (+8 pts)</span>
            </span>
            <span className="chip chip--danger">Risk</span>
          </li>
        ))}
        {allClear && (
          <li className="explain-item">
            <span className="explain-bullet ok-bullet">&#10003;</span>
            <span className="explain-text">
              <span className="explain-label">No suspicious keywords detected</span>
              <span className="explain-feature">URL structure appears normal</span>
            </span>
          </li>
        )}
      </ul>
      <p className="explain-disclaimer">HTTPS alone does not prove a website is trustworthy.</p>
    </div>
  );
}

function RecommendEmail({ level }) {
  const safe = level === "safe";
  const items = safe
    ? [
        "No strong phishing indicators found.",
        "Verify unexpected requests before acting.",
        "Stay cautious with links even in safe-looking emails.",
      ]
    : [
        "Do not click any links in this email.",
        "Do not provide passwords, OTPs, or personal details.",
        "Verify the sender through a trusted, independent channel.",
        "Report to your IT or security team if received at work.",
      ];
  return (
    <div className="recommend-section">
      <p className="section-title">Recommended Action</p>
      <ul className="recommend-list">
        {items.map((item, i) => (
          <li key={i} className="recommend-item">
            <span className="recommend-icon">{safe ? "\u2139" : "\uD83D\uDEE1"}</span>
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

function RecommendUrl({ level }) {
  const safe = level === "safe";
  const items = safe
    ? [
        "No major risk indicators detected.",
        "Always verify the domain matches the official site.",
        "Prefer navigating to sites manually rather than via links.",
      ]
    : [
        "Avoid entering credentials or personal information here.",
        "Check the domain name carefully for typos or lookalike characters.",
        "Navigate to the official website manually instead.",
        "Do not trust HTTPS alone — phishing sites can use HTTPS.",
      ];
  return (
    <div className="recommend-section">
      <p className="section-title">Recommended Action</p>
      <ul className="recommend-list">
        {items.map((item, i) => (
          <li key={i} className="recommend-item">
            <span className="recommend-icon">{safe ? "\u2139" : "\uD83D\uDEE1"}</span>
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
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
  const urlSectionRef = useRef(null);

  const detectedUrls = extractUrls(body);

  async function handleAnalyzeEmail() {
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
    } catch (err) {
      setPhishingError(err.message || "Unable to analyze the email.");
    } finally {
      setPhishingLoading(false);
    }
  }

  async function handleAnalyzeURL(targetUrl) {
    const target = (targetUrl || url).trim();
    setUrlError("");
    setUrlResult(null);
    if (!target) { setUrlError("Please enter a URL."); return; }
    setUrlLoading(true);
    if (targetUrl) setUrl(targetUrl);
    try {
      const data = await analyzeURL(target);
      setUrlResult(data);
    } catch (err) {
      setUrlError(err.message || "Unable to analyze the URL.");
    } finally {
      setUrlLoading(false);
    }
    setTimeout(() => {
      urlSectionRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 100);
  }

  const phishingPct = phishingResult
    ? parseFloat((phishingResult.probability_phishing * 100).toFixed(2))
    : 0;
  const phishingLevel = phishingResult ? getThreatLevel(phishingPct) : null;
  const urlLevel = urlResult ? getThreatLevel(urlResult.risk_score) : null;

  return (
    <div className="page">
      <header className="topbar">
        <div className="topbar-brand">
          <svg className="shield-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path
              d="M12 2L3 7v5c0 5.25 3.75 10.15 9 11.25C17.25 22.15 21 17.25 21 12V7L12 2z"
              fill="var(--accent)" fillOpacity="0.15" stroke="var(--accent)"
              strokeWidth="1.5" strokeLinejoin="round"
            />
            <path d="M9 12l2 2 4-4" stroke="var(--accent)" strokeWidth="1.5"
              strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          <div>
            <p className="eyebrow">Cyber AI Hackathon 2026 &mdash; University of Derby</p>
            <h1>TrustGuard AI</h1>
            <p className="tagline">Adaptive AI for Cyber Threat Detection &amp; Digital Trust</p>
          </div>
        </div>
        <div className="badge badge--ok">
          <span className="badge__dot" />
          System Active
        </div>
      </header>

      <main className="grid">
        {/* LEFT — Email */}
        <div className="column">
          <section className="panel">
            <div className="panel-header">
              <span className="panel-icon">&#9993;</span>
              <div>
                <h2>Email Threat Analysis</h2>
                <p className="lede">Paste email content to detect phishing indicators.</p>
              </div>
            </div>

            <label>
              Sender
              <input type="text" value={sender}
                onChange={(e) => setSender(e.target.value)}
                placeholder="security@example.com" />
            </label>

            <label>
              Subject
              <input type="text" value={subject}
                onChange={(e) => setSubject(e.target.value)}
                placeholder="Urgent account verification required" />
            </label>

            <label>
              Email Body
              <textarea rows="7" value={body}
                onChange={(e) => setBody(e.target.value)}
                placeholder="Paste the email content here..." />
            </label>

            {detectedUrls.length > 0 && (
              <div className="url-detected">
                <p className="url-detected__title">
                  &#128279; URL{detectedUrls.length > 1 ? "s" : ""} detected in email body
                </p>
                <ul className="url-detected__list">
                  {detectedUrls.map((u) => (
                    <li key={u} className="url-detected__item">
                      <span className="url-detected__url">{u}</span>
                      <button className="btn-secondary"
                        onClick={() => handleAnalyzeURL(u)}
                        disabled={urlLoading}>
                        Analyze URL &rarr;
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <button onClick={handleAnalyzeEmail} disabled={phishingLoading}>
              {phishingLoading ? "Analyzing\u2026" : "Analyze Email"}
            </button>

            {phishingError && (
              <div className="callout callout--warn">
                <strong>Error</strong>
                <p>{phishingError}</p>
              </div>
            )}
          </section>

          <section className="panel result-panel">
            <div className="panel-header">
              <span className="panel-icon">&#128269;</span>
              <div><h2>Analysis Result</h2></div>
            </div>

            {!phishingResult && !phishingLoading && (
              <p className="lede">Submit an email above to see the AI detection result.</p>
            )}
            {phishingLoading && (
              <div className="analyzing-state">
                <div className="spinner" />
                <p className="lede">Analyzing email\u2026</p>
              </div>
            )}

            {phishingResult && (
              <>
                <div className="score-block">
                  <ThreatGauge value={phishingPct} max={100} level={phishingLevel} />
                  <div className="score-block__info">
                    <span className={`threat-badge threat-badge--${phishingLevel}`}>
                      {THREAT_LABELS[phishingLevel]}
                    </span>
                    <p className="score-label">Phishing Probability</p>
                    <p className="score-value">{phishingPct}%</p>
                    <p className="score-sub">
                      Status: <strong>{phishingResult.threat_status.replace(/_/g, " ")}</strong>
                    </p>
                  </div>
                </div>
                <div className="divider" />
                <ExplainEmail explanation={phishingResult.explanation} />
                <div className="divider" />
                <RecommendEmail level={phishingLevel} />
                <div className="divider" />
                <div className="meta">
                  <div><strong>Model</strong><span>{phishingResult.model}</span></div>
                  <div><strong>Version</strong><span>{phishingResult.model_version}</span></div>
                </div>
              </>
            )}
          </section>
        </div>

        {/* RIGHT — URL */}
        <div className="column" ref={urlSectionRef}>
          <section className="panel">
            <div className="panel-header">
              <span className="panel-icon">&#128279;</span>
              <div>
                <h2>URL Risk Analysis</h2>
                <p className="lede">Analyze a URL for suspicious patterns and security risks.</p>
              </div>
            </div>

            <label>
              URL
              <input type="text" value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://example.com/login" />
            </label>

            <button onClick={() => handleAnalyzeURL()} disabled={urlLoading}>
              {urlLoading ? "Analyzing\u2026" : "Analyze URL"}
            </button>

            {urlError && (
              <div className="callout callout--warn">
                <strong>Error</strong>
                <p>{urlError}</p>
              </div>
            )}
          </section>

          <section className="panel result-panel">
            <div className="panel-header">
              <span className="panel-icon">&#128202;</span>
              <div><h2>URL Risk Result</h2></div>
            </div>

            {!urlResult && !urlLoading && (
              <p className="lede">Enter a URL above and click <strong>Analyze URL</strong>.</p>
            )}
            {urlLoading && (
              <div className="analyzing-state">
                <div className="spinner" />
                <p className="lede">Analyzing URL\u2026</p>
              </div>
            )}

            {urlResult && (
              <>
                <div className="score-block">
                  <ThreatGauge value={urlResult.risk_score} max={100} level={urlLevel} />
                  <div className="score-block__info">
                    <span className={`threat-badge threat-badge--${urlLevel}`}>
                      {URL_THREAT_LABELS[urlLevel]}
                    </span>
                    <p className="score-label">Risk Score</p>
                    <p className="score-value">{urlResult.risk_score}/100</p>
                  </div>
                </div>

                <div className="stat-grid">
                  <div className="stat-item">
                    <span className="stat-key">HTTPS</span>
                    <span className={`stat-val ${urlResult.https ? "ok" : "danger"}`}>
                      {urlResult.https ? "\u2713 Enabled" : "\u2717 Not enabled"}
                    </span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-key">Hostname</span>
                    <span className="stat-val mono">{urlResult.hostname || "Unknown"}</span>
                  </div>
                </div>

                <div className="divider" />
                <ExplainUrl result={urlResult} />
                <div className="divider" />
                <RecommendUrl level={urlLevel} />
              </>
            )}
          </section>
        </div>
      </main>

      <footer className="footer">
        Defensive research prototype. No real credentials, no offensive tooling,
        no invented accuracy metrics.
      </footer>
    </div>
  );
}
"""

with open(r'C:\TRUSTGUARD-AI\frontend\src\App.jsx', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Done. Lines:", content.count('\n'))
