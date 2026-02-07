import type { Route } from "./+types/browser";
import { ServiceBrowser } from "../pages/service-browser/service-browser";

export function meta({}: Route.MetaArgs) {
    return [
        { title: "Service Browser" },
        { name: "description", content: "Browse your services!" },
    ];
}

export default function Browser() {
    return <ServiceBrowser />;
}