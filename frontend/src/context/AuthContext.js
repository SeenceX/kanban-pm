import { Children, createContext, useContext, useState } from "react";
import { authAPI } from "../api/LoginAPI";

const AuthContext = createContext(null);

export const AuthProvider = ({children}) => {
    const [user, setUser] = useState(null)

    const login = async (email, password) => {
        try {
            const data = await authAPI.login(email, password);
            setUser(data.data);
            localStorage.setItem('access_token', data.access_token)
            return {success: true};
        } catch(error) {
            console.error('Login error: ', error.detail || error.message);
            return {success: false, error: error.detail}
        }
    };
    
    const logout = () => {
        setUser(null);
        localStorage.removeItem('access_token');
    };

    return (
        <AuthContext.Provider value={{user, login, logout}}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);