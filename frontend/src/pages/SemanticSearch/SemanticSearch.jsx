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

import "./SemanticSearch.css";


function SemanticSearch() {

    const [question, setQuestion] = useState("");
    const [result, setResult] = useState(null);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");


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


    return (

        <Layout>

            <main className="semantic-search-page">

                <PageHeader
                    title="Recherche sémantique"
                    description="Posez une question en langage naturel et retrouvez les informations pertinentes dans les archives SNRT."
                />


                {/* =========================
                    SEARCH BOX
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

                    <section className="panel semantic-result-panel">

                        <LoadingState />

                    </section>

                )}


                {/* =========================
                    RESULT
                ========================= */}

                {result && !loading && (

                    <section className="semantic-result-panel">

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

                                {result.chunks || 0} sources analysées

                            </div>

                        </div>


                        <div className="semantic-answer">

                            <div className="answer-icon">

                                <AutoAwesomeRoundedIcon />

                            </div>

                            <div className="answer-content">

                                <h3>
                                    Réponse
                                </h3>

                                <p>
                                    {result.answer}
                                </p>

                            </div>

                        </div>


                        {/* =========================
                            SOURCES - PREPARATION
                        ========================= */}

                        <div className="semantic-sources">

                            <div className="sources-header">

                                <h3>
                                    Documents utilisés
                                </h3>

                                <span>
                                    Les documents sources seront affichés ici.
                                </span>

                            </div>

                            <div className="sources-empty">

                                <DescriptionOutlinedIcon />

                                <p>
                                    Les extraits des documents pertinents
                                    seront affichés ici.
                                </p>

                            </div>

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