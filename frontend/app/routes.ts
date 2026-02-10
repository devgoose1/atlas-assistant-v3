import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
    index("routes/home.tsx"),
    route("browser", "routes/browser.tsx"),
    route("jarvis", "routes/jarvis.tsx"),
] satisfies RouteConfig;
