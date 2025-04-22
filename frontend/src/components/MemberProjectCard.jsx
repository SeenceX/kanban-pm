import { Link } from "react-router"

export function MemberProjectCard({project}){
    return (
        <Link to={`/project/${project.id}`} className="member-card" href="#">
            <div className="member-card-inner">
            <p className="member-card-name">
                {project.title}
            </p>
            </div>
        </Link>
    )
}