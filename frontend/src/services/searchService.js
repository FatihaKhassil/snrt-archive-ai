import api from "../api/api";

class SearchService {
  async search(keyword) {
    const response = await api.get("/search", { params: { keyword } });
    return response.data;
  }
}

export default new SearchService();
