export default function Card({ 
        children,
        className = "", 
    }: { 
        children: React.ReactNode,
        className?: string;
     }) {
    return (
        <div className={`bg-gray-800 p-4 rounded-lg w-11/12 ${className}`}>
            {children}
        </div>
    );
}