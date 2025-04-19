import type { ReactNode } from "react";
import { useEffect, useRef, useState } from "react";
import "./Tooltip.css";

export default function Tooltip({ visible, content }: { visible: boolean; content: ReactNode }) {
    const tooltipRef = useRef<HTMLDivElement>(null);
    const [position, setPosition] = useState({ x: 0, y: 0 });

    useEffect(() => {
        if (!tooltipRef.current) return;

        const handleMouseMove = (event: MouseEvent) => {
            setPosition({ x: event.pageX, y: event.pageY });
        };
        window.addEventListener("mousemove", handleMouseMove);
        return () => {
            window.removeEventListener("mousemove", handleMouseMove);
        };
    }, [])

    return <div className="tooltip" ref={tooltipRef} style={{
        display: visible ? "block" : "none",
        left: position.x + 40,
        top: position.y,
    }}>
        { content }
    </div>
}