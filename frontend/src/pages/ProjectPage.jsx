import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router';
import { useAuth } from '../context/AuthContext';
import api from '../api/StagesAPI'; // Или ваш API-клиент

export function ProjectPage() {
  const { projectId } = useParams(); // Получаем ID проекта из URL
  const { user } = useAuth();
  const navigate = useNavigate();
  //const [stages, setStages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [projectInfo, setProjectInfo] = useState(null);

  useEffect(() => {
    // if (!user) {
    //   navigate('/login', { replace: true });
    //   return;
    // }

    const fetchProjectData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Параллельно получаем информацию о проекте и его этапы
        const stagesResponse = await api.get(`/${projectId}`)

        console.log("Stages data:", stagesResponse.data);

        //setStages(stagesResponse.data || []);
      } catch (err) {
        console.error('Error fetching project data:', err);
        setError(err.response?.data?.detail || 'Failed to load project data');
        // Перенаправляем на главную если проект не найден
        // if (err.response?.status === 404) {
        //   navigate('/', { replace: true });
        // }
      } finally {
        setLoading(false);
      }
    };

    fetchProjectData();
  }, [projectId, user, navigate]);



  //if (!user) return null;
  if (loading) return <div className="loading">Loading project data...</div>;
  if (error) return <div className="error">Error: {error}</div>;


  return (
    <div className="project-page">
      <h1>ПРИВЕТСТВУЮ В ПРОЕКТЕ {projectId}</h1>
    </div>
  );
}