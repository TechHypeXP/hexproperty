import React, { ReactNode } from "react";

// components

import AdminNavbar from "components/Navbars/AdminNavbar.tsx";
import Sidebar from "components/Sidebar/Sidebar.tsx";
import HeaderStats from "components/Headers/HeaderStats.tsx";
import FooterAdmin from "components/Footers/FooterAdmin.tsx";

interface AdminLayoutProps {
  children: ReactNode;
}

const Admin: React.FC<AdminLayoutProps> = ({ children }) => {
  return (
    <>
      <Sidebar />
      <div className="relative md:ml-64 bg-blueGray-100">
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
};

export default Admin;
