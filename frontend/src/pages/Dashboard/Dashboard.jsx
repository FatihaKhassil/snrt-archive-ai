import { useEffect, useState } from "react";
import "./Dashboard.css";

import Layout from "../../components/Layout/Layout";

import DashboardService from "../../services/dashboardService";
import DocumentsService from "../../services/documentsService";

import { getRole } from "../../utils/storage";

import PeopleRoundedIcon from "@mui/icons-material/PeopleRounded";
import DescriptionRoundedIcon from "@mui/icons-material/DescriptionRounded";
import MicRoundedIcon from "@mui/icons-material/MicRounded";
import SearchRoundedIcon from "@mui/icons-material/SearchRounded";
import UploadFileRoundedIcon from "@mui/icons-material/UploadFileRounded";
import CheckCircleRoundedIcon from "@mui/icons-material/CheckCircleRounded";
import ScheduleRoundedIcon from "@mui/icons-material/ScheduleRounded";
import ErrorRoundedIcon from "@mui/icons-material/ErrorRounded";
import SmartToyRoundedIcon from "@mui/icons-material/SmartToyRounded";
import TrendingUpRoundedIcon from "@mui/icons-material/TrendingUpRounded";
import FolderRoundedIcon from "@mui/icons-material/FolderRounded";
import ArticleRoundedIcon from "@mui/icons-material/ArticleRounded";


/* =========================================================
   COMPOSANT CARTE STATISTIQUE
========================================================= */

function DashboardStatCard({
    title,
    value,
    subtitle,
    icon,
    variant = "blue"
}) {

    return (

        <div className={`dashboard-stat-card ${variant}`}>

            <div className="dashboard-stat-top">

                <div className="dashboard-stat-icon">
                    {icon}
                </div>

                <div className="dashboard-stat-content">

                    <span className="dashboard-stat-title">
                        {title}
                    </span>

                    <strong className="dashboard-stat-value">
                        {value}
                    </strong>

                    <span className="dashboard-stat-subtitle">
                        {subtitle}
                    </span>

                </div>

            </div>

        </div>

    );

}


/* =========================================================
   PETITE LIGNE DE STATISTIQUE
========================================================= */

function DashboardInfoRow({
    icon,
    label,
    value,
    variant = ""
}) {

    return (

        <div className="dashboard-info-row">

            <div className="dashboard-info-left">

                <div className={`dashboard-info-icon ${variant}`}>
                    {icon}
                </div>

                <span>
                    {label}
                </span>

            </div>

            <strong>
                {value}
            </strong>

        </div>

    );

}


/* =========================================================
   HEADER INTERNE
========================================================= */

function DashboardIntro({
    eyebrow,
    title,
    description
}) {

    return (

        <div className="dashboard-intro">

            <div>

                <span className="dashboard-eyebrow">
                    {eyebrow}
                </span>

                <h1>
                    {title}
                </h1>

                <p>
                    {description}
                </p>

            </div>

        </div>

    );

}


/* =========================================================
   DASHBOARD DOCUMENTALISTE
========================================================= */

