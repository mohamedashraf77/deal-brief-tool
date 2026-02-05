import React, { useEffect, useState } from "react";

export default function DealDetail({ dealId }) {
  const [deal, setDeal] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:8000/deals/${dealId}`)
      .then((res) => res.json())
      .then(setDeal)
      .catch(err => console.error("Fetch error:", err));
  }, [dealId]);

  if (!deal) return <div style={{ padding: "20px" }}>Loading Analysis...</div>;

  const { entities, investment_brief, tags, status, error, raw_text, created_at } = deal;

  return (
    <div style={{ animation: "fadeIn 0.3s ease-in" }}>
      {/* Header Section */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "20px" }}>
        <div>
          <h2 style={{ margin: 0, color: "#003366" }}>
            {entities?.company || `Deal #${dealId}`}
          </h2>
          <p style={{ color: "#666", fontSize: "0.9em" }}>
            Analyzed on {new Date(created_at).toLocaleDateString()}
          </p>
        </div>
        <div style={{ display: "flex", gap: "5px", flexWrap: "wrap", justifyContent: "flex-end", maxWidth: "200px" }}>
          {tags?.map((tag, i) => (
            <span key={i} style={{ backgroundColor: "#e6f7ff", color: "#1890ff", padding: "2px 8px", borderRadius: "4px", fontSize: "12px", border: "1px solid #91d5ff" }}>
              {tag}
            </span>
          ))}
        </div>
      </div>

      {/* Error Callout */}
      {status === "error" && (
        <div style={{ backgroundColor: "#fff2f0", border: "1px solid #ffccc7", padding: "15px", borderRadius: "8px", marginBottom: "20px", color: "#ff4d4f" }}>
          <strong>⚠️ Analysis Error:</strong> {error}
        </div>
      )}

      {/* Investment Brief */}
      <section style={{ marginBottom: "30px" }}>
        <h3 style={{ borderBottom: "1px solid #eee", paddingBottom: "5px" }}>Investment Brief</h3>
        <p style={{ lineHeight: "1.6", color: "#444", whiteSpace: "pre-wrap" }}>
          {investment_brief || "No brief generated for this deal."}
        </p>
      </section>

      {/* Entities Grid */}
      <section style={{ marginBottom: "30px" }}>
        <h3 style={{ borderBottom: "1px solid #eee", paddingBottom: "5px" }}>Core Entities</h3>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "15px" }}>
          <DataPoint label="Sector" value={entities?.sector} />
          <DataPoint label="Geography" value={entities?.geography} />
          <DataPoint label="Stage" value={entities?.stage} />
          <DataPoint label="Round Size" value={entities?.round_size} />
          <DataPoint label="Founders" value={entities?.founders?.join(", ")} />
        </div>
      </section>

      {/* Notable Metrics */}
      {entities?.notable_metrics?.length > 0 && (
        <section style={{ marginBottom: "30px" }}>
          <h4 style={{ color: "#555" }}>Key Metrics</h4>
          <ul style={{ background: "#fff", padding: "15px 35px", borderRadius: "8px", border: "1px solid #eee" }}>
            {entities.notable_metrics.map((m, i) => (
              <li key={i} style={{ marginBottom: "5px" }}>{m}</li>
            ))}
          </ul>
        </section>
      )}

      {/* Raw Text Accordion (Simplified) */}
      <details style={{ marginTop: "40px", cursor: "pointer" }}>
        <summary style={{ color: "#888", fontSize: "0.85em" }}>View Source Text</summary>
        <pre style={{ background: "#f5f5f5", padding: "15px", borderRadius: "4px", fontSize: "11px", overflowX: "auto", marginTop: "10px" }}>
          {raw_text}
        </pre>
      </details>
    </div>
  );
}

// Helper component for the grid
function DataPoint({ label, value }) {
  return (
    <div style={{ background: "#ffffff", padding: "10px", borderRadius: "6px", border: "1px solid #f0f0f0" }}>
      <div style={{ fontSize: "0.75em", color: "#999", textTransform: "uppercase", letterSpacing: "0.5px" }}>{label}</div>
      <div style={{ fontWeight: "500", color: "#333" }}>{value || "N/A"}</div>
    </div>
  );
}