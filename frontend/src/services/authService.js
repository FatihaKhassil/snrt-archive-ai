import api from "../api/api";

class AuthService {

    async login(email, password) {

        const response = await api.post(

            "/auth/login",

            {
                email,
                password
            }

        );

        return response.data;

    }

}

export default new AuthService();