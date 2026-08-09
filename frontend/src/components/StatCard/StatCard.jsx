import "./StatCard.css";

function StatCard({

    title,

    value,

    icon,

    color,

    subtitle

}) {

    return (

        <div className="stat-card">

            <div
                className="stat-icon"
                style={{

                    background: color

                }}
            >

                {icon}

            </div>

            <div className="stat-content">

                <h4>

                    {title}

                </h4>

                <h2>

                    {value}

                </h2>

                <span>

                    {subtitle}

                </span>

            </div>

        </div>

    );

}

export default StatCard;