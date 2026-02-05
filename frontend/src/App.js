import React, { useState, useEffect, useCallback } from "react";
import DealList from "./components/DealList";
import DealDetail from "./components/DealDetail";
import NewDealForm from "./components/NewDealForm";

function App() {
  const [selectedDealId, setSelectedDealId] = useState(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const refreshList = useCallback(() => {
    setRefreshTrigger(prev => prev + 1);
  }, []);

  return (
    <div style={{ maxWidth: "1200px", margin: "0 auto", padding: "20px", fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif", color: "#333" }}>
      <header style={{ borderBottom: "2px solid #eee", marginBottom: "30px", paddingBottom: "10px" }}>
        <h1>🤝 Deal Brief AI <span style={{ fontSize: "0.5em", verticalAlign: "middle", color: "#666" }}>v2.0</span></h1>
      </header>

      <div style={{ marginBottom: "40px" }}>
        <NewDealForm onDealCreated={(newId) => {
          refreshList();
          setSelectedDealId(newId);
        }} />
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "350px 1fr", gap: "30px" }}>
        <aside>
          <DealList onSelect={setSelectedDealId} refreshTrigger={refreshTrigger} selectedId={selectedDealId} />
        </aside>
        
        <main style={{ background: "#f9f9f9", padding: "20px", borderRadius: "12px", minHeight: "500px", border: "1px solid #eee" }}>
          {selectedDealId ? (
            <DealDetail dealId={selectedDealId} />
          ) : (
            <div style={{ textAlign: "center", marginTop: "100px", color: "#999" }}>
              <p style={{ fontSize: "48px" }}>📋</p>
              <p>Select a deal from the list or paste a new contract above to begin analysis.</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;