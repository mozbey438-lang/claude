import { useEffect } from "react";
import { useWebSocket } from "./hooks/useWebSocket";
import { useProjectStore } from "./stores/projectStore";
import { api } from "./api/client";

export default function App() {
  const { setProjects, activeProject } = useProjectStore();

  useWebSocket((event) => {
    console.log("[ws]", event);
  });

  useEffect(() => {
    api.get("/api/projects").then((r) => setProjects(r.data));
  }, []);

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "monospace", background: "#0d0d0d", color: "#e0e0e0" }}>
      {/* Sidebar */}
      <aside style={{ width: 220, borderRight: "1px solid #222", padding: 16 }}>
        <div style={{ fontSize: 14, fontWeight: "bold", marginBottom: 16, color: "#7c6af7" }}>STUDIO</div>
        <nav style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          {["Projeler", "Blender", "AI", "3D Tarama", "Export"].map((label) => (
            <button key={label} style={{ background: "none", border: "none", color: "#aaa", textAlign: "left", cursor: "pointer", padding: "6px 8px", borderRadius: 4 }}>
              {label}
            </button>
          ))}
        </nav>
      </aside>

      {/* Main */}
      <main style={{ flex: 1, padding: 24 }}>
        <h1 style={{ fontSize: 18, margin: 0, marginBottom: 16 }}>
          {activeProject ? activeProject.name : "Proje Seç"}
        </h1>
        <p style={{ color: "#666", fontSize: 13 }}>Panel burada görünecek.</p>
      </main>

      {/* Status bar */}
      <div style={{ position: "fixed", bottom: 0, left: 0, right: 0, height: 24, background: "#7c6af7", display: "flex", alignItems: "center", padding: "0 12px", fontSize: 11, color: "#fff" }}>
        Backend: localhost:8000 &nbsp;|&nbsp; Blender: bağlantı bekleniyor &nbsp;|&nbsp; Ollama: llama3.2:3b
      </div>
    </div>
  );
}
