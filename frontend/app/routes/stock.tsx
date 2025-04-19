import type { Route } from "./+types/stock";
import { useParams } from "react-router";
import Card from "./Components/Card";
import Heatmap from "./Components/Heatmap";

export async function loader({ params }: Route.LoaderArgs) {
    return params;
    // todo replace with return await fetch(params)
}

export default function Stock({ loaderData }: Route.ComponentProps) {
    const { id } = loaderData;
    return (
        <div>
            hi 
            {id}
            <Card>
            </Card>
        </div>
    )
}


// HydrateFallback is rendered while the client loader is running
export function HydrateFallback() {
    return <div>Loading...</div>;
  }