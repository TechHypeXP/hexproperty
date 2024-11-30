import { Chart as ChartJS, registerables } from "chart.js";
import { ChartConfiguration } from "../domain/types/chart.types";

// Register ChartJS components
ChartJS.register(...registerables);

export class ChartApplication {
  private static instance: ChartApplication;
  private charts: Map<string, ChartJS> = new Map();

  private constructor() {}

  public static getInstance(): ChartApplication {
    if (!ChartApplication.instance) {
      ChartApplication.instance = new ChartApplication();
    }
    return ChartApplication.instance;
  }

  public initializeChart(elementId: string, config: ChartConfiguration): void {
    try {
      // Cleanup existing chart if it exists
      this.destroyChart(elementId);

      const canvas = document.getElementById(elementId) as HTMLCanvasElement;
      if (!canvas) {
        throw new Error(`Canvas element with id ${elementId} not found`);
      }

      const context = canvas.getContext("2d");
      if (!context) {
        throw new Error("Failed to get 2D context from canvas");
      }

      const chart = new ChartJS(context, config);
      this.charts.set(elementId, chart);
    } catch (error) {
      console.error("Failed to initialize chart:", error);
      throw error;
    }
  }

  public destroyChart(elementId: string): void {
    const chart = this.charts.get(elementId);
    if (chart) {
      chart.destroy();
      this.charts.delete(elementId);
    }
  }

  public destroyAllCharts(): void {
    this.charts.forEach(chart => chart.destroy());
    this.charts.clear();
  }
}

export const chartApplication = ChartApplication.getInstance();
