"use client";
import React from "react";

// components
import AdminNavbar from "@/components/organisms/Navbars/AdminNavbar";
import Sidebar from "@/components/organisms/Sidebar/Sidebar";
import HeaderStats from "@/components/organisms/Headers/HeaderStats";
import FooterAdmin from "@/components/organisms/Footers/FooterAdmin";

export default function Admin({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Sidebar />
      <div className="relative md:ml-64 bg-gray-200">
        <AdminNavbar />
        {/* Header */}
        <HeaderStats />
        <div className="px-4 md:px-10 mx-auto w-full -m-24">
          {children}
          <FooterAdmin />
        </div>
      </div>
    </>
  );
}
