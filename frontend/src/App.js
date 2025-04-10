import logo from './logo.svg';
import search from './img/search.svg'
import members from './img/members.svg'
import options from './img/options.svg'
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="header">
        <div className="header-container">
          <a href="/">
            <img src={logo} className="header-logo" alt="logo"/>
          </a>
          <div className="search">
            <img src={search} className="search-img" alt="search"/>
            <input type="text" className="search-field" placeholder="Поиск"/>
          </div>
          <div className="header-controls">
            <input type="button" className="create-button" value="Создать"/>
            <div className="user">
              <img className="user-avatar" alt="user"/>
            </div>
          </div>
        </div>
      </header>
      <div className="wrapper">
        <div className="founder">
          <h2 className="founder-title">Основатель</h2>
          <div className="founder-cards">
            <div className="founder-card">
              <a href="#">
                <div className="card-name">
                  Разработка жидкостного ракетного двигателя (ЖРД)
                </div>
              </a>
              <div className="card-controls">
                <div className="card-members">
                  <img src={members} alt="members"/>
                  <input type="button" value="Участники"/>
                  </div>
                <div className="card-options">
                  <img src={options} alt="options"/>
                  <input type="button" value="Настройки"/>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="member">
          <h2 className="member-title">Участник</h2>
          <div className="member-cards">
            <a className="member-card" href="#">
              <div className="member-card-inner">
                <p className="member-card-name">
                  Курс Fullstack-разработчик на Python
                </p>
              </div>
            </a>
            <a className="member-card" href="#">
              <div className="member-card-inner">
                <p className="member-card-name">
                  Курс Fullstack-разработчик на Python
                </p>
              </div>
            </a>
            <a className="member-card" href="#">
              <div className="member-card-inner">
                <p className="member-card-name">
                  Курс Fullstack-разработчик на Python
                </p>
              </div>
            </a>
            <a className="member-card" href="#">
              <div className="member-card-inner">
                <p className="member-card-name">
                  Курс Fullstack-разработчик на Python
                </p>
              </div>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
