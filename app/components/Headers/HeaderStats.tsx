import React from "react";

// components
import CardStats from "components/Cards/CardStats";

interface StatCardProps {
  title: string;
  subtitle: string;
  arrow: "up" | "down";
  percent: string;
  description: string;
  iconName: string;
  iconColor: string;
  percentColor: string;
}

const HeaderStats: React.FC = () => {
  const stats: StatCardProps[] = [
    {
      title: "350,897",
      subtitle: "TRAFFIC",
      arrow: "up",
      percent: "3.48",
      percentColor: "text-emerald-500",
      description: "Since last month",
      iconName: "far fa-chart-bar",
      iconColor: "bg-red-500"
    },
    {
      title: "2,356",
      subtitle: "NEW USERS",
      arrow: "down",
      percent: "3.48",
      percentColor: "text-red-500",
      description: "Since last week",
      iconName: "fas fa-chart-pie",
      iconColor: "bg-orange-500"
    },
    {
      title: "924",
      subtitle: "SALES",
      arrow: "down",
      percent: "1.10",
      percentColor: "text-orange-500",
      description: "Since yesterday",
      iconName: "fas fa-users",
      iconColor: "bg-pink-500"
    },
    {
      title: "49,65%",
      subtitle: "PERFORMANCE",
      arrow: "up",
      percent: "12",
      percentColor: "text-emerald-500",
      description: "Since last month",
      iconName: "fas fa-percent",
      iconColor: "bg-lightBlue-500"
    }
  ];

  return (
    <>
      {/* Header */}
      <div className="relative bg-blueGray-800 md:pt-32 pb-32 pt-12">
        <div className="px-4 md:px-10 mx-auto w-full">
          <div>
            {/* Card stats */}
            <div className="flex flex-wrap">
              {stats.map((stat) => (
                <div key={stat.subtitle} className="w-full lg:w-6/12 xl:w-3/12 px-4">
                  <CardStats
                    statSubtitle={stat.subtitle}
                    statTitle={stat.title}
                    statArrow={stat.arrow}
                    statPercent={stat.percent}
                    statPercentColor={stat.percentColor}
                    statDescripiron={stat.description}
                    statIconName={stat.iconName}
                    statIconColor={stat.iconColor}
                  />
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default HeaderStats;
