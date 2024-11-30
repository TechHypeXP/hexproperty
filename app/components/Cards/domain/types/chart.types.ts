import { 
  ChartConfiguration as ChartJSConfig, 
  ChartTypeRegistry,
  ChartOptions as ChartJSOptions,
  GridLineOptions
} from "chart.js";

export type ChartPosition = "bottom" | "left" | "right" | "top" | "center" | "chartArea";
export type ChartMode = "index" | "nearest" | "x" | "y" | "dataset" | "point";

export interface ChartDataset {
  label: string;
  backgroundColor: string;
  borderColor: string;
  data: number[];
  fill: boolean;
  barThickness?: number;
  tension?: number;
}

export interface CustomGridConfig {
  display?: boolean;
  drawBorder?: boolean;
  color?: string;
  borderColor?: string;
  dash?: number[];
  dashOffset?: number;
}

export interface CustomScaleConfig {
  display?: boolean;
  title?: {
    display: boolean;
    text: string;
  };
  grid?: Partial<GridLineOptions>;
}

export interface CustomChartPlugins {
  title?: {
    display?: boolean;
    text?: string;
  };
  legend?: {
    labels?: {
      color?: string;
    };
    align?: "start" | "end" | "center";
    position?: ChartPosition;
  };
  tooltip?: {
    mode?: ChartMode;
    intersect?: boolean;
  };
}

export interface CustomChartOptions extends ChartJSOptions<keyof ChartTypeRegistry> {
  maintainAspectRatio?: boolean;
  responsive?: boolean;
  plugins?: CustomChartPlugins;
  interaction?: {
    mode?: ChartMode;
    intersect?: boolean;
  };
  scales?: {
    x?: CustomScaleConfig;
    y?: CustomScaleConfig;
  };
}

export interface BaseChartConfiguration {
  type: keyof ChartTypeRegistry;
  data: {
    labels: string[];
    datasets: ChartDataset[];
  };
  options: CustomChartOptions;
}

// Create a type that combines our base configuration with Chart.js types
export type ChartConfiguration = BaseChartConfiguration & Omit<ChartJSConfig<keyof ChartTypeRegistry, number[], string>, 'type' | 'data' | 'options'>;

// Type guard to ensure chart configuration is valid
export function isValidChartConfiguration(config: unknown): config is ChartConfiguration {
  const conf = config as ChartConfiguration;
  return (
    typeof conf === "object" &&
    conf !== null &&
    typeof conf.type === "string" &&
    typeof conf.data === "object" &&
    Array.isArray(conf.data.datasets) &&
    typeof conf.options === "object"
  );
}
