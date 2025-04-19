import type { Route } from "./+types/stock";
import { useParams } from "react-router";
import Card from "./Components/Card";
import Heatmap from "./Components/Heatmap";
import Graph from "./Components/Graph";
import { useEffect, useState } from "react";
import historical from "node_modules/yahoo-finance2/dist/esm/src/modules/historical";

export async function loader({ params }: Route.LoaderArgs) {
    const id = params.id
    try {
        const predictRes = await fetch(`http://3.145.78.241:5000/predict_ticker_price?ticker=${id}`)
        const data = await predictRes.json()
        console.log(data)
        
        const res = {
            name: data.company_name,
            id: data.ticker,
            price: data.latest_closing_price,
            pred: {
                nextDay: data.expected_next_day_price,
                change: data.prediction,
                percentChange: ((data.expected_next_day_price - data.latest_closing_price) / data.latest_closing_price) * 100,
            },
            market_sentiment: data.avg_sentiment,
            graph: {
                historical_data: Object.entries(data.last_4_days_closing).map(([date, price]) => ({
                    x: date,
                    y: price,
                })),
                predicted_data: [{ x: "Next Day", y: data.expected_next_day_price }],
            },
        };
        
        console.log(res)
        return res
    } catch (error) {
        console.error(error)
    }
}



export default function Stock({ loaderData }: Route.ComponentProps) {
    const data = loaderData;
    
    return (
        <>
        <div className="flex ml-50">
            <div>
                <strong>{data.name}</strong> {data.id.toUpperCase()}
            </div>
            <div className="bg">

            </div>
        </div>
        <div>
            <div className="pt-25 flex justify-around gap-50">
                <Card className="w-60 h-20">
                    <p className="text-sm">Current Price</p>
                    <div>
                        WHY
                        {data.currentPrice}
                    </div>
                </Card>
                <Card className="w-60 h-20">
                    a
                </Card>
            </div>
            <div className="pt-20">
                <Card className="">
                    <Graph></Graph>
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