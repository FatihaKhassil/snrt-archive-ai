export const saveSession = (data) => {
  const profile = {
    user_id: data.user_id,
    first_name: data.first_name,
    last_name: data.last_name,
    email: data.email,
    phone: data.phone,
    department: data.department,
    role: data.role,
    status: data.status
  };

  localStorage.setItem("token", data.access_token);
  localStorage.setItem("profile", JSON.stringify(profile));
};

export const clearSession = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("profile");
  localStorage.removeItem("role");
  localStorage.removeItem("user_id");
  localStorage.removeItem("first_name");
};

export const getProfile = () => {
  try { return JSON.parse(localStorage.getItem("profile")) || null; }
  catch { return null; }
};

export const getToken = () => localStorage.getItem("token");
export const getRole = () => getProfile()?.role || localStorage.getItem("role");
export const getFirstName = () => getProfile()?.first_name || localStorage.getItem("first_name");
export const isAuthenticated = () => !!localStorage.getItem("token");
