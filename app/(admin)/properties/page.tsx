"use client";
import React from "react";

// components
import CardTable from "@/components/organisms/Cards/CardTable";

export default function Properties() {
  // Sample data - replace with actual data fetching
  const properties = [
    {
      id: "1",
      name: "Luxury Villa",
      address: "123 Ocean View Dr, Miami, FL",
      type: "Residential",
      status: "Available",
      price: "$2,500,000",
    },
    {
      id: "2",
      name: "Downtown Office",
      address: "456 Business Ave, New York, NY",
      type: "Commercial",
      status: "Rented",
      price: "$5,000/month",
    },
    {
      id: "3",
      name: "Mountain Retreat",
      address: "789 Pine Ridge Rd, Aspen, CO",
      type: "Vacation",
      status: "Available",
      price: "$1,800,000",
    },
  ];

  return (
    <>
      <div className="flex flex-wrap mt-4">
        <div className="w-full mb-12 px-4">
          <CardTable properties={properties} />
        </div>
      </div>
    </>
  );
}
