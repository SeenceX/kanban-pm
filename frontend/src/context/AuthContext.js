import { createContext, useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router";
import api from "../api/auth";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const navigate = useNavigate();

    const login = async (email, password) => {
        try {
            const response = await api.post('/login', { email, password });
            setUser(response.data.user);
            return { success: true };
        } catch (error) {
            return { 
                success: false, 
                error: error.response?.data?.detail || error.message 
            };
        }
    };
    
    const logout = async () => {
        try {
            await api.post('/logout');
        } finally {
            setUser(null);
            navigate('/login');
        }
    };

    // Автоматическая проверка токена при загрузке
    useEffect(() => {
        const checkAuth = async () => {
            try {
                const token = localStorage.getItem('access_token');
                if (token) {
                    const response = await api.get('/me');
                    setUser(response.data);
                }
            } catch (error) {
                logout();
            }
        };
        checkAuth();
    });

    return (
        <AuthContext.Provider value={{ user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);