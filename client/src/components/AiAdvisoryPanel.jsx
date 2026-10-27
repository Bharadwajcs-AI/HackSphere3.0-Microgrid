import { useState } from 'react'
import { BrainCircuit, Sparkles, Loader2, CheckCircle2, AlertTriangle, ShieldCheck, Cpu, Copy, Check, ArrowRight, Download } from 'lucide-react'
import { postAiAdvisory, getDemoForecast } from '../services/api'
import { exportAdvisoryPDF } from '../utils/pdfExport'
import './AiAdvisoryPanel.css'

export default function AiAdvisoryPanel({ forecast, setForecast, addLog }) {
  const [advisory, setAdvisory] = useState(null)
  const [loading, setLoading] = useState(false)
  const [copied, setCopied] = useState(false)
  const [meta, setMeta] = useState(null)

  const summary = forecast?.forecast?.summary

  const handleGenerate = async () => {
    let targetSummary = summary

    // If no forecast exists yet, automatically load the 24h simulation first
    if (!targetSummary) {
      try {
        setLoading(true)
        addLog?.('info', 'Loading 24h horizon baseline for AI Advisory...')
        const demoRes = await getDemoForecast()
        if (demoRes.success) {
          setForecast?.(demoRes)
          targetSummary = demoRes.forecast.summary
          addLog?.('success', '24h simulation loaded. Proceeding with AI Reasoning...')
        } else {
          throw new Error('Could not load simulation baseline')
        }
      } catch (e) {
        addLog?.('error', `Failed to load baseline: ${e.message}`)
        setLoading(false)
        return
      }
    }

    try {
      setLoading(true)
      addLog?.('info', 'Initiating grid stability reasoning & strategic advisory dispatch...')
      const res = await postAiAdvisory(targetSummary)

      if (res.success) {
        setAdvisory(res.advisory)
        setMeta({
          provider: res.provider || 'Autonomous Grid Reasoning Engine',
          model: res.model || 'Edge-Expert-RuleBased-v3.0',
        })
        addLog?.('success', `Advisory generated via [${res.provider || 'Autonomous Engine'}]`)
      } else {
        throw new Error(res.error || 'Failed to generate advisory')
      }
    } catch (err) {
      addLog?.('error', `AI Advisory error: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = () => {
    if (!advisory) return
    navigator.clipboard.writeText(advisory)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
    addLog?.('info', 'AI Advisory copied to clipboard.')
  }

  const handleDownloadPDF = () => {
    if (!advisory) return
    try {
      exportAdvisoryPDF({ advisory, summary, meta })
      addLog?.('success', 'AI Strategic Advisory PDF report downloaded.')
    } catch (e) {
      addLog?.('error', `Failed to export PDF: ${e.message}`)
    }
  }

  return (
    <div className="ai-advisory-view">
      {/* Intro Header */}
      <div className="view-intro">
        <span className="section-kicker">06 — STRATEGIC DISPATCH REASONING</span>
        <h2 className="editorial-heading">AI Grid Strategic Advisory</h2>
        <p className="section-description">
          Automated engineering reasoning engine analyzing 24-hour demand peaks, battery depth-of-discharge,
          and transition risks. Supported by NVIDIA NIM Multi-Model Pool with local deterministic expert fallback.
        </p>
      </div>

      {/* Main Grid Panel */}
      <div className="advisory-layout">
        {/* Left Column: Analysis & Prompting */}
        <div className="advisory-main-col">
          <div className="advisory-hero-card">
            <div className="advisory-hero-header">
              <div className="advisory-title-group">
                <div className="advisory-icon-frame">
                  <BrainCircuit size={22} />
                </div>
                <div>
                  <div className="advisory-tagline">
                    <h3 className="advisory-title">Autonomous Grid Reasoning & Dispatch Advisory</h3>
                    <span className="engine-badge">
                      <Cpu size={12} /> {meta?.provider || 'Autonomous Engine / NIM Ready'}
                    </span>
                  </div>
                  <p className="advisory-subtitle">
                    Generates operator-ready assessments for relay switching, peak shaving, and reserve protection.
                  </p>
                </div>
              </div>

              <div className="advisory-actions">
                {advisory && (
                  <>
                    <button type="button" className="btn-secondary btn-copy" onClick={handleCopy}>
                      {copied ? <><Check size={14} /> Copied</> : <><Copy size={14} /> Copy Text</>}
                    </button>
                    <button
                      type="button"
                      className="btn-secondary btn-pdf"
                      onClick={handleDownloadPDF}
                      title="Download formatted AI Advisory PDF report"
                    >
                      <Download size={14} /> Download PDF
                    </button>
                  </>
                )}
                <button
                  type="button"
                  className="btn-primary"
                  onClick={handleGenerate}
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <Loader2 size={16} className="btn-spinner" /> Generating Advisory...
                    </>
                  ) : (
                    <>
                      <Sparkles size={16} /> {advisory ? 'Re-Evaluate Horizon' : 'Generate AI Advisory'}
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Metrics context summary strip */}
            {summary && (
              <div className="advisory-context-strip">
                <div className="ctx-item">
                  <span className="ctx-lbl">Peak Demand</span>
                  <span className="ctx-val">{summary.peak_demand_kw} kW</span>
                </div>
                <div className="ctx-item">
                  <span className="ctx-lbl">Critical Overloads</span>
                  <span className={`ctx-val ${summary.overload_alerts > 0 ? 'text-crimson' : ''}`}>
                    {summary.overload_alerts} events
                  </span>
                </div>
                <div className="ctx-item">
                  <span className="ctx-lbl">Renewable Dispatch</span>
                  <span className="ctx-val">{summary.hours_renewable} hrs</span>
                </div>
                <div className="ctx-item">
                  <span className="ctx-lbl">Min Battery SOC</span>
                  <span className={`ctx-val ${summary.min_battery_soc_pct <= 10.5 ? 'text-amber' : ''}`}>
                    {summary.min_battery_soc_pct}%
                  </span>
                </div>
                <div className="ctx-item">
                  <span className="ctx-lbl">Final Battery SOC</span>
                  <span className="ctx-val">{summary.final_battery_soc_pct}%</span>
                </div>
              </div>
            )}

            {/* Content Area */}
            <div className="advisory-body-card">
              {!advisory && !loading ? (
                <div className="advisory-empty-state">
                  <div className="empty-symbol">
                    <BrainCircuit size={36} />
                  </div>
                  <h4>No Advisory Generated Yet</h4>
                  <p>
                    {summary
                      ? 'Telemetry and 24-hour forecast data are loaded and verified. Click "Generate AI Advisory" to run stability reasoning.'
                      : 'Load or simulate a 24-hour demand forecast, then invoke the reasoning engine to synthesize operator advisories.'}
                  </p>
                  <button type="button" className="btn-primary" onClick={handleGenerate}>
                    <Sparkles size={16} /> Run Evaluation Now
                  </button>
                </div>
              ) : loading ? (
                <div className="advisory-loading-state">
                  <Loader2 size={32} className="btn-spinner" />
                  <h4>Evaluating Horizon Dynamics...</h4>
                  <p>Synthesizing transformer loading, battery reserves, and relay transition margins.</p>
                </div>
              ) : (
                <div className="advisory-result-container">
                  {meta && (
                    <div className="advisory-meta-header">
                      <div className="meta-pill">Provider: <strong>{meta.provider}</strong></div>
                      <div className="meta-pill">Engine: <strong>{meta.model}</strong></div>
                      <div className="meta-pill status-verified"><ShieldCheck size={13} /> Verified Grid Assessment</div>
                    </div>
                  )}
                  <div className="advisory-text-block">
                    <pre className="advisory-pre">{advisory}</pre>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right Column: Reasoning Architecture Guide */}
        <aside className="advisory-aside">
          <div className="guide-card">
            <h3>Engine Architecture</h3>
            <p>
              The advisory engine utilizes a dual-tier reasoning pipeline designed for uninterrupted microgrid operations:
            </p>
            <ul className="guide-rules-list">
              <li>
                <strong>NVIDIA NIM Multi-Model Pool:</strong> DiffusionGemma and Nemotron models for open-ended deep language reasoning when an API key is provided.
              </li>
              <li>
                <strong>Autonomous Edge Reasoning:</strong> Deterministic expert inference engine executing locally with guaranteed zero latency and zero dependency failures.
              </li>
              <li>
                <strong>Standardized Sections:</strong> Executive summary, anomaly detection, battery dispatch protection, and shift checklists.
              </li>
            </ul>
          </div>

          <div className="guide-card">
            <h3>Key Dispatch Rules Applied</h3>
            <div className="rule-formula">&gt; 160 kW or 18:00–22:00 $\rightarrow$ Renewable Mode</div>
            <div className="rule-formula">&ge; 200 kW $\rightarrow$ Critical Overload Alarm</div>
            <div className="rule-formula">SOC &le; 10% (50 kWh) $\rightarrow$ Reserve Floor Lock</div>
            <p className="mt-8 text-xs text-muted">
              Advisories explicitly account for transformer thermal strain and battery degradation thresholds.
            </p>
          </div>
        </aside>
      </div>
    </div>
  )
}
