import React from "react";

interface SocialTrafficData {
  referral: string;
  visitors: number;
  percentage: number;
  color: {
    bg: string;
    bar: string;
  };
}

interface ProgressBarProps {
  percentage: number;
  color: {
    bg: string;
    bar: string;
  };
}

const ProgressBar: React.FC<ProgressBarProps> = ({ percentage, color }) => (
  <div className="flex items-center">
    <span className="mr-2">{percentage}%</span>
    <div className="relative w-full">
      <div className={`overflow-hidden h-2 text-xs flex rounded ${color.bg}`}>
        <div
          style={{ width: `${percentage}%` }}
          className={`shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center ${color.bar}`}
        ></div>
      </div>
    </div>
  </div>
);

const socialTrafficData: SocialTrafficData[] = [
  {
    referral: "Facebook",
    visitors: 1480,
    percentage: 60,
    color: {
      bg: "bg-red-200",
      bar: "bg-red-500"
    }
  },
  {
    referral: "Facebook",
    visitors: 5480,
    percentage: 70,
    color: {
      bg: "bg-emerald-200",
      bar: "bg-emerald-500"
    }
  },
  {
    referral: "Google",
    visitors: 4807,
    percentage: 80,
    color: {
      bg: "bg-purple-200",
      bar: "bg-purple-500"
    }
  },
  {
    referral: "Instagram",
    visitors: 3678,
    percentage: 75,
    color: {
      bg: "bg-lightBlue-200",
      bar: "bg-lightBlue-500"
    }
  },
  {
    referral: "Twitter",
    visitors: 2645,
    percentage: 30,
    color: {
      bg: "bg-orange-200",
      bar: "bg-emerald-500"
    }
  }
];

interface CardSocialTrafficProps {
  data?: SocialTrafficData[];
}

const CardSocialTraffic: React.FC<CardSocialTrafficProps> = ({ 
  data = socialTrafficData 
}) => {
  const handleSeeAllClick = React.useCallback(() => {
    // Handle see all button click
    console.log("See all clicked");
  }, []);

  return (
    <>
      <div className="relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-lg rounded">
        <div className="rounded-t mb-0 px-4 py-3 border-0">
          <div className="flex flex-wrap items-center">
            <div className="relative w-full px-4 max-w-full flex-grow flex-1">
              <h3 className="font-semibold text-base text-blueGray-700">
                Social traffic
              </h3>
            </div>
            <div className="relative w-full px-4 max-w-full flex-grow flex-1 text-right">
              <button
                className="bg-indigo-500 text-white active:bg-indigo-600 text-xs font-bold uppercase px-3 py-1 rounded outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150"
                type="button"
                onClick={handleSeeAllClick}
              >
                See all
              </button>
            </div>
          </div>
        </div>
        <div className="block w-full overflow-x-auto">
          <table className="items-center w-full bg-transparent border-collapse">
            <thead className="thead-light">
              <tr>
                <th className="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                  Referral
                </th>
                <th className="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                  Visitors
                </th>
                <th className="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left min-w-140-px"></th>
              </tr>
            </thead>
            <tbody>
              {data.map((item, index) => (
                <tr key={`${item.referral}-${index}`}>
                  <th className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 text-left">
                    {item.referral}
                  </th>
                  <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                    {item.visitors.toLocaleString()}
                  </td>
                  <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                    <ProgressBar percentage={item.percentage} color={item.color} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
};

export default CardSocialTraffic;
