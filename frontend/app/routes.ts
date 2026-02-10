import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
    index("routes/home.tsx"),
    route("browser", "routes/browser.tsx"),
    route("jarvis", "routes/jarvis.tsx"),
    route("web-search", "routes/web-search.tsx"),
    route("todo", "routes/todo.tsx"),
    route("notes", "routes/notes.tsx"),
    route("code", "routes/code.tsx"),
    route("cad", "routes/cad.tsx"),
    route("calendar", "routes/calendar.tsx"),
] satisfies RouteConfig;
