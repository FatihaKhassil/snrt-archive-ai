import api from "../api/api";

class RagService {

    async ask(question) {

        const response = await api.post(
            "/rag/ask",
            {
                question: question
            }
        );

        return response.data;
    }
}

export default new RagService();