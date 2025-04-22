import {Routes, Route} from 'react-router'
import { MainPage } from '../pages/MainPage';
import { NoMatchPage } from '../pages/NoMatchPage';
import LoginPage from '../pages/LoginPage';
import { ProjectPage } from '../pages/ProjectPage';

const AppRoutes = () => {
    const navigationRoutes = [
        {path: "/", element: <MainPage/>},
        {path: "/login", element: <LoginPage/>},
        {path: "/project/:projectId", element: <ProjectPage/>},
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