function DocumentalistDashboard() {

    const [documents, setDocuments] = useState(null);
    const [error, setError] = useState("");


    useEffect(() => {

        const fetchDocuments = async () => {

            try {

                const response =
                    await DocumentsService.getAll();

                console.log(
                    "DOCUMENTALIST /documents :",
                    response
                );

                if (Array.isArray(response)) {

                    setDocuments(response);

                } else if (
                    Array.isArray(response?.documents)
                ) {

                    setDocuments(response.documents);

                } else {

                    setDocuments([]);

                }

            } catch (err) {

                console.error(
                    "Erreur documents :",
                    err
                );

                setError(
                    err.response?.data?.detail ||
                    "Impossible de charger les documents."
                );

                setDocuments([]);

            }

        };

        fetchDocuments();

    }, []);


    if (!documents) {

        return (

            <Layout>

                <div className="dashboard-loading-page">

                    <div className="loading-spinner"></div>

                    <span>
                        Chargement du tableau de bord...
                    </span>

                </div>

            </Layout>

        );

    }


    const count = (predicate) =>
        documents.filter(predicate).length;


    const total = documents.length;

    const audio = count(
        (document) =>
            document.file_type === "audio"
    );

    const indexed = count(
        (document) =>
            document.status === "INDEXED"
    );

    const uploaded = count(
        (document) =>
            document.status === "UPLOADED"
    );

    const processing = count(
        (document) =>
            document.status === "PROCESSING"
    );

    const failed = count(
        (document) =>
            document.status === "FAILED"
    );


    return (

        <Layout>

            <div className="dashboard">

                <DashboardIntro
                    eyebrow="ESPACE DOCUMENTALISTE"
                    title="Vue d’ensemble"
                    description="Suivez l’état de vos archives et du traitement documentaire."
                />


                {error && (

                    <div className="dashboard-error">
                        <ErrorRoundedIcon />

                        <span>
                            {error}
                        </span>
                    </div>

                )}


                {/* =========================
                    STATISTIQUES
                ========================= */}

                <div className="stats-grid">

                    <DashboardStatCard
                        title="Documents"
                        value={total}
                        subtitle="Total des archives"
                        variant="red"
                        icon={<DescriptionRoundedIcon />}
                    />

                    <DashboardStatCard
                        title="Fichiers audio"
                        value={audio}
                        subtitle="Archives audio"
                        variant="blue"
                        icon={<MicRoundedIcon />}
                    />

                    <DashboardStatCard
                        title="Documents indexés"
                        value={indexed}
                        subtitle="Prêts pour la recherche"
                        variant="green"
                        icon={<SearchRoundedIcon />}
                    />

                    <DashboardStatCard
                        title="Documents importés"
                        value={uploaded}
                        subtitle="En attente de traitement"
                        variant="orange"
                        icon={<UploadFileRoundedIcon />}
                    />

                </div>


                {/* =========================
                    BLOCS INFÉRIEURS
                ========================= */}

                <div className="dashboard-row">

                    <div className="dashboard-panel">

                        <div className="dashboard-panel-header">

                            <div>

                                <span className="panel-eyebrow">
                                    SUIVI
                                </span>

                                <h2>
                                    État des documents
                                </h2>

                            </div>

                            <div className="panel-header-icon red">
                                <FolderRoundedIcon />
                            </div>

                        </div>


                        <div className="dashboard-info-list">

                            <DashboardInfoRow
                                icon={<UploadFileRoundedIcon />}
                                label="Documents importés"
                                value={uploaded}
                                variant="orange"
                            />

                            <DashboardInfoRow
                                icon={<ScheduleRoundedIcon />}
                                label="En cours de traitement"
                                value={processing}
                                variant="blue"
                            />

                            <DashboardInfoRow
                                icon={<CheckCircleRoundedIcon />}
                                label="Documents indexés"
                                value={indexed}
                                variant="green"
                            />

                            <DashboardInfoRow
                                icon={<ErrorRoundedIcon />}
                                label="Documents en échec"
                                value={failed}
                                variant="red"
                            />

                        </div>

                    </div>


                    <div className="dashboard-panel">

                        <div className="dashboard-panel-header">

                            <div>

                                <span className="panel-eyebrow">
                                    ARCHIVES
                                </span>

                                <h2>
                                    Gestion des archives
                                </h2>

                            </div>

                            <div className="panel-header-icon blue">
                                <DescriptionRoundedIcon />
                            </div>

                        </div>


                        <div className="dashboard-guidance">

                            <div className="guidance-main-icon">
                                <FolderRoundedIcon />
                            </div>

                            <div>

                                <h3>
                                    Vos archives sont centralisées
                                </h3>

                                <p>
                                    Consultez les documents depuis
                                    le menu <strong>Documents</strong>.
                                    Vous pouvez suivre leur état de
                                    traitement et leur disponibilité
                                    pour la recherche.
                                </p>

                                <div className="guidance-badge">
                                    <CheckCircleRoundedIcon />

                                    <span>
                                        Système opérationnel
                                    </span>

                                </div>

                            </div>

                        </div>

                    </div>

                </div>

            </div>

        </Layout>

    );

}


