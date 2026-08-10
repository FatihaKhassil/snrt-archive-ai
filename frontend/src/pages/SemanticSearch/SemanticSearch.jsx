import { useState } from "react";

import Layout from "../../components/Layout/Layout";

import {
    ErrorNotice,
    LoadingState,
    PageHeader
} from "../../components/AdminUI/AdminUI";

import RagService from "../../services/ragService";

import SearchRoundedIcon from "@mui/icons-material/SearchRounded";
import AutoAwesomeRoundedIcon from "@mui/icons-material/AutoAwesomeRounded";
import DescriptionOutlinedIcon from "@mui/icons-material/DescriptionOutlined";
import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";
import KeyboardArrowDownRoundedIcon from "@mui/icons-material/KeyboardArrowDownRounded";
import KeyboardArrowUpRoundedIcon from "@mui/icons-material/KeyboardArrowUpRounded";
import AudiotrackRoundedIcon from "@mui/icons-material/AudiotrackRounded";
import SourceRoundedIcon from "@mui/icons-material/SourceRounded";

import "./SemanticSearch.css";


function SemanticSearch() {

    const [question, setQuestion] = useState("");
    const [result, setResult] = useState(null);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const [openSources, setOpenSources] = useState({});


    const submit = async (event) => {

        event.preventDefault();

        const value = question.trim();

        if (!value) {
            return;
        }

        try {

            setLoading(true);
            setError("");
            setResult(null);
            setOpenSources({});

            const response = await RagService.ask(value);

            setResult(response);

        } catch (err) {

            console.error(err);

            setError(
                err.response?.data?.detail ||
                "La recherche sémantique est momentanément indisponible."
            );

        } finally {

            setLoading(false);

        }
    };


    const toggleSource = (index) => {

        setOpenSources((previous) => ({
            ...previous,
            [index]: !previous[index]
        }));

    };


    const sources = result?.sources || [];


    return (

        <Layout>

            <main className="semantic-search-page">

                <PageHeader
                    title="Recherche sémantique"
                    description="Posez une question en langage naturel et retrouvez les informations pertinentes dans les archives SNRT."
                />


                {/* =========================
                    SEARCH PANEL
                ========================= */}

                <section className="semantic-search-panel">

                    <div className="semantic-search-intro">

                        <div className="semantic-search-icon">
                            <AutoAwesomeRoundedIcon />
                        </div>

                        <div>

                            <h2>
                                Recherche intelligente
                            </h2>

                            <p>
                                Posez directement votre question.
                                Le système recherche les passages
                                pertinents dans les archives.
                            </p>

                        </div>

                    </div>


                    <form
                        className="semantic-search-form"
                        onSubmit={submit}
                    >

                        <div className="semantic-input-wrapper">

                            <SearchRoundedIcon />

                            <input
                                type="text"
                                value={question}
                                onChange={(event) =>
                                    setQuestion(event.target.value)
                                }
                                placeholder="Posez votre question sur les archives..."
                                aria-label="Question de recherche sémantique"
                                dir="auto"
                            />

                        </div>


                        <button
                            type="submit"
                            className="button button-primary semantic-search-button"
                            disabled={!question.trim() || loading}
                        >

                            <SearchRoundedIcon />

                            {loading
                                ? "Recherche..."
                                : "Rechercher"
                            }

                        </button>

                    </form>

                </section>


                <ErrorNotice message={error} />


                {/* =========================
                    LOADING
                ========================= */}

                {loading && (

                    <section className="semantic-result-panel">

                        <LoadingState />

                    </section>

                )}


                {/* =========================
                    RESULT
                ========================= */}

                {result && !loading && (

                    <section className="semantic-result-panel">


                        {/* RESULT HEADER */}

                        <div className="semantic-result-header">

                            <div>

                                <span className="result-label">
                                    RÉPONSE DE L'ARCHIVE
                                </span>

                                <h2>
                                    Résultat de la recherche
                                </h2>

                            </div>


                            <div className="chunks-badge">

                                <SourceRoundedIcon />

                                {sources.length || result.chunks || 0}

                                <span>
                                    sources analysées
                                </span>

                            </div>

                        </div>


                        {/* =========================
                            ANSWER
                        ========================= */}

                        <div className="semantic-answer">

                            <div className="answer-icon">

                                <AutoAwesomeRoundedIcon />

                            </div>

                            <div className="answer-content">

                                <h3>
                                    Réponse
                                </h3>

                                <p dir="auto">
                                    {result.answer}
                                </p>

                            </div>

                        </div>


                        {/* =========================
                            SOURCES
                        ========================= */}

                        <div className="semantic-sources">


                            <div className="sources-header">

                                <div>

                                    <h3>
                                        Documents utilisés
                                    </h3>

                                    <p>
                                        Documents ayant contribué à la réponse.
                                    </p>

                                </div>


                                <div className="sources-count">

                                    <DescriptionOutlinedIcon />

                                    {sources.length}

                                    <span>
                                        document{sources.length !== 1 ? "s" : ""}
                                    </span>

                                </div>

                            </div>


                            {sources.length > 0 ? (

                                <div className="sources-list">

                                    {sources.map((source, index) => {

                                        const isOpen =
                                            !!openSources[index];

                                        return (

                                            <article
                                                className="source-card"
                                                key={
                                                    source.document_id ||
                                                    `${source.title}-${index}`
                                                }
                                            >


                                                {/* SOURCE TOP */}

                                                <div className="source-main">


                                                    <div className="source-file-icon">

                                                        {source.file_type === "audio" ? (
                                                            <AudiotrackRoundedIcon />
                                                        ) : (
                                                            <DescriptionOutlinedIcon />
                                                        )}

                                                    </div>


                                                    <div className="source-info">

                                                        <div className="source-title-row">

                                                            <h4>
                                                                {source.title ||
                                                                    source.filename ||
                                                                    "Document sans titre"}
                                                            </h4>

                                                            <span className="source-number">
                                                                SOURCE {index + 1}
                                                            </span>

                                                        </div>


                                                        <p className="source-filename">

                                                            {source.filename ||
                                                                "Fichier archive"}

                                                        </p>


                                                        <div className="source-meta">

                                                            <span>

                                                                {source.file_type === "audio"
                                                                    ? "Audio"
                                                                    : "Document"}

                                                            </span>


                                                            {source.mime_type && (

                                                                <span>
                                                                    {source.mime_type}
                                                                </span>

                                                            )}


                                                            {source.file_size && (

                                                                <span>
                                                                    {Math.round(
                                                                        source.file_size / 1024
                                                                    )} KB
                                                                </span>

                                                            )}

                                                        </div>

                                                    </div>


                                                    {/* VIEW EXCERPT */}

                                                    <button
                                                        type="button"
                                                        className={
                                                            `source-view-button ${
                                                                isOpen
                                                                    ? "active"
                                                                    : ""
                                                            }`
                                                        }
                                                        onClick={() =>
                                                            toggleSource(index)
                                                        }
                                                    >

                                                        <VisibilityOutlinedIcon />

                                                        <span>
                                                            {isOpen
                                                                ? "Masquer"
                                                                : "Voir l'extrait"}
                                                        </span>

                                                        {isOpen ? (
                                                            <KeyboardArrowUpRoundedIcon />
                                                        ) : (
                                                            <KeyboardArrowDownRoundedIcon />
                                                        )}

                                                    </button>

                                                </div>


                                                {/* EXCERPT */}

                                                {isOpen && source.excerpt && (

                                                    <div
                                                        className="source-excerpt"
                                                        dir="auto"
                                                    >

                                                        <div className="excerpt-label">

                                                            <DescriptionOutlinedIcon />

                                                            Extrait du document

                                                        </div>


                                                        <p>
                                                            {source.excerpt}
                                                        </p>

                                                    </div>

                                                )}

                                            </article>

                                        );

                                    })}

                                </div>

                            ) : (

                                <div className="sources-empty">

                                    <DescriptionOutlinedIcon />

                                    <p>
                                        Aucun document source disponible.
                                    </p>

                                </div>

                            )}

                        </div>

                    </section>

                )}


                {/* =========================
                    EMPTY STATE
                ========================= */}

                {!result && !loading && !error && (

                    <section className="semantic-empty">

                        <div className="semantic-empty-icon">

                            <AutoAwesomeRoundedIcon />

                        </div>

                        <h2>
                            Posez votre question
                        </h2>

                        <p>
                            Exemple : « Qui était le chef de l'équipe
                            de Four dans le jeu ? »
                        </p>

                    </section>

                )}

            </main>

        </Layout>

    );

}


export default SemanticSearch;