import React, { useEffect, useState } from "react";

export default function DealList({ onSelect, refreshTrigger, selectedId }) {
  const [deals, setDeals] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/deals")
      .then((res) => res.json())
      .then(setDeals);
  }, [refreshTrigger]);

  const getStatusStyle = (status) => ({
    fontSize: "10px",
    padding: "2px 6px",
    borderRadius: "10px",
    marginLeft: "8px",
    backgroundColor: status === "error" ? "#ff4d4f" : "#52c41a",
    color: "white",
    textTransform: "uppercase"
  });

  return (
    <div>
      <h3 style={{ borderLeft: "4px solid #007bff", paddingLeft: "10px" }}>History</h3>
      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
        {deals.map((deal) => (
          <div 
            key={deal.id}
            onClick={() => onSelect(deal.id)}
            style={{
              padding: "12px",
              borderRadius: "6px",
              cursor: "pointer",
              border: selectedId === deal.id ? "1px solid #007bff" : "1px solid #eee",
              backgroundColor: selectedId === deal.id ? "#e6f7ff" : "white",
              transition: "0.2s"
            }}
          >
            <div style={{ fontWeight: "bold" }}>
              Deal #{deal.id} 
              <span style={getStatusStyle(deal.status)}>{deal.status}</span>
            </div>
            <div style={{ fontSize: "0.8em", color: "#888", marginTop: "4px" }}>
              {new Date(deal.created_at).toLocaleString()}
            </div>
            {deal.error && (
              <div style={{ color: "#ff4d4f", fontSize: "0.75em", marginTop: "4px", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                ⚠️ {deal.error}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}