import { Navigate } from "react-router-dom";

import { getToken, getRole } from "../utils/storage";

function ProtectedRoute({ children, allowedRoles = [] }) {

    const token = getToken();
    const role = getRole();

    if (!token) {

        return <Navigate to="/" replace />;

    }

    if (
        allowedRoles.length > 0 &&
        !allowedRoles.includes(role)
    ) {

        return <Navigate to="/dashboard" replace />;

    }

    return children;

}

export default ProtectedRoute;