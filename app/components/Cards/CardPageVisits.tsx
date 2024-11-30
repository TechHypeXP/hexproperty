import React from "react";

interface PageVisit {
  pageName: string;
  visitors: number;
  uniqueUsers: number;
  bounceRate: number;
  trend: "up" | "down";
}

const pageVisitsData: PageVisit[] = [
  {
    pageName: "/argon/",
    visitors: 4569,
    uniqueUsers: 340,
    bounceRate: 46.53,
    trend: "up"
  },
  {
    pageName: "/argon/index.html",
    visitors: 3985,
    uniqueUsers: 319,
    bounceRate: 46.53,
    trend: "down"
  },
  {
    pageName: "/argon/charts.html",
    visitors: 3513,
    uniqueUsers: 294,
    bounceRate: 36.49,
    trend: "down"
  },
  {
    pageName: "/argon/tables.html",
    visitors: 2050,
    uniqueUsers: 147,
    bounceRate: 50.87,
    trend: "up"
  },
  {
    pageName: "/argon/profile.html",
    visitors: 1795,
    uniqueUsers: 190,
    bounceRate: 46.53,
    trend: "down"
  }
];

export default function CardPageVisits(): JSX.Element {
  return (
    <>
      <div className="relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-lg rounded">
        <div className="rounded-t mb-0 px-4 py-3 border-0">
          <div className="flex flex-wrap items-center">
            <div className="relative w-full px-4 max-w-full flex-grow flex-1">
              <h3 className="font-semibold text-base text-blueGray-700">
                Page visits
              </h3>
            </div>
            <div className="relative w-full px-4 max-w-full flex-grow flex-1 text-right">
              <button
                className="bg-indigo-500 text-white active:bg-indigo-600 text-xs font-bold uppercase px-3 py-1 rounded outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150"
                type="button"
              >
                See all
              </button>
            </div>
          </div>
        </div>
        <div className="block w-full overflow-x-auto">
          {/* Projects table */}
          <table className="items-center w-full bg-transparent border-collapse">
            <thead>
              <tr>
                <th className="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                  Page name
                </th>
                <th className="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                  Visitors
                </th>
                <th className="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                  Unique users
                </th>
                <th className="px-6 bg-blueGray-50 text-blueGray-500 align-middle border border-solid border-blueGray-100 py-3 text-xs uppercase border-l-0 border-r-0 whitespace-nowrap font-semibold text-left">
                  Bounce rate
                </th>
              </tr>
            </thead>
            <tbody>
              {pageVisitsData.map((visit, index) => (
                <tr key={index}>
                  <th className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 text-left">
                    {visit.pageName}
                  </th>
                  <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                    {visit.visitors.toLocaleString()}
                  </td>
                  <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                    {visit.uniqueUsers}
                  </td>
                  <td className="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4">
                    <i className={`fas fa-arrow-${visit.trend} text-${visit.trend === "up" ? "emerald" : "orange"}-500 mr-4`}></i>
                    {visit.bounceRate.toFixed(2)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