/* =========================================================
   DASHBOARD ADMINISTRATEUR
========================================================= */

function AdminDashboard() {

    const [stats, setStats] = useState(null);
    const [error, setError] = useState("");


    useEffect(() => {

        const fetchStatistics = async () => {

            try {

                const response =
                    await DashboardService.getStatistics();

                setStats(response);

            } catch (err) {

                console.error(err);

                setError(
                    err.response?.data?.detail ||
                    "Impossible de charger les statistiques."
                );

            }

        };

        fetchStatistics();

    }, []);


    if (!stats) {

        return (

            <Layout>

                <div className="dashboard-loading-page">

                    {error ? (

                        <div className="dashboard-error">
                            <ErrorRoundedIcon />
                            <span>{error}</span>
                        </div>

                    ) : (

                        <>
                            <div className="loading-spinner"></div>

                            <span>
                                Chargement des statistiques...
                            </span>
                        </>

                    )}

                </div>

            </Layout>

        );

    }


    return (

        <Layout>

            <div className="dashboard">

                <DashboardIntro
                    eyebrow="ADMINISTRATION"
                    title="Vue d’ensemble"
                    description="Supervisez les utilisateurs, les archives et les traitements intelligents."
                />


                {/* =========================
                    STATISTIQUES PRINCIPALES
                ========================= */}

                <div className="stats-grid">

                    <DashboardStatCard
                        title="Utilisateurs"
                        value={stats.users.total}
                        subtitle={`${stats.users.active} utilisateurs actifs`}
                        variant="blue"
                        icon={<PeopleRoundedIcon />}
                    />

                    <DashboardStatCard
                        title="Documents"
                        value={stats.documents.total}
                        subtitle={`${stats.documents.audio} documents audio`}
                        variant="red"
                        icon={<DescriptionRoundedIcon />}
                    />

                    <DashboardStatCard
                        title="Transcriptions"
                        value={stats.processing.transcribed}
                        subtitle="Documents transcrits"
                        variant="green"
                        icon={<MicRoundedIcon />}
                    />

                    <DashboardStatCard
                        title="Documents indexés"
                        value={stats.processing.indexed}
                        subtitle="Prêts pour la recherche"
                        variant="orange"
                        icon={<SearchRoundedIcon />}
                    />

                </div>


                {/* =========================
                    STATISTIQUES SECONDAIRES
                ========================= */}

                <div className="dashboard-row">

                    <div className="dashboard-panel">

                        <div className="dashboard-panel-header">

                            <div>

                                <span className="panel-eyebrow">
                                    UTILISATEURS
                                </span>

                                <h2>
                                    Statistiques des utilisateurs
                                </h2>

                            </div>

                            <div className="panel-header-icon blue">
                                <PeopleRoundedIcon />
                            </div>

                        </div>


                        <div className="dashboard-info-list">

                            <DashboardInfoRow
                                icon={<PeopleRoundedIcon />}
                                label="Total utilisateurs"
                                value={stats.users.total}
                                variant="blue"
                            />

                            <DashboardInfoRow
                                icon={<PeopleRoundedIcon />}
                                label="Administrateurs"
                                value={stats.users.admins}
                                variant="red"
                            />

                            <DashboardInfoRow
                                icon={<DescriptionRoundedIcon />}
                                label="Documentalistes"
                                value={stats.users.documentalists}
                                variant="orange"
                            />

                            <DashboardInfoRow
                                icon={<PeopleRoundedIcon />}
                                label="Utilisateurs standards"
                                value={stats.users.standard_users}
                                variant="green"
                            />

                        </div>

                    </div>


                    <div className="dashboard-panel">

                        <div className="dashboard-panel-header">

                            <div>

                                <span className="panel-eyebrow">
                                    INTELLIGENCE ARTIFICIELLE
                                </span>

                                <h2>
                                    Traitement IA
                                </h2>

                            </div>

                            <div className="panel-header-icon purple">
                                <SmartToyRoundedIcon />
                            </div>

                        </div>


                        <div className="dashboard-info-list">

                            <DashboardInfoRow
                                icon={<MicRoundedIcon />}
                                label="Transcriptions"
                                value={stats.processing.transcribed}
                                variant="green"
                            />

                            <DashboardInfoRow
                                icon={<ArticleRoundedIcon />}
                                label="Résumés"
                                value={stats.processing.summarized}
                                variant="blue"
                            />

                            <DashboardInfoRow
                                icon={<TrendingUpRoundedIcon />}
                                label="Mots-clés"
                                value={stats.processing.keywords}
                                variant="orange"
                            />

                            <DashboardInfoRow
                                icon={<SearchRoundedIcon />}
                                label="Documents indexés"
                                value={stats.processing.indexed}
                                variant="red"
                            />

                        </div>

                    </div>

                </div>


                {/* =========================
                    BANDEAU IA
                ========================= */}

                <div className="dashboard-ai-banner">

                    <div className="ai-banner-icon">
                        <SmartToyRoundedIcon />
                    </div>

                    <div>

                        <span>
                            SNRT SMART ARCHIVE
                        </span>

                        <h3>
                            Traitement intelligent des archives
                        </h3>

                        <p>
                            Transcription, résumé, extraction de mots-clés
                            et indexation sont intégrés dans votre chaîne
                            de traitement documentaire.
                        </p>

                    </div>

                </div>

            </div>

        </Layout>

    );

}


