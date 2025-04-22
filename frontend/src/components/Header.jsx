import logo from '../logo.svg';
import search from '../img/search.svg'
import { Link } from 'react-router';
import { useAuth } from '../context/AuthContext';

export function Header(){

    const {user} = useAuth();

    return (
        <header className="header">
            <div className="header-container">
            <Link to="/">
                <img src={logo} className="header-logo" alt="logo"/>
            </Link>
            {user ? 
            <div className="search">
                <img src={search} className="search-img" alt="search"/>
                <input type="text" className="search-field" placeholder="Поиск"/>
            </div>
            : <></>}
            {user ? 
            <div className="header-controls">
                <input type="button" className="create-button" value="Создать"/>
                <div className="user">
                <img className="user-avatar" alt="user"/>
                </div>
            </div>
            : <></>}
            </div>
        </header>
    )
}