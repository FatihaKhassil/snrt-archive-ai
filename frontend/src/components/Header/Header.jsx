import { useState } from "react";
import { useNavigate } from "react-router-dom";

import "./Header.css";

import SearchRoundedIcon from "@mui/icons-material/SearchRounded";
import CalendarTodayRoundedIcon from "@mui/icons-material/CalendarTodayRounded";
import KeyboardArrowDownRoundedIcon from "@mui/icons-material/KeyboardArrowDownRounded";
import PersonOutlineRoundedIcon from "@mui/icons-material/PersonOutlineRounded";
import LockResetRoundedIcon from "@mui/icons-material/LockResetRounded";
import LogoutRoundedIcon from "@mui/icons-material/LogoutRounded";

import { clearSession, getProfile } from "../../utils/storage";

function Header() {
    const [open, setOpen] = useState(false);
    const navigate = useNavigate();

    const profile = getProfile();

    const firstName = profile?.first_name || "Utilisateur";
    const role = profile?.role;

    let headerTitle = "Utilisateur";
    let roleLabel = "Utilisateur";

    if (role === "ADMIN") {
        headerTitle = "Administration";
        roleLabel = "Administrateur";
    } else if (role === "DOCUMENTALIST") {
        headerTitle = "Espace documentaliste";
        roleLabel = "Documentaliste";
    } else if (role === "SNRT_USER") {
        headerTitle = "Utilisateur";
        roleLabel = "Utilisateur";
    }

    const logout = () => {
        clearSession();
        navigate("/", { replace: true });
    };

    const openProfile = () => {
        setOpen(false);
        navigate("/profile");
    };

    const openPassword = () => {
        setOpen(false);
        navigate("/profile#security");
    };

    return (
        <header className="header">

            <div className="header-left">
                <h2>{headerTitle}</h2>
                <p>SNRT Smart Archive</p>
            </div>

            <div className="header-right">

                <label className="search-box">
                    <SearchRoundedIcon />

                    <input
                        type="search"
                        placeholder="Rechercher..."
                        aria-label="Rechercher"
                    />
                </label>

                <div className="date-box">
                    <CalendarTodayRoundedIcon />

                    <span>
                        {new Intl.DateTimeFormat("fr-FR").format(
                            new Date()
                        )}
                    </span>
                </div>

                <div className="profile-menu">

                    <button
                        className="profile"
                        type="button"
                        onClick={() => setOpen(!open)}
                        aria-haspopup="menu"
                        aria-expanded={open}
                    >

                        <div className="profile-avatar">
                            {firstName
                                .slice(0, 1)
                                .toUpperCase()}
                        </div>

                        <div>
                            <h4>{firstName}</h4>
                            <span>{roleLabel}</span>
                        </div>

                        <KeyboardArrowDownRoundedIcon />

                    </button>

                    {open && (
                        <div
                            className="profile-dropdown"
                            role="menu"
                        >

                            <button
                                type="button"
                                onClick={openProfile}
                            >
                                <PersonOutlineRoundedIcon />
                                Mon profil
                            </button>

                            <button
                                type="button"
                                onClick={openPassword}
                            >
                                <LockResetRoundedIcon />
                                Changer le mot de passe
                            </button>

                            <span className="dropdown-separator" />

                            <button
                                type="button"
                                className="dropdown-logout"
                                onClick={logout}
                            >
                                <LogoutRoundedIcon />
                                Déconnexion
                            </button>

                        </div>
                    )}

                </div>

            </div>

        </header>
    );
}

export default Header;