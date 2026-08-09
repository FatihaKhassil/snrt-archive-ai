import "./Layout.css";

import Sidebar from "../Sidebar/Sidebar";
import Header from "../Header/Header";

function Layout({ children }) {

    return (
        <div className="layout">

            <Sidebar />

            <div className="layout-content">

                <Header />

                <main className="page-content">
                    {children}
                </main>

            </div>

        </div>
    );
}

export default Layout;