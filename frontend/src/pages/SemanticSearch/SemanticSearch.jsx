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
import AudioFileRoundedIcon from "@mui/icons-material/AudioFileRounded";
import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";
import DownloadRoundedIcon from "@mui/icons-material/DownloadRounded";
import KeyboardArrowDownRoundedIcon from "@mui/icons-material/KeyboardArrowDownRounded";

import "./SemanticSearch.css";


function SemanticSearch() {

    const [question, setQuestion] = useState("");

    const [result, setResult] = useState(null);

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");

    const [expandedSource, setExpandedSource] = useState(null);


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

            setExpandedSource(null);

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

        setExpandedSource(
            expandedSource === index
                ? null
                : index
        );

    };


    /*
     * Les sources viennent directement de la réponse RAG.
     *
     * Exemple :
     *
     * {
     *   document_id: "...",
     *   title: "part2",
     *   filename: "part2.wav",
     *   file_type: "audio",
     *   excerpt: "...",
     *   mime_type: "audio/wav",
     *   file_size: 4197690
     * }
     */

    const sources = result?.sources || [];


    return (

        <Layout>

            <main className="semantic-search-page">


                {/* =====================================================
                    HEADER + SEARCH
                ===================================================== */}

                <PageHeader
                    title="Recherche sémantique"
                    description="Posez une question en langage naturel et retrouvez les informations pertinentes dans les archives SNRT."
                />


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


                {/* =====================================================
                    ERROR
                ===================================================== */}

                <ErrorNotice message={error} />


                {/* =====================================================
                    LOADING
                ===================================================== */}

                {loading && (

                    <section className="panel semantic-result-panel">

                        <LoadingState />

                    </section>

                )}


                {/* =====================================================
                    RESULT
                ===================================================== */}

                {result && !loading && (

                    <section className="semantic-result-panel">


                        {/* =================================================
                            RESULT HEADER
                        ================================================= */}

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

                                <DescriptionOutlinedIcon />

                                <span>
                                    {sources.length}
                                </span>

                                sources analysées

                            </div>

                        </div>


                        {/* =================================================
                            ANSWER
                        ================================================= */}

                        <div className="semantic-answer">

                            <div className="answer-icon">

                                <AutoAwesomeRoundedIcon />

                            </div>


                            <div className="answer-content">

                                <h3>
                                    Réponse
                                </h3>

                                <p dir="auto">
                                    {result.answer ||
                                        "Aucune réponse n'a été générée."}
                                </p>

                            </div>

                        </div>


                        {/* =================================================
                            SOURCES
                        ================================================= */}

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

                                    <span>
                                        {sources.length}
                                    </span>

                                    document
                                    {sources.length !== 1 ? "s" : ""}

                                </div>

                            </div>


                            {/* =================================================
                                SOURCE LIST
                            ================================================= */}

                            {sources.length > 0 ? (

                                <div className="sources-list">

                                    {sources.map((source, index) => (

                                        <article
                                            className="source-card"
                                            key={
                                                source.document_id ||
                                                `${source.filename}-${index}`
                                            }
                                        >


                                            {/* =================================
                                                SOURCE MAIN
                                            ================================= */}

                                            <div className="source-main">


                                                {/* FILE ICON */}

                                                <div className="source-file-icon">

                                                    {source.file_type === "audio" ? (

                                                        <AudioFileRoundedIcon />

                                                    ) : (

                                                        <DescriptionOutlinedIcon />

                                                    )}

                                                </div>


                                                {/* SOURCE INFORMATION */}

                                                <div className="source-info">


                                                    <div className="source-title-row">

                                                        <h4>

                                                            {source.title ||
                                                                source.filename ||
                                                                "Document"}

                                                        </h4>


                                                        <span className="source-number">

                                                            SOURCE {index + 1}

                                                        </span>

                                                    </div>


                                                    <p className="source-filename">

                                                        {source.filename ||
                                                            source.original_filename ||
                                                            "Fichier source"}

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

                                                                {(
                                                                    source.file_size /
                                                                    1024
                                                                ).toFixed(0)}{" "}
                                                                KB

                                                            </span>

                                                        )}

                                                    </div>

                                                </div>


                                                {/* =================================
                                                    ACTIONS
                                                ================================= */}

                                                <div className="source-actions">


                                                    {/* VIEW EXCERPT */}

                                                    <button
                                                        type="button"
                                                        className={`source-view-button ${
                                                            expandedSource === index
                                                                ? "active"
                                                                : ""
                                                        }`}
                                                        onClick={() =>
                                                            toggleSource(index)
                                                        }
                                                    >

                                                        <VisibilityOutlinedIcon />

                                                        <span>

                                                            {expandedSource === index
                                                                ? "Masquer l'extrait"
                                                                : "Voir l'extrait"}

                                                        </span>

                                                        <KeyboardArrowDownRoundedIcon />

                                                    </button>


                                                    {/* DOWNLOAD ORIGINAL */}

                                                    {source.document_id && (

                                                        <a
                                                            className="source-download-button"
                                                            href={`http://localhost:8000/documents/${source.document_id}/download`}
                                                            title="Télécharger le document original"
                                                        >

                                                            <DownloadRoundedIcon />

                                                            <span>
                                                                Télécharger
                                                            </span>

                                                        </a>

                                                    )}

                                                </div>

                                            </div>


                                            {/* =================================
                                                EXCERPT
                                            ================================= */}

                                            {expandedSource === index && (

                                                <div className="source-excerpt">


                                                    <div className="excerpt-label">

                                                        <DescriptionOutlinedIcon />

                                                        <span>
                                                            Extrait utilisé pour répondre
                                                        </span>

                                                    </div>


                                                    <p dir="auto">

                                                        {source.excerpt ||
                                                            "Aucun extrait disponible pour ce document."}

                                                    </p>

                                                </div>

                                            )}

                                        </article>

                                    ))}

                                </div>

                            ) : (

                                <div className="sources-empty">

                                    <DescriptionOutlinedIcon />

                                    <p>
                                        Aucun document source n'a été retourné.
                                    </p>

                                </div>

                            )}

                        </div>

                    </section>

                )}


                {/* =====================================================
                    EMPTY STATE
                ===================================================== */}

                {!result && !loading && !error && (

                    <section className="semantic-empty">

                        <div className="semantic-empty-icon">

                            <AutoAwesomeRoundedIcon />

                        </div>


                        <h2>
                            Posez votre question
                        </h2>


                        <p>
                            Exemple : « Que s'est-il passé lors de
                            l'attaque de la ville ? »
                        </p>

                    </section>

                )}

            </main>

        </Layout>

    );

}


export default SemanticSearch;