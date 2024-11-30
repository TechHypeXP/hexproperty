import React from "react";
import { Chart as ChartJS, registerables } from "chart.js";
import '../types/chart.js';

ChartJS.register(...registerables);
interface ChartConfiguration {
  type: string;
  data: {
    labels: string[];
    datasets: {
      label: string;
      backgroundColor: string;
      borderColor: string;
      data: number[];
      fill: boolean;
    }[];
  };
  options: {
    maintainAspectRatio: boolean;
    responsive: boolean;
    plugins: {
      title: {
        display: boolean;
        text: string;
        color: string;
      };
      legend: {
        labels: {
          color: string;
        };
        align: string;
        position: string;
      };
      tooltip: {
        mode: string;
        intersect: boolean;
      };
    };
    interaction: {
      mode: string;
      intersect: boolean;
    };
    scales: {
      x: {
        ticks: {
          color: string;
        };
        display: boolean;
        title: {
          display: boolean;
          text: string;
          color: string;
        };
        grid: {
          display: boolean;
          borderDash: number[];
          borderDashOffset: number;
          color: string;
          borderColor: string;
        };
      };
      y: {
        ticks: {
          color: string;
        };
        display: boolean;
        title: {
          display: boolean;
          text: string;
          color: string;
        };
        grid: {
          borderDash: number[];
          borderDashOffset: number;
          drawBorder: boolean;
          color: string;
          borderColor: string;
        };
      };
    };
  };
}

declare global {
  interface Window {
    myLine: ChartJS;
  }
}

export default function CardLineChart(): JSX.Element {
  React.useEffect(() => {
    const config: ChartConfiguration = {
      type: "line",
      data: {
        labels: [
          "January",
          "February",
          "March",
          "April",
          "May",
          "June",
          "July",
        ],
        datasets: [
          {
            label: new Date().getFullYear().toString(),
            backgroundColor: "#4c51bf",
            borderColor: "#4c51bf",
            data: [65, 78, 66, 44, 56, 67, 75],
            fill: false,
          },
          {
            label: (new Date().getFullYear() - 1).toString(),
            fill: false,
            backgroundColor: "#fff",
            borderColor: "#fff",
            data: [40, 68, 86, 74, 56, 60, 87],
          },
        ],
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
        plugins: {
          title: {
            display: false,
            text: "Sales Charts",
            color: "white",
          },
          legend: {
            labels: {
              color: "white",
            },
            align: "end",
            position: "bottom",
          },
          tooltip: {
            mode: "index",
            intersect: false,
          },
        },
        interaction: {
          mode: "nearest",
          intersect: true,
        },
        scales: {
          x: {
            ticks: {
              color: "rgba(255,255,255,.7)",
            },
            display: true,
            title: {
              display: false,
              text: "Month",
              color: "white",
            },
            grid: {
              display: false,
              borderDash: [2],
              borderDashOffset: 2,
              color: "rgba(33, 37, 41, 0.3)",
              borderColor: "rgba(0, 0, 0, 0)",
            },
          },
          y: {
            ticks: {
              color: "rgba(255,255,255,.7)",
            },
            display: true,
            title: {
              display: false,
              text: "Value",
              color: "white",
            },
            grid: {
              borderDash: [3],
              borderDashOffset: 3,
              drawBorder: false,
              color: "rgba(255, 255, 255, 0.15)",
              borderColor: "rgba(33, 37, 41, 0)",
            },
          },
        },
      },
    };
    const ctx = document.getElementById("line-chart") as HTMLCanvasElement;
    window.myLine = new ChartJS(ctx.getContext("2d")!, config);
  }, []);

  return (
    <>
      <div className="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded bg-blueGray-700">
        <div className="rounded-t mb-0 px-4 py-3 bg-transparent">
          <div className="flex flex-wrap items-center">
            <div className="relative w-full max-w-full flex-grow flex-1">
              <h6 className="uppercase text-blueGray-100 mb-1 text-xs font-semibold">
                Overview
              </h6>
              <h2 className="text-white text-xl font-semibold">Sales value</h2>
            </div>
          </div>
        </div>
        <div className="p-4 flex-auto">
          {/* Chart */}
          <div className="relative h-350-px">
            <canvas id="line-chart"></canvas>
          </div>
        </div>
      </div>
    </>
  );
}
