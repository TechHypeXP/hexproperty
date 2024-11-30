import { ChartConfiguration, ChartDataset } from '../types/chart.types';

export class LineChartService {
  private static instance: LineChartService;

  private constructor() {}

  public static getInstance(): LineChartService {
    if (!LineChartService.instance) {
      LineChartService.instance = new LineChartService();
    }
    return LineChartService.instance;
  }

  public generateDataset(label: string, color: string, data: number[]): ChartDataset {
    return {
      label,
      backgroundColor: color,
      borderColor: color,
      data,
      fill: false,
      tension: 0.4,
    };
  }

  public getConfiguration(currentMonthData: number[], previousMonthData: number[]): ChartConfiguration {
    return {
      type: "line",
      data: {
        labels: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        datasets: [
          this.generateDataset("Current Month", "#4c51bf", currentMonthData),
          this.generateDataset("Previous Month", "#fff", previousMonthData),
        ],
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
        plugins: {
          title: {
            display: false,
            text: "Sales Chart",
          },
          legend: {
            labels: {
              color: "rgba(255,255,255,.7)",
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
            display: true,
            title: {
              display: false,
              text: "Month",
            },
            grid: {
              borderDash: [2],
              borderDashOffset: 2,
              color: "rgba(33, 37, 41, 0.3)",
              borderColor: "rgba(33, 37, 41, 0.3)",
            },
          },
          y: {
            display: true,
            title: {
              display: false,
              text: "Value",
            },
            grid: {
              borderDash: [2],
              drawBorder: false,
              borderDashOffset: 2,
              color: "rgba(33, 37, 41, 0.2)",
              borderColor: "rgba(33, 37, 41, 0.15)",
            },
          },
        },
      },
    };
  }
}

export const lineChartService = LineChartService.getInstance();
