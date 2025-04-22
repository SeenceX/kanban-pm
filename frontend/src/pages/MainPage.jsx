import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';
import { useAuth } from '../context/AuthContext';
import { FounderProjectCard } from '../components/FounderProjectCard';
import { MemberProjectCard } from '../components/MemberProjectCard';
import api from '../api/ProjectsAPI'

export function MainPage() {

  const { user } = useAuth();
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [projectsMember, setProjectsMember] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!user) {
      navigate('/login', { replace: true });
      return;
    }

    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        const [projectsRes, membersRes] = await Promise.all([
          api.get(`/project/${user.id}`).catch(e => ({ data: [] })),
          api.get(`/project_membership/${user.id}`).catch(e => ({ data: [] }))
        ]);

        console.log("Projects response:", projectsRes);
        console.log("Members response:", membersRes);

        // Проверяем и нормализуем данные
        const projectsData = Array.isArray(projectsRes.data) ? projectsRes.data : [];
        const membersData = Array.isArray(membersRes.data) ? membersRes.data : [];

        setProjects(projectsData);
        setProjectsMember(membersData);
      } catch (err) {
        console.error('Full fetch error:', err);
        setError(err.response?.data?.detail || 'Failed to fetch data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [user, navigate]);

  if (loading) return <div>Loading projects...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="wrapper">
      <div className="founder">
        <h2 className="founder-title">Основатель</h2>
        <div className="founder-cards">
          {projects.filter(p => p.creator_id === user.id).map(project => (
            <FounderProjectCard key={project.id} project={project} />
          ))}
        </div>
      </div>
      <div className="member">
        <h2 className="member-title">Участник</h2>
        <div className="member-cards">
          {projectsMember.map(pm => (
            <MemberProjectCard key={pm.id} project={pm} />
          ))}
        </div>
      </div>
    </div>
  )
}

