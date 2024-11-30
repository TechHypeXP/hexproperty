import React from "react";
import { ArrowUpIcon, ArrowDownIcon } from "lucide-react";

interface CardStatsProps {
  statSubtitle: string;
  statTitle: string;
  statArrow: "up" | "down";
  statPercent: string;
  statPercentColor: string;
  statDescription: string;
  icon: React.ReactNode;
  statIconColor: string;
}

export default function CardStats({
  statSubtitle,
  statTitle,
  statArrow,
  statPercent,
  statPercentColor,
  statDescription,
  icon,
  statIconColor,
}: CardStatsProps) {
  return (
    <div className="relative flex flex-col min-w-0 break-words bg-white rounded mb-6 xl:mb-0 shadow-lg">
      <div className="flex-auto p-4">
        <div className="flex flex-wrap">
          <div className="relative w-full pr-4 max-w-full flex-grow flex-1">
            <h5 className="text-blueGray-400 uppercase font-bold text-xs">
              {statSubtitle}
            </h5>
            <span className="font-semibold text-xl text-blueGray-700">
              {statTitle}
            </span>
          </div>
          <div className="relative w-auto pl-4 flex-initial">
            <div
              className={
                "text-white p-3 text-center inline-flex items-center justify-center w-12 h-12 shadow-lg rounded-full " +
                statIconColor
              }
            >
              {icon}
            </div>
          </div>
        </div>
        <p className="text-sm text-blueGray-400 mt-4">
          <span className={statPercentColor + " mr-2"}>
            {statArrow === "up" ? (
              <ArrowUpIcon className="inline w-4 h-4" />
            ) : (
              <ArrowDownIcon className="inline w-4 h-4" />
            )}{" "}
            {statPercent}%
          </span>
          <span className="whitespace-nowrap">{statDescription}</span>
        </p>
      </div>
    </div>
  );
}
