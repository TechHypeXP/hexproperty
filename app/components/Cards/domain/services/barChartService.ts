import { ChartConfiguration, ChartDataset } from '../types/chart.types';

export class BarChartService {
  private static instance: BarChartService;

  private constructor() {}

  public static getInstance(): BarChartService {
    if (!BarChartService.instance) {
      BarChartService.instance = new BarChartService();
    }
    return BarChartService.instance;
  }

  public generateDataset(year: number, color: string, data: number[]): ChartDataset {
    return {
      label: year.toString(),
      backgroundColor: color,
      borderColor: color,
      data,
      fill: false,
      barThickness: 8,
    };
  }

  public getConfiguration(currentYearData: number[], previousYearData: number[]): ChartConfiguration {
    const currentYear = new Date().getFullYear();
    
    return {
      type: "bar",
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
          this.generateDataset(currentYear, "#ed64a6", currentYearData),
          this.generateDataset(currentYear - 1, "#4c51bf", previousYearData),
        ],
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
        plugins: {
          title: {
            display: false,
            text: "Orders Chart",
          },
          legend: {
            labels: {
              color: "rgba(0,0,0,.4)",
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
            display: false,
            title: {
              display: true,
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

export const barChartService = BarChartService.getInstance();
