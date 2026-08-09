import api from "../api/api";

class UploadService {
    async upload(file) {
        const data = new FormData();
        data.append("file", file);

        const response = await api.post(
            "/api/v1/upload/",
            data
        );

        return response.data;
    }
}

export default new UploadService();