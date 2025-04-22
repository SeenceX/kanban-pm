import { Link } from 'react-router'
import members from '../img/members.svg'
import options from '../img/options.svg'


export function FounderProjectCard({project}){
    return (
        <div className="founder-card">
            <Link to={`/project/${project.id}`}>
            <div className="card-name">
                {project.title}
            </div>
            </Link>
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
    )
}