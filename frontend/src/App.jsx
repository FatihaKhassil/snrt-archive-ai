import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import Login from "./pages/Login/Login";

import Dashboard from "./pages/Dashboard/Dashboard";
import Users from "./pages/Users/Users";
import Documents from "./pages/Documents/Documents";
import Profile from "./pages/Profile/Profile";
import Upload from "./pages/Upload/Upload";
import Search from "./pages/Search/Search";
import SemanticSearch from "./pages/SemanticSearch/SemanticSearch";

import ProtectedRoute from "./routes/ProtectedRoute";


const protect = (page, roles) => (
    <ProtectedRoute allowedRoles={roles}>
        {page}
    </ProtectedRoute>
);


function App() {

    return (

        <BrowserRouter>

            <Routes>

                {/* ==========================
                    PUBLIC
                ========================== */}

                <Route
                    path="/"
                    element={<Login />}
                />


                {/* ==========================
                    DASHBOARD
                ========================== */}

                <Route
                    path="/dashboard"
                    element={protect(
                        <Dashboard />,
                        [
                            "ADMIN",
                            "DOCUMENTALIST",
                            "SNRT_USER"
                        ]
                    )}
                />


                {/* ==========================
                    USERS
                    ADMIN ONLY
                ========================== */}

                <Route
                    path="/users"
                    element={protect(
                        <Users />,
                        ["ADMIN"]
                    )}
                />


                {/* ==========================
                    DOCUMENTS
                ========================== */}

                <Route
                    path="/documents"
                    element={protect(
                        <Documents />,
                        [
                            "ADMIN",
                            "DOCUMENTALIST",
                            "SNRT_USER"
                        ]
                    )}
                />


                {/* ==========================
                    PROFILE
                ========================== */}

                <Route
                    path="/profile"
                    element={protect(
                        <Profile />,
                        [
                            "ADMIN",
                            "DOCUMENTALIST",
                            "SNRT_USER"
                        ]
                    )}
                />


                {/* ==========================
                    UPLOAD
                    ADMIN + DOCUMENTALIST
                ========================== */}

                <Route
                    path="/upload"
                    element={protect(
                        <Upload />,
                        [
                            "ADMIN",
                            "DOCUMENTALIST"
                        ]
                    )}
                />


                {/* ==========================
                    CLASSIC SEARCH
                ========================== */}

                <Route
                    path="/search"
                    element={protect(
                        <Search />,
                        [
                            "ADMIN",
                            "DOCUMENTALIST",
                            "SNRT_USER"
                        ]
                    )}
                />


                {/* ==========================
                    SEMANTIC SEARCH
                ========================== */}

                <Route
                    path="/semantic-search"
                    element={protect(
                        <SemanticSearch />,
                        [
                            "ADMIN",
                            "DOCUMENTALIST",
                            "SNRT_USER"
                        ]
                    )}
                />


                {/* ==========================
                    DEFAULT
                ========================== */}

                <Route
                    path="*"
                    element={
                        <Navigate
                            to="/dashboard"
                            replace
                        />
                    }
                />

            </Routes>

        </BrowserRouter>

    );
}


export default App;