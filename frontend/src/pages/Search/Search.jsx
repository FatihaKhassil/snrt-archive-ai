import { useState } from "react";

import Layout from "../../components/Layout/Layout";

import "./Search.css";

import {
    ErrorNotice,
    LoadingState,
    PageHeader,
    StatusBadge,
    formatDate
} from "../../components/AdminUI/AdminUI";

import SearchService from "../../services/searchService";

import SearchRoundedIcon from "@mui/icons-material/SearchRounded";
import DescriptionOutlinedIcon from "@mui/icons-material/DescriptionOutlined";
import VisibilityOutlinedIcon from "@mui/icons-material/VisibilityOutlined";
import DownloadOutlinedIcon from "@mui/icons-material/DownloadOutlined";
import KeyboardArrowDownRoundedIcon from "@mui/icons-material/KeyboardArrowDownRounded";


function Search() {

    const [keyword, setKeyword] = useState("");

    const [results, setResults] = useState(null);

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");

    const [expandedResult, setExpandedResult] = useState(null);


    const submit = async (event) => {

        event.preventDefault();

        const value = keyword.trim();

        if (!value) {
            return;
        }

        try {

            setLoading(true);

            setError("");

            setResults(null);

            setExpandedResult(null);

            const response =
                await SearchService.search(value);

            setResults(response);

        } catch (err) {

            console.error(err);

            setError(
                err.response?.data?.detail ||
                "Recherche impossible. Veuillez réessayer."
            );

            setResults(null);

        } finally {

            setLoading(false);

        }
    };


    const toggleResult = (index) => {

        setExpandedResult(
            expandedResult === index
                ? null
                : index
        );

    };


    /*
     * Récupérer l'identifiant du document.
     *
     * On accepte plusieurs formats car la réponse
     * Solr peut utiliser id, _id ou document_id.
     */

    const getDocumentId = (document) => {

        return (
            document.document_id ||
            document._id ||
            document.id
        );

    };


    return (

        <Layout>

            <main className="admin-page">


                {/* =====================================================
                    HEADER
                ===================================================== */}

                <PageHeader
                    title="Recherche"
                    description="Recherchez dans les documents indexés avec le moteur existant."
                />


                {/* =====================================================
                    SEARCH FORM
                ===================================================== */}

                <form
                    className="search-page-form"
                    onSubmit={submit}
                >

                    <SearchRoundedIcon />

                    <input
                        value={keyword}
                        onChange={(event) =>
                            setKeyword(event.target.value)
                        }
                        placeholder="Saisissez un mot-clé"
                        aria-label="Mot-clé de recherche"
                    />


                    <button
                        type="submit"
                        className="button button-primary"
                        disabled={
                            !keyword.trim() ||
                            loading
                        }
                    >

                        <SearchRoundedIcon />

                        {loading
                            ? "Recherche…"
                            : "Rechercher"
                        }

                    </button>

                </form>


                {/* =====================================================
                    ERROR
                ===================================================== */}

                <ErrorNotice message={error} />


                {/* =====================================================
                    LOADING
                ===================================================== */}

                {loading && (

                    <section className="panel">

                        <LoadingState />

                    </section>

                )}


                {/* =====================================================
                    RESULTS
                ===================================================== */}

                {results && !loading && (

                    <section className="panel search-results">


                        {/* =================================================
                            RESULTS HEADER
                        ================================================= */}

                        <div className="search-results-title">

                            <div>

                                <h2>
                                    Résultats
                                </h2>

                                <p>
                                    Documents correspondant à votre recherche
                                </p>

                            </div>


                            <span className="results-count">

                                {results.length}

                                {" "}

                                document
                                {results.length !== 1 ? "s" : ""}

                            </span>

                        </div>


                        {/* =================================================
                            RESULT LIST
                        ================================================= */}

                        {results.length ? (

                            <div className="result-list">

                                {results.map(
                                    (document, index) => {

                                        const documentId =
                                            getDocumentId(document);

                                        const isExpanded =
                                            expandedResult === index;


                                        return (

                                            <article
                                                className="result-item"
                                                key={
                                                    documentId ||
                                                    `${document.title}-${index}`
                                                }
                                            >


                                                {/* =================================
                                                    DOCUMENT ICON
                                                ================================= */}

                                                <div className="result-icon">

                                                    <DescriptionOutlinedIcon />

                                                </div>


                                                {/* =================================
                                                    CONTENT
                                                ================================= */}

                                                <div className="result-content">


                                                    <div className="result-title-row">

                                                        <h3>

                                                            {document.title ||
                                                                document.original_filename ||
                                                                document.filename ||
                                                                "Document"}

                                                        </h3>


                                                        <span className="result-number">

                                                            RÉSULTAT {index + 1}

                                                        </span>

                                                    </div>


                                                    <p>

                                                        {document.original_filename ||
                                                            document.filename ||
                                                            "Fichier source"}

                                                    </p>


                                                    <div className="result-meta">


                                                        <span>

                                                            {document.file_type === "audio"
                                                                ? "Audio"
                                                                : "Document"}

                                                        </span>


                                                        {document.created_at && (

                                                            <span>

                                                                {formatDate(
                                                                    document.created_at
                                                                )}

                                                            </span>

                                                        )}


                                                        {document.status && (

                                                            <StatusBadge
                                                                value={
                                                                    document.status
                                                                }
                                                            />

                                                        )}

                                                    </div>

                                                </div>


                                                {/* =================================
                                                    ACTIONS
                                                ================================= */}

                                                <div className="result-actions">


                                                    {/* =================================
                                                        VOIR L'EXTRAIT
                                                    ================================= */}

                                                    <button
                                                        type="button"
                                                        className="result-view-button"
                                                        onClick={() =>
                                                            toggleResult(index)
                                                        }
                                                    >

                                                        <VisibilityOutlinedIcon />

                                                        <span>

                                                            {isExpanded
                                                                ? "Masquer l'extrait"
                                                                : "Voir l'extrait"}

                                                        </span>


                                                        <KeyboardArrowDownRoundedIcon
                                                            className={
                                                                isExpanded
                                                                    ? "expanded"
                                                                    : ""
                                                            }
                                                        />

                                                    </button>


                                                    {/* =================================
                                                        TÉLÉCHARGER ORIGINAL
                                                    ================================= */}

                                                    {documentId ? (

                                                        <a
                                                            className="result-download-button"
                                                            href={`http://localhost:8000/documents/${documentId}/download`}
                                                            title="Télécharger le fichier original"
                                                        >

                                                            <DownloadOutlinedIcon />

                                                            <span>
                                                                Télécharger
                                                            </span>

                                                        </a>

                                                    ) : (

                                                        <button
                                                            type="button"
                                                            className="result-download-button"
                                                            disabled
                                                        >

                                                            <DownloadOutlinedIcon />

                                                            <span>
                                                                Télécharger
                                                            </span>

                                                        </button>

                                                    )}

                                                </div>


                                                {/* =================================
                                                    EXCERPT
                                                ================================= */}

                                                {isExpanded && (

                                                    <div className="result-excerpt">


                                                        <div className="excerpt-header">

                                                            <DescriptionOutlinedIcon />

                                                            <span>
                                                                Extrait du document
                                                            </span>

                                                        </div>


                                                        <p dir="auto">

                                                            {document.excerpt ||
                                                                document.transcription ||
                                                                document.content ||
                                                                "Aucun extrait disponible pour ce document."}

                                                        </p>

                                                    </div>

                                                )}

                                            </article>

                                        );

                                    }
                                )}

                            </div>

                        ) : (

                            <div className="empty-state">

                                Aucun document ne correspond à ce mot-clé.

                            </div>

                        )}

                    </section>

                )}

            </main>

        </Layout>

    );

}


export default Search;