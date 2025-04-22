import { useNavigate } from 'react-router';
import './App.css';
import { Header } from './components/Header';
import AppRoutes from './routes/routes';


function App() {

  const navigate = useNavigate()

  return (
    <div className="App">
      <Header/>
      <AppRoutes/>
    </div>
  );
}

export default App;
