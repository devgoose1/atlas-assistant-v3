import { useState, useRef, useEffect } from "react";
import type { Route } from "./+types/web-search";
import { AIAssistantButton } from "../components/ai-assistant-button";

interface SearchResult {
  type: string;
  title: string;
  content: string;
  url: string;
}

interface SearchResponse {
  success: boolean;
  data?: SearchResult[];
  error?: string;
}

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "WEB SEARCH - JARVIS" },
  ];
}

export default function WebSearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [lastQuery, setLastQuery] = useState("");

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/tools/execute`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tool: "web_search",
          query: query,
          max_results: 10
        })
      });

      const data: SearchResponse = await response.json();
      if (data.success && data.data) {
        setResults(data.data);
        setLastQuery(query);
      }
    } catch (error) {
      console.error("Search failed:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-cyan-400 font-mono">
      <AIAssistantButton />

      {/* Grid background */}
      <div className="fixed inset-0 opacity-10 pointer-events-none">
        <div 
          className="w-full h-full"
          style={{
            backgroundImage: `
              linear-gradient(0deg, transparent 24%, rgba(0, 255, 255, 0.05) 25%, rgba(0, 255, 255, 0.05) 26%, transparent 27%, transparent 74%, rgba(0, 255, 255, 0.05) 75%, rgba(0, 255, 255, 0.05) 76%, transparent 77%, transparent),
              linear-gradient(90deg, transparent 24%, rgba(0, 255, 255, 0.05) 25%, rgba(0, 255, 255, 0.05) 26%, transparent 27%, transparent 74%, rgba(0, 255, 255, 0.05) 75%, rgba(0, 255, 255, 0.05) 76%, transparent 77%, transparent)
            `,
            backgroundSize: '50px 50px'
          }}
        />
      </div>

      {/* Header */}
      <div className="relative z-10 border-b border-cyan-400 border-opacity-30 p-4">
        <a href="/" className="text-cyan-400 hover:text-cyan-300 text-sm mb-4 inline-block">
          ◄ MAIN MENU
        </a>
        <div className="max-w-4xl mx-auto">
          <div className="text-2xl font-bold tracking-widest">🌐 WEB SEARCH</div>
          <div className="text-xs text-cyan-300 mt-2">GLOBAL INFORMATION NETWORK ACCESS</div>
        </div>
      </div>

      {/* Main content */}
      <div className="relative z-10 max-w-4xl mx-auto p-8">
        {/* Search bar */}
        <form onSubmit={handleSearch} className="mb-8">
          <div className="border border-cyan-400 border-opacity-50">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="ENTER SEARCH QUERY..."
              className="w-full bg-black text-cyan-400 px-4 py-3 focus:outline-none placeholder-cyan-600 placeholder-opacity-50"
              disabled={loading}
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="mt-3 px-6 py-2 border border-cyan-400 bg-cyan-400 bg-opacity-10 text-cyan-400 hover:bg-opacity-20 transition-all disabled:opacity-50"
          >
            {loading ? "SEARCHING..." : "EXECUTE SEARCH"}
          </button>
        </form>

        {/* Results */}
        {results.length > 0 && (
          <div className="space-y-4">
            <div className="text-xs text-green-400">
              ◆ {results.length} RESULTS FOUND FOR: "{lastQuery}" ◆
            </div>
            {results.map((result, idx) => (
              <div key={idx} className="border border-cyan-400 border-opacity-30 p-4 hover:border-opacity-100 transition-all">
                <div className="text-sm text-cyan-300 mb-2">
                  [{result.type.toUpperCase()}]
                </div>
                <div className="font-bold text-cyan-400 mb-2">
                  {result.title}
                </div>
                <div className="text-sm text-gray-400 mb-3">
                  {result.content.substring(0, 200)}...
                </div>
                {result.url && (
                  <a
                    href={result.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xs text-blue-400 hover:text-blue-300 break-all"
                  >
                    → {result.url}
                  </a>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
