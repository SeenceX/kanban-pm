import { useNavigate } from 'react-router';
import { useAuth } from '../context/AuthContext';
import { FounderProjectCard } from '../components/FounderProjectCard';
import { MemberProjectCard } from '../components/MemberProjectCard';

export function MainPage(){

    const {user} = useAuth();
    const navigate = useNavigate();

    if (!user){
        navigate('/login')
        return null;
    }

    return (
    <div className="wrapper">
        <div className="founder">
          <h2 className="founder-title">Основатель</h2>
          <div className="founder-cards">
            <FounderProjectCard/>
          </div>
        </div>
        <div className="member">
          <h2 className="member-title">Участник</h2>
          <div className="member-cards">
            <MemberProjectCard/>
          </div>
        </div>
      </div>
    )
}

