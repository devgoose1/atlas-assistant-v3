import { useState, useEffect } from "react";
import type { Route } from "./+types/todo";
import { AIAssistantButton } from "../components/ai-assistant-button";

interface Todo {
  id: number;
  text: string;
  priority: "high" | "normal" | "low";
  done: boolean;
  created?: string;
}

interface TodoResponse {
  success: boolean;
  data?: Todo | Todo[];
  error?: string;
}

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "MISSION LOG - JARVIS" },
  ];
}

export default function TodoModule() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTodo, setNewTodo] = useState("");
  const [priority, setPriority] = useState<"high" | "normal" | "low">("normal");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTodos();
  }, []);

  const loadTodos = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/tools/execute`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tool: "todo",
          query: "",
          action: "list"
        })
      });

      const data: TodoResponse = await response.json();
      if (data.success && Array.isArray(data.data)) {
        setTodos(data.data);
      }
    } catch (error) {
      console.error("Failed to load todos:", error);
    } finally {
      setLoading(false);
    }
  };

  const addTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTodo.trim()) return;

    try {
      const response = await fetch(`${API_BASE_URL}/api/tools/execute`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tool: "todo",
          query: newTodo,
          action: "add",
          priority: priority
        })
      });

      const data: TodoResponse = await response.json();
      if (data.success && data.data && !Array.isArray(data.data)) {
        setTodos([...todos, data.data as Todo]);
        setNewTodo("");
      }
    } catch (error) {
      console.error("Failed to add todo:", error);
    }
  };

  const toggleTodo = async (id: number) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/tools/execute`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tool: "todo",
          query: id.toString(),
          action: "done"
        })
      });

      const data: TodoResponse = await response.json();
      if (data.success) {
        loadTodos();
      }
    } catch (error) {
      console.error("Failed to toggle todo:", error);
    }
  };

  const removeTodo = async (id: number) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/tools/execute`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tool: "todo",
          query: id.toString(),
          action: "remove"
        })
      });

      const data: TodoResponse = await response.json();
      if (data.success) {
        loadTodos();
      }
    } catch (error) {
      console.error("Failed to remove todo:", error);
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
          <div className="text-2xl font-bold tracking-widest">📋 MISSION LOG</div>
          <div className="text-xs text-cyan-300 mt-2">TASK MANAGEMENT SYSTEM</div>
        </div>
      </div>

      {/* Main content */}
      <div className="relative z-10 max-w-4xl mx-auto p-8">
        {/* Add new todo */}
        <form onSubmit={addTodo} className="mb-8 border border-cyan-400 border-opacity-50 p-4">
          <div className="mb-3">
            <input
              type="text"
              value={newTodo}
              onChange={(e) => setNewTodo(e.target.value)}
              placeholder="NEW MISSION..."
              className="w-full bg-black text-cyan-400 px-3 py-2 focus:outline-none placeholder-cyan-600 placeholder-opacity-50 text-sm"
            />
          </div>
          <div className="flex gap-3">
            <select
              value={priority}
              onChange={(e) => setPriority(e.target.value as any)}
              className="bg-black text-cyan-400 border border-cyan-400 border-opacity-30 px-3 py-2 text-sm focus:outline-none"
            >
              <option value="low">🟢 LOW</option>
              <option value="normal">🟡 NORMAL</option>
              <option value="high">🔴 HIGH</option>
            </select>
            <button
              type="submit"
              className="px-4 py-2 border border-cyan-400 bg-cyan-400 bg-opacity-10 text-cyan-400 hover:bg-opacity-20 transition-all text-sm"
            >
              ADD MISSION
            </button>
          </div>
        </form>

        {/* Todos list */}
        <div className="space-y-2">
          {loading ? (
            <div className="text-cyan-300 text-sm">LOADING MISSIONS...</div>
          ) : todos.length === 0 ? (
            <div className="text-cyan-300 text-sm">NO MISSIONS ACTIVE</div>
          ) : (
            todos.map((todo) => (
              <div
                key={todo.id}
                className={`border p-3 transition-all ${
                  todo.done
                    ? "border-cyan-400 border-opacity-20 opacity-50"
                    : "border-cyan-400 border-opacity-50 hover:border-opacity-100"
                }`}
              >
                <div className="flex items-center gap-3">
                  <button
                    onClick={() => toggleTodo(todo.id)}
                    className="text-lg"
                  >
                    {todo.done ? "✓" : "○"}
                  </button>
                  <div className="flex-1">
                    <div className={`text-sm ${todo.done ? "line-through" : ""}`}>
                      {todo.text}
                    </div>
                    <div className="text-xs text-cyan-300 opacity-60">
                      {todo.priority === "high" && "🔴 HIGH PRIORITY"}
                      {todo.priority === "normal" && "🟡 NORMAL"}
                      {todo.priority === "low" && "🟢 LOW"}
                    </div>
                  </div>
                  <button
                    onClick={() => removeTodo(todo.id)}
                    className="text-xs text-red-400 hover:text-red-300"
                  >
                    ✕
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
