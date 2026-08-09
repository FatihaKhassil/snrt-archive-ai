import { useState } from "react";
import Layout from "../../components/Layout/Layout";
import "./Search.css";
import { ErrorNotice, LoadingState, PageHeader, StatusBadge, formatDate } from "../../components/AdminUI/AdminUI";
import SearchService from "../../services/searchService";
import SearchRoundedIcon from "@mui/icons-material/SearchRounded";
import DescriptionOutlinedIcon from "@mui/icons-material/DescriptionOutlined";

function Search() {
  const [keyword, setKeyword] = useState(""), [results, setResults] = useState(null), [loading, setLoading] = useState(false), [error, setError] = useState("");
  const submit = async (event) => { event.preventDefault(); const value = keyword.trim(); if (!value) return; try { setLoading(true); setError(""); setResults(await SearchService.search(value)); } catch (err) { setError(err.response?.data?.detail || "Recherche impossible. Veuillez réessayer."); setResults(null); } finally { setLoading(false); } };
  return <Layout><main className="admin-page"><PageHeader title="Recherche" description="Recherchez dans les documents indexés avec le moteur existant." /><form className="search-page-form" onSubmit={submit}><SearchRoundedIcon /><input value={keyword} onChange={(event) => setKeyword(event.target.value)} placeholder="Saisissez un mot-clé" aria-label="Mot-clé de recherche" /><button className="button button-primary" disabled={!keyword.trim() || loading}>{loading ? "Recherche…" : "Rechercher"}</button></form><ErrorNotice message={error} />{loading && <section className="panel"><LoadingState /></section>}{results && !loading && <section className="panel search-results"><div className="search-results-title"><h2>Résultats</h2><span>{results.length} document{results.length !== 1 ? "s" : ""}</span></div>{results.length ? <div className="result-list">{results.map((document) => <article className="result-item" key={document._id}><div className="result-icon"><DescriptionOutlinedIcon /></div><div className="result-content"><h3>{document.title}</h3><p>{document.original_filename}</p><div><span>{document.file_type === "audio" ? "Audio" : "Document"}</span><span>{formatDate(document.created_at)}</span><StatusBadge value={document.status} /></div></div></article>)}</div> : <div className="empty-state">Aucun document ne correspond à ce mot-clé.</div>}</section>}</main></Layout>;
}
export default Search;
