import { useEffect, useState } from "react";
import { Bug, Code2, ShieldCheck } from "lucide-react";
import { checkBackend } from "./services/api";

function App() {
  const [status, setStatus] = useState("Checking...");

  useEffect(() => {
    checkBackend()
      .then((data) => setStatus(data.status))
      .catch(() => setStatus("Disconnected"));
  }, []);

  return (
    <main style={{
      minHeight: "100vh",
      background: "#0b1020",
      color: "#ffffff",
      fontFamily: "Inter, Arial, sans-serif",
      padding: "40px"
    }}>
      <header style={{
        display: "flex",
        alignItems: "center",
        gap: "12px"
      }}>
        <Bug size={32} color="#a78bfa" />
        <h1>DebugMind AI</h1>
      </header>

      <section style={{
        maxWidth: "850px",
        margin: "100px auto",
        textAlign: "center"
      }}>
        <Code2 size={60} color="#a78bfa" />

        <h1 style={{ fontSize: "42px" }}>
          Debug Smarter. Code Better.
        </h1>

        <p style={{ color: "#94a3b8", fontSize: "17px" }}>
          Your intelligent AI-powered debugging assistant.
        </p>

        <div style={{
          marginTop: "35px",
          padding: "20px",
          background: "#172033",
          borderRadius: "12px"
        }}>
          <ShieldCheck color="#22c55e" />
          <h3>Backend Connection</h3>
          <p>API Status: {status}</p>
        </div>
      </section>
    </main>
  );
}

export default App;
