import { useState } from "react";
import type { Route } from "./+types/home";

interface NavItem {
  id: string;
  label: string;
  path: string;
  icon: string;
  description: string;
}

const navItems: NavItem[] = [
  { id: "web-search", label: "WEB SEARCH", path: "/web-search", icon: "🌐", description: "Search the web" },
  { id: "todo", label: "MISSION LOG", path: "/todo", icon: "📋", description: "Task management" },
  { id: "notes", label: "DATABANK", path: "/notes", icon: "📝", description: "Knowledge base" },
  { id: "code", label: "CODE SUITE", path: "/code", icon: "💻", description: "Programming help" },
  { id: "cad", label: "DESIGN LAB", path: "/cad", icon: "⚙️", description: "Circuit & CAD" },
  { id: "calendar", label: "SCHEDULE", path: "/calendar", icon: "📅", description: "Calendar events" },
];

export function meta({}: Route.MetaArgs) {
  return [
    { title: "JARVIS - Main Interface" },
    { name: "description", content: "Your personal AI assistant" },
  ];
}

export default function Home() {
  const [selectedItem, setSelectedItem] = useState<string | null>(null);

  return (
    <div className="min-h-screen bg-black text-cyan-400 font-mono overflow-hidden relative">
      {/* Animated background grid */}
      <div className="absolute inset-0 opacity-10">
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

      {/* Top bar */}
      <div className="relative z-10 border-b border-cyan-400 border-opacity-30 p-4">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <div>
            <div className="text-2xl font-bold tracking-widest">
              ◆ J.A.R.V.I.S ◆
            </div>
            <div className="text-xs tracking-widest mt-1">
              JUST A RATHER VERY INTELLIGENT SYSTEM
            </div>
          </div>
          <div className="text-right">
            <div className="text-xs text-cyan-300">STATUS: OPERATIONAL</div>
            <div className="text-xs text-green-400">INTERFACE ACTIVE</div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="relative z-10 max-w-6xl mx-auto p-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-block p-4 border-2 border-cyan-400 border-opacity-50 bg-cyan-400 bg-opacity-5">
            <div className="text-xl tracking-widest mb-2">SYSTEM INTERFACE</div>
            <div className="text-xs text-cyan-300">Select operational module</div>
          </div>
        </div>

        {/* Grid of tools */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {navItems.map((item) => (
            <a
              key={item.id}
              href={item.path}
              className="group relative"
              onMouseEnter={() => setSelectedItem(item.id)}
              onMouseLeave={() => setSelectedItem(null)}
            >
              {/* Border glow effect */}
              <div className={`absolute inset-0 border-2 transition-all duration-300 ${
                selectedItem === item.id
                  ? "border-cyan-400 shadow-lg shadow-cyan-400/50"
                  : "border-cyan-400 border-opacity-30"
              }`} />

              {/* Hover overlay */}
              <div className={`absolute inset-0 bg-cyan-400 opacity-0 group-hover:opacity-5 transition-opacity duration-300`} />

              {/* Content */}
              <div className="relative p-6 h-full flex flex-col">
                <div className="text-4xl mb-3 opacity-70 group-hover:opacity-100 transition-opacity">
                  {item.icon}
                </div>
                <div className="text-sm font-bold tracking-widest mb-2">
                  {item.label}
                </div>
                <div className="text-xs text-cyan-300 opacity-60 group-hover:opacity-100 transition-opacity">
                  {item.description}
                </div>

                {/* Scan line effect on hover */}
                {selectedItem === item.id && (
                  <div className="absolute inset-0 pointer-events-none">
                    <div className="absolute inset-0 bg-gradient-to-b from-cyan-400 via-transparent to-transparent opacity-20 animate-pulse" />
                  </div>
                )}
              </div>
            </a>
          ))}
        </div>
      </div>

      {/* Bottom status bar */}
      <div className="fixed bottom-0 left-0 right-0 border-t border-cyan-400 border-opacity-30 bg-black bg-opacity-50 backdrop-blur p-3">
        <div className="max-w-6xl mx-auto flex justify-between text-xs">
          <div>◆ SYSTEMS READY ◆</div>
          <div>6 MODULES ACTIVE</div>
          <div>AI ASSISTANT AVAILABLE</div>
        </div>
      </div>
    </div>
  );
}
