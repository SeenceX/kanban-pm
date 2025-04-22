import { useState } from 'react';
import { useAuth } from '../context/AuthContext'; 
import { Link, useNavigate } from 'react-router';
import '../styles/LoginPage.css';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth(); 
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    const result = await login(email, password);

    if (result.success) {
        navigate('/');
    }
    else{
        setError(result.error)
    }
  };

  return (
    <div className="login-wrapper">
      <div className="login-form">
        <h1 className="login-title">Вход</h1>
        
        <form onSubmit={handleSubmit} className="login-form-content">
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="login-input"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Пароль</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="login-input"
              required
            />
          </div>

          <div className="form-links">
            <Link to="/register" className="form-link">Регистрация</Link>
            <Link to="/forgot-password" className="form-link">Забыли пароль?</Link>
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" className="login-button">
            Войти
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;