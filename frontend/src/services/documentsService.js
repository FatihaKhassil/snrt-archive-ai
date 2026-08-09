import api from "../api/api";

class DocumentsService {
  async getAll() { const response = await api.get("/documents"); return response.data; }
  async getById(documentId) { const response = await api.get(`/documents/${documentId}`); return response.data; }
  async update(documentId, data) { const response = await api.put(`/documents/${documentId}`, data); return response.data; }
  async remove(documentId) { const response = await api.delete(`/documents/${documentId}`); return response.data; }
}

export default new DocumentsService();
