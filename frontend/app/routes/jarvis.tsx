import type { Route } from "./+types/jarvis";
import { JarvisChat } from "../pages/jarvis-chat/jarvis-chat";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "JARVIS Assistant" },
    { name: "description", content: "Your local AI assistant" },
  ];
}

export default function Jarvis() {
  return <JarvisChat />;
}
