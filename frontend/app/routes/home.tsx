import type { Route } from "./+types/home";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "New React Router App" }, //TODO change
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export default function Home() {
  return <div> wefwefwefwef </div>;
}
