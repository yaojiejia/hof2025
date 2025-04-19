/*
File for providing hardcoded data for home.tsx
*/

export const homeData = {
    marketSummary: [
        {
            name: "Market State",
            value: "Bullish"
        },
        {
            name: "Top Gaining Sector",
            value: "Healthcare"
        },
        {
            name: "Top Losing Sector",
            value: "Technology"
        },
        {
            name: "Top Gaining Stock",
            value: "Netflix"
        },
        {
            name: "Top Losing Stock",
            value: "NVIDIA"
        }
    ],
    heatmap: {
        categories: [
            "Technology",
            "Healthcare",
            "Finance",
            "Energy",
            "Consumer Goods",
            "Utilities",
            "Telecommunications",
            "Real Estate"
        ],
        stocks: [
            {
                name: "GOOGL",
                change: -1.35
            },
            {
                name: "AMAZON",
                change: 3.15
            },
            {
                name: "NETFLIX",
                change: -1.85
            }
        ]
    },
    predictions: {
        predictedValue: 533.4,
        currentValue: 522.6,
        history: [
            {
                date: "2023-10-01",
                value: 500.0
            },
            {
                date: "2023-10-02",
                value: 505.0
            },
            {
                date: "2023-10-03",
                value: 510.0
            },
            {
                date: "2023-10-04",
                value: 515.0
            },
            {
                date: "2023-10-05",
                value: 520.0
            },
            {
                date: "2023-10-06",
                value: 522.6
            }
        ]
    }
}