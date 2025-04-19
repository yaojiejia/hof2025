import "./navbar.css";
import { useNavigate } from "react-router";
import { useState } from "react";

export default function Navbar() {
    const navigate = useNavigate();
    const [ ticker, setTicker ] = useState("");

    return <div className="navbar">
        <button className="navbar-button home-button" onClick={() => navigate("/")}>Home</button>
        
        <div>
            <input
                className="navbar-input"
                type="text"
                placeholder="Enter ticker"
                value={ticker}
                onChange={(e) => setTicker(e.target.value)}
            />
            <button className="navbar-button" onClick={() => navigate(`./${ticker}`)}>Go</button>
        </div>
    </div>
}