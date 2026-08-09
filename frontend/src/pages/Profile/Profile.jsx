import "./Profile.css";
import Layout from "../../components/Layout/Layout";
import { PageHeader, StatusBadge, roleLabel } from "../../components/AdminUI/AdminUI";
import { getProfile } from "../../utils/storage";
import LockResetRoundedIcon from "@mui/icons-material/LockResetRounded";

function Profile() {
  const profile = getProfile();
  const unavailable = "Non disponible";
  return <Layout><main className="admin-page"><PageHeader title="Mon profil" description="Consultez vos informations professionnelles." />{profile ? <div className="profile-page-grid"><section className="panel profile-summary"><div className="profile-hero"><div className="profile-photo">{profile.first_name?.[0] || "?"}{profile.last_name?.[0] || ""}</div><div><h2>{profile.first_name || unavailable} {profile.last_name || ""}</h2><p>{roleLabel(profile.role)}</p></div></div><div className="profile-info"><div><span>Email</span><strong>{profile.email || unavailable}</strong></div><div><span>Téléphone</span><strong>{profile.phone || unavailable}</strong></div><div><span>Département</span><strong>{profile.department || unavailable}</strong></div><div><span>Rôle</span><strong>{roleLabel(profile.role)}</strong></div><div><span>Statut</span><StatusBadge value={profile.status} /></div></div></section><section className="panel security-panel" id="security"><div className="section-heading"><div><h2>Sécurité du compte</h2><p>La modification de mot de passe sera disponible lorsque l’API correspondante sera activée.</p></div><LockResetRoundedIcon /></div><button className="button button-secondary" type="button" disabled><LockResetRoundedIcon />Changer le mot de passe</button></section></div> : <section className="panel profile-empty">Les informations de session ne sont pas disponibles. Veuillez vous reconnecter.</section>}</main></Layout>;
}

export default Profile;
