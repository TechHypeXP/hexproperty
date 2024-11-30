"use client";
import React from "react";

// components
import CardTable from "@/app/components/Cards/CardTable";

export default function Tenants() {
  return (
    <>
      <div className="flex flex-wrap mt-4">
        <div className="w-full mb-12 px-4">
          <CardTable
            title="Tenants"
            headers={["Name", "Property", "Unit", "Lease End", "Status"]}
            data={[
              ["John Smith", "Skyline Apartments", "3A", "2024-06-30", "Active"],
              ["Sarah Johnson", "Ocean View Complex", "2B", "2024-08-15", "Active"],
              ["Mike Brown", "Skyline Apartments", "5C", "2024-03-20", "Notice Given"],
              ["Emma Davis", "City Center Suites", "10D", "2025-01-01", "Active"],
            ]}
          />
        </div>
      </div>
    </>
  );
}
