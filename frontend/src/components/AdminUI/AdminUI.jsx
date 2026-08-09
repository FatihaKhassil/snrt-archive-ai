/* eslint-disable react-refresh/only-export-components */

import "./AdminUI.css";
import { getProfile } from "../../utils/storage";


export const roleLabel = (role) => ({
    ADMIN: "Administrateur",
    DOCUMENTALIST: "Documentaliste",
    SNRT_USER: "Utilisateur"
}[role] || role || "Utilisateur");


export const roleEyebrow = (role) => ({
    ADMIN: "ADMINISTRATION",
    DOCUMENTALIST: "DOCUMENTALISTE",
    SNRT_USER: "UTILISATEUR"
}[role] || "UTILISATEUR");


export function PageHeader({
    eyebrow,
    title,
    description,
    action
}) {

    const profile = getProfile();

    const role = profile?.role;

    const currentEyebrow =
        eyebrow || roleEyebrow(role);

    return (
        <div className="page-header">

            <div className="page-header-content">

                <span className="page-header-eyebrow">
                    {currentEyebrow}
                </span>

                <h1>
                    {title}
                </h1>

                {description && (
                    <p>
                        {description}
                    </p>
                )}

            </div>

            {action && (
                <div className="page-header-action">
                    {action}
                </div>
            )}

        </div>
    );
}


export function StatusBadge({ value }) {

    return (
        <span
            className={`status-badge status-${String(
                value || "unknown"
            ).toLowerCase()}`}
        >
            {value || "—"}
        </span>
    );
}


export function Modal({
    title,
    children,
    onClose
}) {

    return (
        <section
            className="modal"
            role="dialog"
            aria-modal="true"
            aria-label={title}
            onMouseDown={(event) => event.stopPropagation()}
        >

            <div className="modal-header">

                <h2>
                    {title}
                </h2>

                <button
                    type="button"
                    onClick={onClose}
                    aria-label="Fermer"
                >
                    ×
                </button>

            </div>

            <div className="modal-content">
                {children}
            </div>

        </section>
    );
}


export function ErrorNotice({ message }) {

    return message ? (
        <div className="error-notice">
            {message}
        </div>
    ) : null;
}


export function LoadingState() {

    return (
        <div className="loading-state">
            Chargement des données…
        </div>
    );
}


export const formatDate = (value) =>
    value
        ? new Intl.DateTimeFormat("fr-FR", {
              dateStyle: "medium"
          }).format(new Date(value))
        : "—";