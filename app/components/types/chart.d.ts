import { Chart as ChartJS, ChartConfiguration } from 'chart.js';

declare module 'chart.js' {
  interface ChartConfiguration {
    type: 'line' | 'bar' | 'radar' | 'doughnut' | 'pie' | 'polarArea' | 'bubble' | 'scatter';
    data: {
      labels: string[];
      datasets: Array<{
        label: string | number;
        data: number[];
        backgroundColor?: string | string[];
        borderColor?: string | string[];
        fill?: boolean;
        barThickness?: number;
        tension?: number;
      }>;
    };
    options: {
      maintainAspectRatio?: boolean;
      responsive?: boolean;
      plugins?: {
        title?: {
          display?: boolean;
          text?: string;
          color?: string;
        };
        legend?: {
          display?: boolean;
          labels?: {
            color?: string;
          };
          align?: 'start' | 'center' | 'end';
          position?: 'top' | 'left' | 'bottom' | 'right';
        };
        tooltip?: {
          mode?: 'point' | 'nearest' | 'index' | 'dataset' | 'x' | 'y';
          intersect?: boolean;
        };
      };
      interaction?: {
        mode?: 'point' | 'nearest' | 'index' | 'dataset' | 'x' | 'y';
        intersect?: boolean;
      };
      scales?: {
        x?: {
          display?: boolean;
          grid?: {
            display?: boolean;
            borderDash?: number[];
            borderDashOffset?: number;
            color?: string;
            borderColor?: string;
          };
          ticks?: {
            color?: string;
          };
          title?: {
            display?: boolean;
            text?: string;
            color?: string;
          };
        };
        y?: {
          display?: boolean;
          grid?: {
            borderDash?: number[];
            borderDashOffset?: number;
            color?: string;
            borderColor?: string;
            drawBorder?: boolean;
          };
          ticks?: {
            color?: string;
          };
          title?: {
            display?: boolean;
            text?: string;
            color?: string;
          };
        };
      };
    };
  }
}

declare global {
  interface Window {
    myBar: ChartJS;
    myLine: ChartJS;
  }
}
