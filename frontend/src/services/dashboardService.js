import api from "../api/api";

class DashboardService {

    async getStatistics() {

        const response = await api.get("/dashboard/stats");

        return response.data;

    }

}

export default new DashboardService();