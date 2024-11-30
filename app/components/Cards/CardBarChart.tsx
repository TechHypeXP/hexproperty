import React, { useEffect } from "react";
import { chartApplication } from "./application/chartApplication";
import { barChartService } from "./domain/services/barChartService";

const CHART_ID = "bar-chart";

/**
 * CardBarChart component displays a bar chart comparing order data between current and previous year.
 * Implements hexagonal architecture with proper cleanup and error handling.
 */
export default function CardBarChart(): React.ReactElement {
  useEffect(() => {
    try {
      // Sample data - in a real application, this would come from an API or props
      const currentYearData = [30, 78, 56, 34, 100, 45, 13];
      const previousYearData = [27, 68, 86, 74, 10, 4, 87];

      const config = barChartService.getConfiguration(currentYearData, previousYearData);
      chartApplication.initializeChart(CHART_ID, config);

      // Cleanup function
      return () => {
        chartApplication.destroyChart(CHART_ID);
      };
    } catch (error) {
      console.error("Failed to initialize bar chart:", error);
      // In a real application, we would handle this error appropriately
      // e.g., showing an error message to the user or falling back to a default view
    }
  }, []);

  return (
    <div className="relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-lg rounded">
      <div className="rounded-t mb-0 px-4 py-3 bg-transparent">
        <div className="flex flex-wrap items-center">
          <div className="relative w-full max-w-full flex-grow flex-1">
            <h6 className="uppercase text-blueGray-400 mb-1 text-xs font-semibold">
              Performance
            </h6>
            <h2 className="text-blueGray-700 text-xl font-semibold">
              Total orders
            </h2>
          </div>
        </div>
      </div>
      <div className="p-4 flex-auto">
        {/* Chart */}
        <div className="relative h-350-px">
          <canvas id={CHART_ID}></canvas>
        </div>
      </div>
    </div>
  );
}
