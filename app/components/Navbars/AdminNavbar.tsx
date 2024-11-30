import React from "react";
import UserDropdown from "../Dropdowns/UserDropdown";
import Link from "next/link";

interface SearchInputProps {
  placeholder: string;
}

const SearchInput: React.FC<SearchInputProps> = ({ placeholder }) => (
  <div className="relative flex w-full flex-wrap items-stretch">
    <span className="z-10 h-full leading-snug font-normal absolute text-center text-gray-300 bg-transparent rounded text-base items-center justify-center w-8 pl-3 py-3">
      <i className="fas fa-search"></i>
    </span>
    <input
      type="text"
      placeholder={placeholder}
      className="border-0 px-3 py-3 placeholder-gray-300 text-gray-600 relative bg-white rounded text-sm shadow outline-none focus:outline-none focus:ring w-full pl-10"
    />
  </div>
);

export default function AdminNavbar() {
  return (
    <>
      <nav className="absolute top-0 left-0 w-full z-10 bg-transparent md:flex-row md:flex-nowrap md:justify-start flex items-center p-4">
        <div className="w-full mx-auto items-center flex justify-between md:flex-nowrap flex-wrap md:px-10 px-4">
          <Link
            href="/"
            className="text-white text-sm uppercase hidden lg:inline-block font-semibold"
          >
            Dashboard
          </Link>
          <form className="md:flex hidden flex-row flex-wrap items-center lg:ml-auto mr-3">
            <div className="relative flex w-full flex-wrap items-stretch">
              <SearchInput placeholder="Search here..." />
            </div>
          </form>
          <ul className="flex-col md:flex-row list-none items-center hidden md:flex">
            <UserDropdown />
          </ul>
        </div>
      </nav>
    </>
  );
}
