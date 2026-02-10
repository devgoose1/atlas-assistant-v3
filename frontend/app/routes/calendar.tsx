import type { Route } from "./+types/calendar";
import { AIAssistantButton } from "../components/ai-assistant-button";

export function meta({}: Route.MetaArgs) {
  return [{ title: "SCHEDULE - JARVIS" }];
}

export default function CalendarModule() {
  return (
    <div className="min-h-screen bg-black text-cyan-400 font-mono">
      <AIAssistantButton />
      <div className="fixed inset-0 opacity-10 pointer-events-none" style={{backgroundImage: "linear-gradient(0deg, transparent 24%, rgba(0, 255, 255, 0.05) 25%, rgba(0, 255, 255, 0.05) 26%, transparent 27%, transparent 74%, rgba(0, 255, 255, 0.05) 75%, rgba(0, 255, 255, 0.05) 76%, transparent 77%, transparent), linear-gradient(90deg, transparent 24%, rgba(0, 255, 255, 0.05) 25%, rgba(0, 255, 255, 0.05) 26%, transparent 27%, transparent 74%, rgba(0, 255, 255, 0.05) 75%, rgba(0, 255, 255, 0.05) 76%, transparent 77%, transparent)", backgroundSize: "50px 50px"}} />
      <div className="relative z-10 border-b border-cyan-400 border-opacity-30 p-4">
        <a href="/" className="text-cyan-400 hover:text-cyan-300 text-sm mb-4 inline-block">◄ MAIN MENU</a>
        <div className="max-w-4xl mx-auto">
          <div className="text-2xl font-bold tracking-widest">📅 SCHEDULE</div>
          <div className="text-xs text-cyan-300 mt-2">CALENDAR & TIME MANAGEMENT</div>
        </div>
      </div>
      <div className="relative z-10 max-w-4xl mx-auto p-8 text-center">
        <div className="border border-cyan-400 border-opacity-30 p-6 inline-block">
          <div className="text-xs text-green-400 mb-4">◆ MODULE STATUS ◆</div>
          <div className="text-sm">SCHEDULE SYSTEM INITIALIZING...</div>
          <div className="text-xs text-cyan-300 mt-4">Coming soon</div>
        </div>
      </div>
    </div>
  );
}
