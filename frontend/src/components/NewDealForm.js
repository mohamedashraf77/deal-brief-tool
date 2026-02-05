import React, { useState } from "react";

export default function NewDealForm({ onDealCreated }) {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:8000/deal", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      const data = await response.json();

      if (!response.ok) {
        // This handles the 400 error (Token Limit) from your API
        throw new Error(data.detail || "Failed to process deal");
      }

      setText("");
      onDealCreated(data.id);
    } catch (err) {
      setError(err.message);
      // We still refresh the list because your API saves the "error" state to the DB!
      onDealCreated(null); 
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ background: "#fff", padding: "20px", borderRadius: "8px", boxShadow: "0 2px 10px rgba(0,0,0,0.1)" }}>
      <h3>Analyze New Contract</h3>
      <form onSubmit={handleSubmit}>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste deal text here..."
          style={{ width: "100%", height: "120px", padding: "10px", borderRadius: "4px", border: "1px solid #ccc", boxSizing: "border-box" }}
          required
        />
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: "10px" }}>
          <span style={{ color: "red", fontSize: "0.9em" }}>{error}</span>
          <button 
            type="submit" 
            disabled={loading}
            style={{ 
              padding: "10px 25px", 
              backgroundColor: loading ? "#ccc" : "#007bff", 
              color: "white", 
              border: "none", 
              borderRadius: "4px", 
              cursor: "pointer",
              fontWeight: "bold"
            }}
          >
            {loading ? "Processing..." : "Run Analysis"}
          </button>
        </div>
      </form>
    </div>
  );
}