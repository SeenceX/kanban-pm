import members from '../img/members.svg'
import options from '../img/options.svg'


export function FounderProjectCard(){
    return (
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
    )
}