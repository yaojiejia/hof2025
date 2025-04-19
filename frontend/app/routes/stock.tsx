import type { Route } from "./+types/stock";
import { useParams } from "react-router";

export default function Stock() {
    const { id } = useParams();
    return (
        <div>
            hi 
            {id}
        </div>
    )
}