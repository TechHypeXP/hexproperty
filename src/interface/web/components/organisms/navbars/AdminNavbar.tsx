import { Menu, Search } from 'lucide-react';
import Link from 'next/link';
import React, { useState } from 'react';
import UserDropdown from '@/interface/web/components/molecules/dropdowns/UserDropdown';

interface AdminNavbarProps {
  onSearch?: (query: string) => void;
  onProfileClick?: () => void;
  onSettingsClick?: () => void;
  onLogoutClick?: () => void;
  userName?: string;
  userImage?: string;
}

export default function AdminNavbar({ 
  onSearch,
  onProfileClick,
  onSettingsClick,
  onLogoutClick,
  userName,
  userImage,
}: AdminNavbarProps) {
  const [navbarOpen, setNavbarOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSearch?.(searchQuery);
  };

  return (
    <>
      {/* Navbar */}
      <nav className="absolute top-0 left-0 w-full z-10 bg-transparent md:flex-row md:flex-nowrap md:justify-start flex items-center p-4">
        <div className="w-full mx-auto items-center flex justify-between md:flex-nowrap flex-wrap md:px-10 px-4">
          {/* Brand */}
          <Link
            className="text-white text-sm uppercase hidden lg:inline-block font-semibold"
            href="/dashboard"
          >
            Dashboard
          </Link>
          {/* Form */}
          <form 
            onSubmit={handleSearch}
            className="md:flex hidden flex-row flex-wrap items-center lg:ml-auto mr-3"
          >
            <div className="relative flex w-full flex-wrap items-stretch">
              <span className="z-10 h-full leading-snug font-normal absolute text-center text-blueGray-300 absolute bg-transparent rounded text-base items-center justify-center w-8 pl-3 py-3">
                <Search className="w-5 h-5 text-gray-300" />
              </span>
              <input
                type="text"
                placeholder="Search here..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 relative bg-white rounded text-sm shadow outline-none focus:outline-none focus:ring w-full pl-10"
              />
            </div>
          </form>
          {/* User */}
          <ul className="flex-col md:flex-row list-none items-center hidden md:flex">
            <UserDropdown
              userName={userName}
              userImage={userImage}
              onProfileClick={onProfileClick}
              onSettingsClick={onSettingsClick}
              onLogoutClick={onLogoutClick}
            />
          </ul>
          {/* Mobile menu button */}
          <button
            type="button"
            className="cursor-pointer text-white md:hidden px-3 py-1 text-xl leading-none bg-transparent rounded border border-solid border-transparent"
            onClick={() => setNavbarOpen(!navbarOpen)}
            aria-label="Toggle navigation menu"
          >
            <Menu className="w-6 h-6" />
          </button>
          {/* Mobile menu */}
          <div
            className={`
              md:hidden fixed inset-0 z-40 bg-white transform transition-transform duration-300 ease-in-out
              ${navbarOpen ? 'translate-x-0' : '-translate-x-full'}
            `}
          >
            <div className="flex items-center justify-between p-4 border-b">
              <Link
                href="/"
                className="text-gray-800 text-xl font-semibold"
                onClick={() => setNavbarOpen(false)}
              >
                HexProperty
              </Link>
              <button
                type="button"
                className="text-gray-600 hover:text-gray-900"
                onClick={() => setNavbarOpen(false)}
                aria-label="Close menu"
              >
                <span className="text-2xl">&times;</span>
              </button>
            </div>
            <div className="p-4">
              <form onSubmit={handleSearch} className="mb-4">
                <div className="relative">
                  <span className="absolute inset-y-0 left-0 flex items-center pl-3">
                    <Search className="w-5 h-5 text-gray-400" />
                  </span>
                  <input
                    type="text"
                    placeholder="Search here..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </form>
              <nav className="space-y-4">
                <Link
                  href="/dashboard"
                  className="block text-gray-600 hover:text-gray-900"
                  onClick={() => setNavbarOpen(false)}
                >
                  Dashboard
                </Link>
                <Link
                  href="/properties"
                  className="block text-gray-600 hover:text-gray-900"
                  onClick={() => setNavbarOpen(false)}
                >
                  Properties
                </Link>
                <Link
                  href="/tenants"
                  className="block text-gray-600 hover:text-gray-900"
                  onClick={() => setNavbarOpen(false)}
                >
                  Tenants
                </Link>
              </nav>
            </div>
          </div>
        </div>
      </nav>
    </>
  );
}
