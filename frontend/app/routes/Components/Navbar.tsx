import "./Navbar.css";
import { useNavigate } from "react-router";
import { useState } from "react";
import { MagnifyingGlassIcon } from '@heroicons/react/24/solid';

export default function Navbar() {
    const navigate = useNavigate();
    const [ ticker, setTicker ] = useState("");

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        if (ticker.trim()) {
            const url = new URL(`/stock/${ticker.trim().toLowerCase()}`, window.location.origin);
            navigate(url.pathname)
        }
    }

    return (
        <div className="navbar">
            <button className="navbar-button home-button hover:bg-[#2c2c2c]" onClick={() => navigate("/")}>Home</button>
            
            <form action="" onSubmit={handleSubmit}>
                <div className="relative">
                    <input
                        className="navbar-input"
                        type="text"
                        placeholder="Enter ticker"
                        value={ticker}
                        onChange={(e) => setTicker(e.target.value)}
                    />
                    <MagnifyingGlassIcon className="absolute right-2 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-500" />
                </div>
            </form>
        </div>
    )
}