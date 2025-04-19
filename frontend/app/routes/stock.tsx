import { useParams } from "react-router";
import Card from "./Components/Card";
import { useEffect, useState } from "react";
import Graph from "./Components/Graph";

// Define inline types instead of importing them
interface LoaderArgs {
  params: {
    id: string;
    [key: string]: string | undefined;
  };
}

interface StockData {
  name: string;
  id: string;
  currentPrice: number;
  pred: {
    nextDate: string;
    nextPrice: number;
    change: number;
    percentChange: number;
  };
  market_sentiment: number;
  historical_data: Array<Object>;
}

interface ComponentProps {
  loaderData: StockData;
}

export async function loader({ params }: LoaderArgs) {
  const id = params.id
  try {
    const predictRes = await fetch(`http://3.145.78.241:5000/predict_ticker_price?ticker=${id}`)
    const data = await predictRes.json()
    const lastClosingEntry = Object.entries(data.last_4_days_closing).at(-1); // Use .at(-1) for the last element
    const [lastDate, lastPrice] = lastClosingEntry || ["", 0]; // Destructure the date and price
    const nextDate = new Date(new Date(lastDate).getTime() + 24 * 60 * 60 * 1000).toISOString().split('T')[0]

    const historical_data = Object.entries(data.last_4_days_closing).map(([date, close]) => ({date, close}))
    const full_graph = [...historical_data]
    full_graph.push(
        {
            date: nextDate,
            close: data.expected_next_day_price,
            predicted: true
        })

    const res = {
      name: data.company_name,
      id: data.ticker,
      currentPrice: Number(lastPrice), // Ensure this is a number
      pred: {
        // next day after lastday
        nextDate: nextDate,
        nextPrice: data.expected_next_day_price,
        change: data.prediction,
        percentChange: ((data.expected_next_day_price - data.latest_closing_price) / data.latest_closing_price) * 100,
      },
      market_sentiment: data.avg_sentiment,
      historical_data: historical_data,
      full_graph: full_graph
    };
    console.log(res)
    return res
  } catch (error) {
    console.error(error)
    throw error; // Make sure errors are properly propagated
  }
}

export default function Stock({ loaderData }: ComponentProps) {
  const data = loaderData;
  return (
    <>
      <div className="cards-container">
        <strong>{data.name}</strong> {data.id.toUpperCase()}
      </div>
      <div className="cards-container">
        <div className="pt-6 flex justify-between gap-5">
          <Card className="w-60 h-20">
            <p className="text-sm">Current Price</p>
            <div>
              ${data.currentPrice?.toFixed(2)}
            </div>
          </Card>
          <Card className="w-60 h-20">
            <p className="text-sm">Predicted Price</p>
            <div>
              ${data.pred.nextPrice?.toFixed(2)}
              <span className={data.pred.change > 0 ? "text-green-500" : "text-red-500"}>
                {data.pred.change > 0 ? " +" : " "}{data.pred.percentChange?.toFixed(2)}%
              </span>
            </div>
          </Card>
        </div>
        <div className="pt-5">
            <Card>
                <Graph data={data.full_graph} />
            </Card>
        </div>
      </div>
    </>
  )
}

// HydrateFallback is rendered while the client loader is running
export function HydrateFallback() {
  return <div>Loading...</div>;
}