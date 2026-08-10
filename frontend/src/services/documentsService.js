import api from "../api/api";

class DocumentsService {

    async getAll() {

        const response = await api.get(
            "/documents"
        );

        return response.data;
    }


    async getById(documentId) {

        const response = await api.get(
            `/documents/${documentId}`
        );

        return response.data;
    }


    async update(documentId, data) {

        const response = await api.put(
            `/documents/${documentId}`,
            data
        );

        return response.data;
    }


    async remove(documentId) {

        const response = await api.delete(
            `/documents/${documentId}`
        );

        return response.data;
    }


    async download(documentId) {

        const response = await api.get(
            `/documents/${documentId}/download`,
            {
                responseType: "blob"
            }
        );

        const blob = new Blob(
            [response.data],
            {
                type: response.headers["content-type"]
            }
        );

        const url = window.URL.createObjectURL(
            blob
        );

        const link = document.createElement("a");

        link.href = url;

        link.download =
            response.headers[
                "content-disposition"
            ]
                ?.split("filename=")[1]
                ?.replaceAll('"', "")
            || "document";

        document.body.appendChild(link);

        link.click();

        link.remove();

        window.URL.revokeObjectURL(url);
    }
}


export default new DocumentsService();