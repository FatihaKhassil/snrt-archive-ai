import { useState } from "react";
import { useNavigate } from "react-router-dom";

import "./Login.css";

import hero from "../../assets/images/login-background.png";
import logo from "../../assets/logo/snrt-logo.png";

import AuthService from "../../services/authService";
import { saveSession } from "../../utils/storage";

import {
    Box,
    TextField,
    Button,
    Typography,
    Alert,
    CircularProgress,
    InputAdornment,
    IconButton
} from "@mui/material";

import EmailOutlinedIcon from "@mui/icons-material/EmailOutlined";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";
import FolderOpenOutlinedIcon from "@mui/icons-material/FolderOpenOutlined";
import SearchOutlinedIcon from "@mui/icons-material/SearchOutlined";
import PsychologyOutlinedIcon from "@mui/icons-material/PsychologyOutlined";

function Login() {

    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleLogin = async () => {

        try {

            setLoading(true);
            setError("");

            const response = await AuthService.login(
                email,
                password
            );

            saveSession(response);

            navigate("/dashboard");

        }

        catch (err) {

            console.error(err);

            setError(

                err.response?.data?.detail ||

                "Unable to login."

            );

        }

        finally {

            setLoading(false);

        }

    };

    const features = [
        {
            icon: <FolderOpenOutlinedIcon />,
            label: "Centralisez vos documents"
        },
        {
            icon: <SearchOutlinedIcon />,
            label: "Recherchez rapidement"
        },
        {
            icon: <PsychologyOutlinedIcon />,
            label: "Exploitez la puissance de l'IA"
        }
    ];

    return (

        <div className="login-container">

            <div className="login-left">

                <img
                    src={hero}
                    alt="SNRT Building"
                    className="hero-image"
                />

                <div className="hero-overlay" />

                <div className="hero-content">

                    <div className="brand-row">

                        <img
                            src={logo}
                            alt="SNRT Logo"
                            className="brand-logo"
                        />

                        <div>

                            <Typography className="brand-title">
                                SNRT
                            </Typography>

                            <Typography className="brand-subtitle">
                                ARCHIVE AI
                            </Typography>

                        </div>

                    </div>

                    <div className="brand-divider" />

                    <Typography className="hero-tagline">
                        Plateforme intelligente de gestion et de recherche
                        dans les archives audiovisuelles de la SNRT
                    </Typography>

                    <div className="feature-list">

                        {features.map((feature, index) => (

                            <div className="feature-item" key={index}>

                                <span className="feature-icon">
                                    {feature.icon}
                                </span>

                                <Typography className="feature-label">
                                    {feature.label}
                                </Typography>

                            </div>

                        ))}

                    </div>

                </div>

            </div>

            <div className="login-right">

                <Box className="login-card">

                    <div className="login-logo-circle">

                        <img
                            src={logo}
                            alt="SNRT Logo"
                            className="logo"
                        />

                    </div>

                    <Typography
                        variant="h4"
                        className="title"
                    >

                        Connexion

                    </Typography>

                    <Typography
                        className="subtitle"
                    >

                        Veuillez vous connecter pour accéder à votre espace

                    </Typography>

                    <Typography className="field-label">
                        Email
                    </Typography>

                    <TextField

                        fullWidth

                        placeholder="votre.email@snrt.ma"

                        value={email}

                        onChange={(e)=>setEmail(e.target.value)}

                        InputProps={{

                            startAdornment:(

                                <InputAdornment position="start">

                                    <EmailOutlinedIcon/>

                                </InputAdornment>

                            )

                        }}

                    />

                    <Typography className="field-label">
                        Mot de passe
                    </Typography>

                    <TextField

                        fullWidth

                        type={showPassword ? "text" : "password"}

                        placeholder="Votre mot de passe"

                        value={password}

                        onChange={(e)=>setPassword(e.target.value)}

                        InputProps={{

                            startAdornment:(

                                <InputAdornment position="start">

                                    <LockOutlinedIcon/>

                                </InputAdornment>

                            ),

                            endAdornment:(

                                <InputAdornment position="end">

                                    <IconButton

                                        onClick={() => setShowPassword(!showPassword)}

                                        edge="end"

                                    >

                                        {showPassword ? <VisibilityOff /> : <Visibility />}

                                    </IconButton>

                                </InputAdornment>

                            )

                        }}

                    />

                    <div className="forgot-password-row">

                        <a href="#" className="forgot-password-link">
                            Mot de passe oublié ?
                        </a>

                    </div>

                    {

                        error &&

                        <Alert

                            severity="error"

                            sx={{mt:2}}

                        >

                            {error}

                        </Alert>

                    }

                    <Button

                        fullWidth

                        variant="contained"

                        className="login-button"

                        disabled={loading}

                        onClick={handleLogin}

                        startIcon={!loading && <LockOutlinedIcon />}

                    >

                        {

                            loading ?

                            <CircularProgress

                                size={24}

                                sx={{color:"white"}}

                            />

                            :

                            "Se connecter"

                        }

                    </Button>

                </Box>

            </div>

        </div>

    );

}

export default Login;
