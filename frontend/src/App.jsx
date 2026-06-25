import { useState } from "react"
import axios from "axios"

const SUGGESTIONS = [
  { category: "ONBOARDING", text: "How do I set up the VPN at Northwind?" },
  { category: "TROUBLESHOOTING", text: "Has anyone seen Kafka consumer lag before?" },
  { category: "DOCUMENTATION", text: "Summarize the Kubernetes deployment docs" },
  { category: "INCIDENTS", text: "What is Northwind's deployment policy for Singapore?" },
]

const CATEGORY_COLORS = {
  ONBOARDING: "#3b82f6",
  TROUBLESHOOTING: "#22c55e",
  DOCUMENTATION: "#f59e0b",
  INCIDENTS: "#ef4444",
}

export default function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [started, setStarted] = useState(false)

  const sendMessage = async (question) => {
    if (!question.trim() || loading) return
    setStarted(true)
    setLoading(true)

    const userMsg = { role: "user", content: question }
    setMessages(prev => [...prev, userMsg])
    setInput("")

    try {
      const res = await axios.post("http://localhost:8080/ask", { question })
      const { answer, citations, escalated } = res.data

      const botMsg = { role: "bot", content: answer, citations, escalated }
      setMessages(prev => [...prev, botMsg])
    } catch (err) {
      setMessages(prev => [...prev, {
        role: "bot",
        content: "Error connecting to the server. Make sure FastAPI is running on port 8000.",
        citations: [],
        escalated: false,
        error: true,
      }])
    }
    setLoading(false)
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      sendMessage(input)
    }
  }

  return (
    <div style={styles.root}>
      {/* Sidebar */}
      <div style={styles.sidebar}>
        <div style={styles.sidebarHeader}>
          <div style={styles.logo}>✦</div>
          <span style={styles.logoText}>CoPilot</span>
        </div>
        <button style={styles.newChat} onClick={() => { setMessages([]); setStarted(false) }}>
          + New conversation
        </button>
        <div style={styles.sidebarSection}>RECENT</div>
        {["VPN Setup Help", "Kafka Consumer Lag", "K8s Deployment Docs", "Incident Response SOP"].map((t, i) => (
          <div key={i} style={styles.sidebarItem}>{t}</div>
        ))}
        <div style={styles.sidebarFooter}>
          <div style={styles.syncDot} />
          <div>
            <div style={styles.syncText}>Knowledge base synced</div>
            <div style={styles.syncSub}>749 chunks · Northwind Systems</div>
          </div>
        </div>
      </div>

      {/* Main */}
      <div style={styles.main}>
        {!started ? (
          /* Hero screen */
          <div style={styles.hero}>
            <div style={styles.badge}>INTERNAL · NORTHWIND SYSTEMS</div>
            <h1 style={styles.heroTitle}>What can I help you<br />find today?</h1>
            <p style={styles.heroSub}>
              Ask anything about internal procedures, troubleshooting runbooks, or past incidents.
            </p>
            <div style={styles.cards}>
              {SUGGESTIONS.map((s, i) => (
                <div key={i} style={styles.card} onClick={() => sendMessage(s.text)}>
                  <div style={{ ...styles.cardDot, background: CATEGORY_COLORS[s.category] }} />
                  <div style={styles.cardCategory}>{s.category}</div>
                  <div style={styles.cardText}>{s.text}</div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          /* Chat window */
          <div style={styles.chatWindow}>
            {messages.map((msg, i) => (
              <div key={i} style={msg.role === "user" ? styles.userRow : styles.botRow}>
                {msg.role === "bot" && <div style={styles.botAvatar}>✦</div>}
                <div style={msg.role === "user" ? styles.userBubble : msg.escalated ? styles.escalateBubble : msg.error ? styles.errorBubble : styles.botBubble}>
                  {msg.escalated && <div style={styles.escalateHeader}>⚠️ Escalated to Human Support</div>}
                  <div style={styles.msgText}>{msg.content}</div>
                  {msg.citations && msg.citations.length > 0 && (
                    <div style={styles.citations}>
                      <div style={styles.citationsTitle}>Sources</div>
                      {msg.citations.map((c, j) => (
                        <div key={j} style={styles.citation}>
                          {c.type === "ticket" ? "🎫" : "📄"} [{c.n}] <span style={styles.citationSource}>{c.source}</span> — page {c.page}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div style={styles.botRow}>
                <div style={styles.botAvatar}>✦</div>
                <div style={styles.botBubble}>
                  <div style={styles.typing}>
                    <span style={styles.dot} />
                    <span style={styles.dot} />
                    <span style={styles.dot} />
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Input box */}
        <div style={styles.inputArea}>
          <div style={styles.inputBox}>
            <textarea
              style={styles.textarea}
              placeholder="Ask about Northwind procedures, incidents, or docs..."
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              rows={1}
            />
            <button
              style={{ ...styles.sendBtn, opacity: loading || !input.trim() ? 0.4 : 1 }}
              onClick={() => sendMessage(input)}
              disabled={loading || !input.trim()}
            >
              ↑
            </button>
          </div>
          <div style={styles.disclaimer}>Responses are grounded in Northwind docs · verify critical info</div>
        </div>
      </div>
    </div>
  )
}

const styles = {
  root: { display: "flex", height: "100vh", background: "#0d1117", color: "#e6edf3", fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif", overflow: "hidden" },
  sidebar: { width: 240, background: "#010409", borderRight: "1px solid #21262d", display: "flex", flexDirection: "column", padding: "16px 0" },
  sidebarHeader: { display: "flex", alignItems: "center", gap: 10, padding: "0 16px 16px" },
  logo: { width: 32, height: 32, background: "linear-gradient(135deg, #7c3aed, #ec4899)", borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16 },
  logoText: { fontSize: 15, fontWeight: 600, color: "#e6edf3" },
  newChat: { margin: "0 12px 16px", padding: "8px 12px", background: "transparent", border: "1px solid #21262d", borderRadius: 8, color: "#8b949e", cursor: "pointer", fontSize: 13, textAlign: "left" },
  sidebarSection: { padding: "4px 16px 8px", fontSize: 11, color: "#484f58", letterSpacing: 1 },
  sidebarItem: { padding: "8px 16px", fontSize: 13, color: "#8b949e", cursor: "pointer", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" },
  sidebarFooter: { marginTop: "auto", padding: "16px", display: "flex", alignItems: "center", gap: 10, borderTop: "1px solid #21262d" },
  syncDot: { width: 8, height: 8, borderRadius: "50%", background: "#22c55e", flexShrink: 0 },
  syncText: { fontSize: 12, color: "#8b949e" },
  syncSub: { fontSize: 11, color: "#484f58" },
  main: { flex: 1, display: "flex", flexDirection: "column", overflow: "hidden" },
  hero: { flex: 1, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: "40px 24px", overflowY: "auto" },
  badge: { background: "#161b22", border: "1px solid #21262d", borderRadius: 20, padding: "4px 14px", fontSize: 11, color: "#8b949e", letterSpacing: 1, marginBottom: 24 },
  heroTitle: { fontSize: 42, fontWeight: 700, textAlign: "center", lineHeight: 1.2, margin: "0 0 16px", color: "#e6edf3" },
  heroSub: { fontSize: 15, color: "#8b949e", textAlign: "center", maxWidth: 500, margin: "0 0 40px", lineHeight: 1.6 },
  cards: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, width: "100%", maxWidth: 680 },
  card: { background: "#161b22", border: "1px solid #21262d", borderRadius: 12, padding: "16px", cursor: "pointer", transition: "border-color 0.2s" },
  cardDot: { width: 32, height: 32, borderRadius: 8, marginBottom: 12 },
  cardCategory: { fontSize: 11, color: "#8b949e", letterSpacing: 1, marginBottom: 6 },
  cardText: { fontSize: 14, color: "#e6edf3", lineHeight: 1.5 },
  chatWindow: { flex: 1, overflowY: "auto", padding: "24px 40px", display: "flex", flexDirection: "column", gap: 20 },
  userRow: { display: "flex", justifyContent: "flex-end" },
  botRow: { display: "flex", gap: 12, alignItems: "flex-start" },
  botAvatar: { width: 28, height: 28, borderRadius: "50%", background: "linear-gradient(135deg, #7c3aed, #ec4899)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 12, flexShrink: 0 },
  userBubble: { background: "#1f6feb", color: "#fff", padding: "10px 14px", borderRadius: "12px 12px 2px 12px", fontSize: 14, maxWidth: "70%", lineHeight: 1.6 },
  botBubble: { background: "#161b22", border: "1px solid #21262d", padding: "12px 16px", borderRadius: "2px 12px 12px 12px", fontSize: 14, maxWidth: "80%", lineHeight: 1.7 },
  escalateBubble: { background: "#1a0a0a", border: "1px solid #7f1d1d", padding: "12px 16px", borderRadius: "2px 12px 12px 12px", fontSize: 14, maxWidth: "80%", lineHeight: 1.7 },
  errorBubble: { background: "#1a0a0a", border: "1px solid #484f58", padding: "12px 16px", borderRadius: "2px 12px 12px 12px", fontSize: 14, maxWidth: "80%", color: "#8b949e" },
  escalateHeader: { fontWeight: 600, color: "#f87171", marginBottom: 8 },
  msgText: { whiteSpace: "pre-wrap", color: "#e6edf3" },
  citations: { marginTop: 12, paddingTop: 12, borderTop: "1px solid #21262d" },
  citationsTitle: { fontSize: 12, color: "#8b949e", marginBottom: 6 },
  citation: { fontSize: 12, color: "#8b949e", marginBottom: 4 },
  citationSource: { color: "#58a6ff" },
  typing: { display: "flex", gap: 4, alignItems: "center", padding: "4px 0" },
  dot: { width: 6, height: 6, borderRadius: "50%", background: "#484f58", animation: "pulse 1.4s infinite" },
  inputArea: { padding: "16px 40px 20px", borderTop: "1px solid #21262d" },
  inputBox: { display: "flex", gap: 10, alignItems: "flex-end", background: "#161b22", border: "1px solid #21262d", borderRadius: 12, padding: "10px 12px" },
  textarea: { flex: 1, background: "transparent", border: "none", outline: "none", color: "#e6edf3", fontSize: 14, resize: "none", fontFamily: "inherit", lineHeight: 1.5 },
  sendBtn: { width: 32, height: 32, borderRadius: 8, background: "#1f6feb", border: "none", color: "#fff", fontSize: 16, cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 },
  disclaimer: { fontSize: 11, color: "#484f58", textAlign: "center", marginTop: 8 },
}