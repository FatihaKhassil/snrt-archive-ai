import { useRef, useState } from "react";
import Layout from "../../components/Layout/Layout";
import "./Upload.css";
import { ErrorNotice, PageHeader } from "../../components/AdminUI/AdminUI";
import UploadService from "../../services/uploadService";
import CloudUploadOutlinedIcon from "@mui/icons-material/CloudUploadOutlined";
import InsertDriveFileOutlinedIcon from "@mui/icons-material/InsertDriveFileOutlined";

function Upload() {
  const inputRef = useRef(null); const [file, setFile] = useState(null), [dragging, setDragging] = useState(false), [loading, setLoading] = useState(false), [message, setMessage] = useState(""), [error, setError] = useState("");
  const select = (selected) => { if (!selected) return; setFile(selected); setMessage(""); setError(""); };
  const submit = async () => { if (!file) { setError("Veuillez sélectionner un fichier."); return; } try { setLoading(true); setError(""); const response = await UploadService.upload(file); setMessage(response.message || "Document importé avec succès."); setFile(null); if (inputRef.current) inputRef.current.value = ""; } catch (err) { setError(err.response?.data?.detail || "Import impossible. Veuillez réessayer."); } finally { setLoading(false); } };
  return <Layout><main className="admin-page"><PageHeader title="Importer un document" description="Ajoutez un fichier à l’archive SNRT." /><section className="panel upload-panel"><ErrorNotice message={error} />{message && <div className="success-notice">{message}</div>}<input ref={inputRef} type="file" className="visually-hidden" onChange={(event) => select(event.target.files?.[0])} /><div className={`drop-zone${dragging ? " is-dragging" : ""}`} onDragOver={(event) => { event.preventDefault(); setDragging(true); }} onDragLeave={() => setDragging(false)} onDrop={(event) => { event.preventDefault(); setDragging(false); select(event.dataTransfer.files?.[0]); }} onClick={() => inputRef.current?.click()} role="button" tabIndex="0" onKeyDown={(event) => event.key === "Enter" && inputRef.current?.click()}><div className="upload-icon"><CloudUploadOutlinedIcon /></div><h2>Glissez-déposez votre fichier ici</h2><p>ou cliquez pour parcourir vos fichiers</p><span>Le format et la taille sont vérifiés par le service d’import existant.</span></div>{file && <div className="selected-file"><InsertDriveFileOutlinedIcon /><div><strong>{file.name}</strong><span>{(file.size / 1024 / 1024).toFixed(2)} Mo</span></div><button type="button" onClick={() => setFile(null)} aria-label="Retirer le fichier">×</button></div>}<div className="upload-actions"><button className="button button-secondary" type="button" onClick={() => { setFile(null); setError(""); setMessage(""); }}>Annuler</button><button className="button button-primary" type="button" onClick={submit} disabled={!file || loading}><CloudUploadOutlinedIcon />{loading ? "Import en cours…" : "Importer"}</button></div></section></main></Layout>;
}
export default Upload;
