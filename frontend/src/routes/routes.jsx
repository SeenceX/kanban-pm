import {Routes, Route} from 'react-router'
import { MainPage } from '../pages/MainPage';
import { NoMatchPage } from '../pages/NoMatchPage';
import LoginPage from '../pages/LoginPage';

const AppRoutes = () => {
    const navigationRoutes = [
        {path: "/", element: <MainPage/>},
        {path: "/login", element: <LoginPage/>},
        {path: "*", element: <NoMatchPage/>},
    ];

    return (
        <Routes>
            {navigationRoutes.map((route) => (
                <Route key={route.path} path={route.path} element={route.element} />
            ))}
        </Routes>
    );
}

export default AppRoutes;