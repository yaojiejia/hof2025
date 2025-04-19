import "./Card.css";

export default function Card({ children }: { children: React.ReactNode }) {
    return (
        <div className="card">
            {children}
        </div>
    );
}