import './ProgressBar.css'

export default function ProgressBar({ filled, total }) {
  const pct = total > 0 ? (filled / total) * 100 : 0

  return (
    <div className="progress-wrapper">
      <div className="progress-label">{filled} / {total} FILLED</div>
      <div className="progress-track">
        <div className="progress-fill" style={{ width: `${pct}%` }}>
          <div className="progress-texture" />
        </div>
      </div>
    </div>
  )
}
