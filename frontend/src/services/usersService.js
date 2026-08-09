import api from "../api/api";

class UsersService {
  async getAll() { const response = await api.get("/users"); return response.data; }
  async getById(userId) { const response = await api.get(`/users/${userId}`); return response.data; }
  async create(data) { const response = await api.post("/users", data); return response.data; }
  async update(userId, data) { const response = await api.put(`/users/${userId}`, data); return response.data; }
  async remove(userId) { const response = await api.delete(`/users/${userId}`); return response.data; }
}

export default new UsersService();