/* =========================================================
   DASHBOARD UTILISATEUR
========================================================= */

function UserDashboard() {

    const [documents, setDocuments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");


    useEffect(() => {

        const loadDocuments = async () => {

            try {

                const response =
                    await DocumentsService.getAll();

                console.log(
                    "USER /documents :",
                    response
                );


                if (Array.isArray(response)) {

                    setDocuments(response);

                } else if (
                    Array.isArray(response?.documents)
                ) {

                    setDocuments(response.documents);

                } else {

                    setDocuments([]);

                }

            } catch (err) {

                console.error(
                    "Erreur USER /documents :",
                    err
                );

                console.error(
                    "Status :",
                    err.response?.status
                );

                console.error(
                    "Data :",
                    err.response?.data
                );

                setError(
                    err.response?.data?.detail ||
                    "Impossible de charger les documents."
                );

                setDocuments([]);

            } finally {

                setLoading(false);

            }

        };

        loadDocuments();

    }, []);


    if (loading) {

        return (

            <Layout>

                <div className="dashboard-loading-page">

                    <div className="loading-spinner"></div>

                    <span>
                        Chargement de vos archives...
                    </span>

                </div>

            </Layout>

        );

    }


    const total = documents.length;


    const audio = documents.filter(
        (document) =>
            document.file_type === "audio"
    ).length;


    const pdf = documents.filter(
        (document) =>
            document.file_type === "document" ||
            document.file_type === "pdf"
    ).length;


    const indexed = documents.filter(
        (document) =>
            document.status === "INDEXED"
    ).length;


    return (

        <Layout>

            <div className="dashboard">

                <DashboardIntro
                    eyebrow="ESPACE UTILISATEUR"
                    title="Bienvenue sur SNRT Smart Archive"
                    description="Accédez rapidement aux archives et utilisez la recherche intelligente."
                />


                {error && (

                    <div className="dashboard-error">

                        <ErrorRoundedIcon />

                        <span>
                            {error}
                        </span>

                    </div>

                )}


                <div className="stats-grid">

                    <DashboardStatCard
                        title="Documents"
                        value={total}
                        subtitle="Documents disponibles"
                        variant="blue"
                        icon={<DescriptionRoundedIcon />}
                    />

                    <DashboardStatCard
                        title="Archives audio"
                        value={audio}
                        subtitle="Fichiers audio"
                        variant="green"
                        icon={<MicRoundedIcon />}
                    />

                    <DashboardStatCard
                        title="Documents PDF"
                        value={pdf}
                        subtitle="Documents disponibles"
                        variant="red"
                        icon={<ArticleRoundedIcon />}
                    />

                    <DashboardStatCard
                        title="Recherche"
                        value="Active"
                        subtitle="Recherche intelligente"
                        variant="orange"
                        icon={<SearchRoundedIcon />}
                    />

                </div>


                <div className="dashboard-row">

                    <div className="dashboard-panel">

                        <div className="dashboard-panel-header">

                            <div>

                                <span className="panel-eyebrow">
                                    RECHERCHE
                                </span>

                                <h2>
                                    Recherche intelligente
                                </h2>

                            </div>

                            <div className="panel-header-icon orange">
                                <SearchRoundedIcon />
                            </div>

                        </div>


                        <div className="dashboard-guidance">

                            <div className="guidance-main-icon orange">
                                <SearchRoundedIcon />
                            </div>

                            <div>

                                <h3>
                                    Retrouvez rapidement vos archives
                                </h3>

                                <p>
                                    Utilisez la recherche classique ou
                                    la recherche sémantique pour retrouver
                                    les contenus pertinents dans les
                                    archives SNRT.
                                </p>

                                <div className="guidance-badge">
                                    <CheckCircleRoundedIcon />

                                    <span>
                                        Recherche disponible
                                    </span>

                                </div>

                            </div>

                        </div>

                    </div>


                    <div className="dashboard-panel">

                        <div className="dashboard-panel-header">

                            <div>

                                <span className="panel-eyebrow">
                                    ARCHIVES
                                </span>

                                <h2>
                                    État de vos documents
                                </h2>

                            </div>

                            <div className="panel-header-icon green">
                                <FolderRoundedIcon />
                            </div>

                        </div>


                        <div className="dashboard-info-list">

                            <DashboardInfoRow
                                icon={<DescriptionRoundedIcon />}
                                label="Documents disponibles"
                                value={total}
                                variant="blue"
                            />

                            <DashboardInfoRow
                                icon={<MicRoundedIcon />}
                                label="Archives audio"
                                value={audio}
                                variant="green"
                            />

                            <DashboardInfoRow
                                icon={<ArticleRoundedIcon />}
                                label="Documents PDF"
                                value={pdf}
                                variant="red"
                            />

                            <DashboardInfoRow
                                icon={<CheckCircleRoundedIcon />}
                                label="Documents indexés"
                                value={indexed}
                                variant="orange"
                            />

                        </div>

                    </div>

                </div>

            </div>

        </Layout>

    );

}


/* =========================================================
   DASHBOARD PRINCIPAL
========================================================= */

function Dashboard() {

    const role = getRole();

    console.log(
        "ROLE ACTUEL :",
        role
    );


    if (role === "ADMIN") {

        return <AdminDashboard />;

    }


    if (role === "DOCUMENTALIST") {

        return <DocumentalistDashboard />;

    }


    if (role === "SNRT_USER") {

        return <UserDashboard />;

    }


    return (

        <Layout>

            <div className="dashboard">

                <div className="dashboard-access-denied">

                    <ErrorRoundedIcon />

                    <h2>
                        Accès refusé
                    </h2>

                    <p>
                        Rôle détecté :
                        {" "}
                        <strong>
                            {role || "Aucun rôle"}
                        </strong>
                    </p>

                </div>

            </div>

        </Layout>

    );

}


export default Dashboard;