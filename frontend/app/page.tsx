"use client";

import { useState } from "react";

export default function Home() {
  const [clientId, setClientId] = useState("demo-client");
  const [transcript, setTranscript] = useState("");
  const [summary, setSummary] = useState<string[] | null>(null);

  async function runSummary() {
    const res = await fetch("http://localhost:8000/summaries", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ client_id: clientId, transcript }),
    });
    const data = await res.json();
    setSummary(data.bullets || []);
  }

  return (
    <main style={{ maxWidth: 880, margin: "40px auto", padding: 24 }}>
      <h1>AI Secretary — Live Demo</h1>
      <p>Paste a sample call transcript and generate a quick summary.</p>

      <label>Client ID</label>
      <input value={clientId} onChange={(e) => setClientId(e.target.value)} style={{ width: "100%", padding: 8, marginBottom: 8 }} />

      <label>Transcript</label>
      <textarea value={transcript} onChange={(e) => setTranscript(e.target.value)} rows={8} style={{ width: "100%", padding: 8 }} />

      <div style={{ display: "flex", gap: 12, marginTop: 12 }}>
        <button onClick={runSummary}>Summarize</button>
      </div>

      {summary && (
        <div style={{ marginTop: 24 }}>
          <h2>Summary</h2>
          <ul>
            {summary.map((s, i) => (<li key={i}>{s}</li>))}
          </ul>
        </div>
      )}

      <hr style={{ margin: "36px 0" }} />

      <h2>Become a Client</h2>
      <p>Tell us about your use case and we'll reach out.</p>
      <form action="https://example.com/lead-capture" method="POST" onSubmit={(e) => e.preventDefault()}>
        <input placeholder="Your name" style={{ width: "100%", padding: 8, marginBottom: 8 }} />
        <input placeholder="Email" type="email" style={{ width: "100%", padding: 8, marginBottom: 8 }} />
        <textarea placeholder="How can the AI secretary help?" rows={4} style={{ width: "100%", padding: 8 }} />
        <button>Submit</button>
      </form>
    </main>
  );
}
