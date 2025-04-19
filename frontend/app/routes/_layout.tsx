import { Outlet } from "react-router";

export default function Layout() {
    return (
        <div>
            <h1>layout test</h1>
            {/* add navbar */}
            <main>
                <Outlet />
            </main>
        </div>
    )
}