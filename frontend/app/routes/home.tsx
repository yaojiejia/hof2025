import type { Route } from "./+types/home";
import './home.css';
import Card from "./Components/Card";
import { homeData } from "./data";
import HeatMap from "./Components/Heatmap";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "New React Router App" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export default function Home() {
  return <div className="home">
    {/* Market Summary */}
    <div className="home-title">
      <h1> Market Summary </h1>
    </div>
    <Card>
      <div className="market-entries">
        { homeData.marketSummary.map(({ name, value }: {name: string; value: string;}, index: number) => {
          return <div className="market-entry" key={index}>
            <p> {name} </p>
            <h2> {value} </h2>
          </div>
        }) }
      </div>
    </Card>

    {/* Heatmap */}
    <div className="home-title">
      <h1> Heatmap </h1>
    </div>
    <Card>
      <HeatMap />
    </Card>

    {/* Predictions */}
    <div className="home-title">
      <h1> Predictions </h1>
    </div>
    <Card>
      <h1> Predictions... </h1>
    </Card>
  </div>;
}
