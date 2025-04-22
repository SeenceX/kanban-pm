import axios from 'axios';

const api = axios.create({
    baseURL: "http://localhost:8000/projects",
    withCredentials: true
});


export const projectsAPI = {
    self_projects: async (id) => {
        const response = await axios.get(`${api.baseURL}/project/${id}`);
        return response;
    }
}

export default api;