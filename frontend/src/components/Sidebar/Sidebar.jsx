import { NavLink, useNavigate } from "react-router-dom";

import "./Sidebar.css";

import logo from "../../assets/logo/snrt-logo.png";

import DashboardRoundedIcon from "@mui/icons-material/DashboardRounded";
import PeopleRoundedIcon from "@mui/icons-material/PeopleRounded";
import DescriptionRoundedIcon from "@mui/icons-material/DescriptionRounded";
import UploadFileRoundedIcon from "@mui/icons-material/UploadFileRounded";
import ManageSearchRoundedIcon from "@mui/icons-material/ManageSearchRounded";
import PersonOutlineRoundedIcon from "@mui/icons-material/PersonOutlineRounded";
import LogoutRoundedIcon from "@mui/icons-material/LogoutRounded";

import {
    clearSession,
    getProfile
} from "../../utils/storage";


function Sidebar() {

    const navigate = useNavigate();

    const profile = getProfile();

    const firstName =
        profile?.first_name || "Utilisateur";

    const role =
        profile?.role;

    let menu = [];

    let roleLabel =
        "Utilisateur";


    // =========================
    // ADMINISTRATEUR
    // =========================

    switch (role) {

        case "ADMIN":

            roleLabel = "Administrateur";

            menu = [

                {
                    title: "Dashboard",
                    to: "/dashboard",
                    icon: <DashboardRoundedIcon />
                },

                {
                    title: "Utilisateurs",
                    to: "/users",
                    icon: <PeopleRoundedIcon />
                },

                {
                    title: "Documents",
                    to: "/documents",
                    icon: <DescriptionRoundedIcon />
                },

                {
                    title: "Mon profil",
                    to: "/profile",
                    icon: <PersonOutlineRoundedIcon />
                }

            ];

            break;


        // =========================
        // DOCUMENTALISTE
        // =========================

        case "DOCUMENTALIST":

            roleLabel = "Documentaliste";

            menu = [

                {
                    title: "Dashboard",
                    to: "/dashboard",
                    icon: <DashboardRoundedIcon />
                },

                {
                    title: "Documents",
                    to: "/documents",
                    icon: <DescriptionRoundedIcon />
                },

                {
                    title: "Importer",
                    to: "/upload",
                    icon: <UploadFileRoundedIcon />
                },

                {
                    title: "Recherche",
                    to: "/search",
                    icon: <ManageSearchRoundedIcon />
                },

                {
                    title: "Recherche sémantique",
                    to: "/semantic-search",
                    icon: <ManageSearchRoundedIcon />
                },

                {
                    title: "Mon profil",
                    to: "/profile",
                    icon: <PersonOutlineRoundedIcon />
                }

            ];

            break;


        // =========================
        // UTILISATEUR STANDARD
        // =========================

        case "SNRT_USER":

            roleLabel = "Utilisateur";

            menu = [

                {
                    title: "Dashboard",
                    to: "/dashboard",
                    icon: <DashboardRoundedIcon />
                },

                {
                    title: "Documents",
                    to: "/documents",
                    icon: <DescriptionRoundedIcon />
                },

                {
                    title: "Recherche",
                    to: "/search",
                    icon: <ManageSearchRoundedIcon />
                },

                {
                    title: "Recherche sémantique",
                    to: "/semantic-search",
                    icon: <ManageSearchRoundedIcon />
                },

                {
                    title: "Mon profil",
                    to: "/profile",
                    icon: <PersonOutlineRoundedIcon />
                }

            ];

            break;


        // =========================
        // ROLE INCONNU
        // =========================

        default:

            roleLabel = "Utilisateur";

            menu = [];

            break;
    }


    // =========================
    // LOGOUT
    // =========================

    const logout = () => {

        clearSession();

        navigate("/", {
            replace: true
        });

    };


    return (

        <aside className="sidebar">


            {/* =========================
                LOGO
            ========================= */}

            <div className="sidebar-logo">

                <img
                    src={logo}
                    alt="SNRT"
                />

                <div>

                    <h2>
                        SNRT
                    </h2>

                    <span>
                        SMART ARCHIVE
                    </span>

                </div>

            </div>


            {/* =========================
                MENU
            ========================= */}

            <nav className="sidebar-menu">

                {menu.map((item) => (

                    <NavLink
                        key={item.to}
                        to={item.to}
                        className={({ isActive }) =>
                            `sidebar-item${isActive ? " active" : ""}`
                        }
                    >

                        {item.icon}

                        <span>
                            {item.title}
                        </span>

                    </NavLink>

                ))}

            </nav>


            {/* =========================
                FOOTER
            ========================= */}

            <div className="sidebar-footer">


                {/* USER */}

                <div className="sidebar-user">

                    <div className="avatar">

                        {firstName
                            .charAt(0)
                            .toUpperCase()
                        }

                    </div>


                    <div className="sidebar-user-info">

                        <strong>
                            {firstName}
                        </strong>

                        <span>
                            {roleLabel}
                        </span>

                    </div>

                </div>


                {/* LOGOUT */}

                <button
                    type="button"
                    className="logout-button"
                    onClick={logout}
                >

                    <LogoutRoundedIcon />

                    <span>
                        Déconnexion
                    </span>

                </button>

            </div>

        </aside>
    );
}


export default Sidebar;