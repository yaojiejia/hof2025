import { useParams } from "react-router";
import Card from "./Components/Card";
import { useEffect, useState } from "react";

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
    nextDay: number;
    change: number;
    percentChange: number;
  };
  market_sentiment: number;
  
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
    const res = {
      name: data.company_name,
      id: data.ticker,
      currentPrice: Number(lastPrice), // Ensure this is a number
      pred: {
        nextDay: data.expected_next_day_price,
        change: data.prediction,
        percentChange: ((data.expected_next_day_price - data.latest_closing_price) / data.latest_closing_price) * 100,
      },
      market_sentiment: data.avg_sentiment,
    };
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
      <div className="flex ml-5">
        <div>
          <strong>{data.name}</strong> {data.id.toUpperCase()}
        </div>
      </div>
      <div>
        <div className="pt-6 flex justify-around gap-5">
          <Card className="w-60 h-20">
            <p className="text-sm">Current Price</p>
            <div>
              ${data.currentPrice?.toFixed(2)}
            </div>
          </Card>
          <Card className="w-60 h-20">
            <p className="text-sm">Predicted Price</p>
            <div>
              ${data.pred.nextDay?.toFixed(2)}
              <span className={data.pred.change > 0 ? "text-green-500" : "text-red-500"}>
                {data.pred.change > 0 ? " +" : " "}{data.pred.percentChange?.toFixed(2)}%
              </span>
            </div>
          </Card>
        </div>
        <div className="pt-5">
        </div>
      </div>
    </>
  )
}

// HydrateFallback is rendered while the client loader is running
export function HydrateFallback() {
  return <div>Loading...</div>;
}