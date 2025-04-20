import type { Route } from "./+types/home";
import './home.css';
import Card from "./Components/Card";
import { homeData } from "./data";
import HeatMap from "./Components/Heatmap";
import Graph from "./Components/Graph";


export function meta({}: Route.MetaArgs) {
  return [
    { title: "New React Router App" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export async function loader() {
    try {
        const response = await fetch('http://3.145.78.241:5000/predict_market_price')
        const data = await response.json()
        

        // Get the last closing entry
        const lastClosingEntry = Object.entries(data.last_4_days_closing).at(-1); // Use .at(-1) for the last element
        const [lastDate, lastPrice] = lastClosingEntry || ["", 0]; // Destructure the date and price

        // Calculate the next date
        const nextDate = new Date(new Date(lastDate).getTime() + 24 * 60 * 60 * 1000).toISOString().split("T")[0];

        // Format historical data
        const historical_data = Object.entries(data.last_4_days_closing).map(([date, close]) => ({
            date,
            close,
        }));

        // Create full graph data
        const full_graph = [
            ...historical_data,
            {
                date: nextDate,
                close: data.expected_next_day_price,
                predicted: true,
            },
        ];

        // Construct the response object
        const res = {
            historical_data,
            full_graph,
            prediction: {
                nextDate,
                nextPrice: data.expected_next_day_price,
                percentChange: ((data.expected_next_day_price - lastPrice) / lastPrice) * 100,
            },
        };

        return res;
    } catch (error) {
        console.error("Error processing data:", error);
        throw new Response("Failed to load data", { status: 500 });
    }
}

export default function Home({ loaderData }: ComponentProps) {
  const data = loaderData;

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
      <Graph data={data.full_graph} />
    </Card>
  </div>;
}
