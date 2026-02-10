import { useState, useRef, useEffect } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export function AIAssistantButton() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "JARVIS READY. HOW CAN I ASSIST?"
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input;
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: userMessage }]);
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
      });

      const data = await response.json();
      setMessages(prev => [...prev, { role: "assistant", content: data.response }]);
    } catch (error) {
      console.error("Chat error:", error);
      setMessages(prev => [...prev, {
        role: "assistant",
        content: "COMMUNICATION ERROR. RETRY?"
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Floating button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`fixed bottom-6 right-6 z-50 w-16 h-16 rounded-full border-2 transition-all duration-300 flex items-center justify-center text-2xl font-bold ${
          isOpen
            ? "border-cyan-400 bg-cyan-400 bg-opacity-20 text-cyan-400"
            : "border-cyan-400 border-opacity-50 bg-black hover:border-opacity-100 text-cyan-400"
        }`}
      >
        ◆
      </button>

      {/* Chat panel */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 z-50 w-96 h-96 bg-black border-2 border-cyan-400 border-opacity-70 flex flex-col shadow-lg shadow-cyan-400/20">
          {/* Header */}
          <div className="border-b border-cyan-400 border-opacity-30 p-3 flex justify-between items-center">
            <div className="text-xs font-bold text-cyan-400 tracking-widest">
              JARVIS TERMINAL
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-cyan-400 hover:text-cyan-300"
            >
              ✕
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-3 space-y-3 font-mono text-sm">
            {messages.map((msg, idx) => (
              <div key={idx} className={`${msg.role === "user" ? "text-green-400" : "text-cyan-400"}`}>
                <div className="text-xs opacity-60 mb-1">
                  [{msg.role === "user" ? "INPUT" : "OUTPUT"}]
                </div>
                <div className="text-xs leading-relaxed whitespace-pre-wrap break-words">
                  {msg.content}
                </div>
              </div>
            ))}
            {loading && (
              <div className="text-cyan-400 animate-pulse text-xs">
                [PROCESSING...]
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <form onSubmit={sendMessage} className="border-t border-cyan-400 border-opacity-30 p-2 flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="COMMAND..."
              className="flex-1 bg-black text-cyan-400 px-2 py-1 text-xs focus:outline-none placeholder-cyan-600 placeholder-opacity-50 border border-cyan-400 border-opacity-20"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="px-3 py-1 border border-cyan-400 bg-cyan-400 bg-opacity-10 text-cyan-400 hover:bg-opacity-20 text-xs disabled:opacity-50 transition-all"
            >
              →
            </button>
          </form>
        </div>
      )}
    </>
  );
}
