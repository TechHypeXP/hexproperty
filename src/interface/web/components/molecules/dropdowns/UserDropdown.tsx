import React, { useRef, useState, useEffect } from "react";
import { createPopper, Instance } from "@popperjs/core";
import { User, Settings, LogOut } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

interface UserDropdownProps {
  userName?: string;
  userImage?: string;
  onProfileClick?: () => void;
  onSettingsClick?: () => void;
  onLogoutClick?: () => void;
}

export default function UserDropdown({
  userName = "John Doe",
  userImage = "/img/team-1-800x800.jpg",
  onProfileClick,
  onSettingsClick,
  onLogoutClick,
}: UserDropdownProps) {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const btnRef = useRef<HTMLButtonElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const popperInstance = useRef<Instance | null>(null);

  useEffect(() => {
    if (dropdownOpen && btnRef.current && dropdownRef.current) {
      popperInstance.current = createPopper(btnRef.current, dropdownRef.current, {
        placement: "bottom-end",
        modifiers: [
          {
            name: "offset",
            options: {
              offset: [0, 10],
            },
          },
        ],
      });
    }

    return () => {
      if (popperInstance.current) {
        popperInstance.current.destroy();
        popperInstance.current = null;
      }
    };
  }, [dropdownOpen]);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        btnRef.current &&
        !dropdownRef.current.contains(event.target as Node) &&
        !btnRef.current.contains(event.target as Node)
      ) {
        setDropdownOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const toggleDropdown = () => {
    setDropdownOpen(!dropdownOpen);
  };

  const handleItemClick = (handler?: () => void) => {
    handler?.();
    setDropdownOpen(false);
  };

  return (
    <div className="relative">
      <button
        ref={btnRef}
        className="flex items-center focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 rounded-full"
        onClick={toggleDropdown}
        aria-expanded={dropdownOpen}
        aria-haspopup="true"
        aria-label="User menu"
      >
        <div className="w-12 h-12 relative">
          <Image
            src={userImage}
            alt={userName}
            width={48}
            height={48}
            className="rounded-full object-cover"
            priority
          />
        </div>
      </button>

      <div
        ref={dropdownRef}
        className={`
          ${dropdownOpen ? "opacity-100 visible" : "opacity-0 invisible"}
          transition-all duration-200 ease-in-out
          min-w-[200px] bg-white rounded-lg shadow-lg py-2
          absolute right-0 mt-2 z-50
        `}
      >
        <div className="px-4 py-2 border-b border-gray-100">
          <p className="text-sm font-medium text-gray-900">{userName}</p>
        </div>

        <div className="py-1">
          <button
            onClick={() => handleItemClick(onProfileClick)}
            className="flex w-full items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors duration-150"
          >
            <User className="mr-2 h-4 w-4" />
            Profile
          </button>

          <button
            onClick={() => handleItemClick(onSettingsClick)}
            className="flex w-full items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors duration-150"
          >
            <Settings className="mr-2 h-4 w-4" />
            Settings
          </button>
        </div>

        <div className="border-t border-gray-100">
          <button
            onClick={() => handleItemClick(onLogoutClick)}
            className="flex w-full items-center px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors duration-150"
          >
            <LogOut className="mr-2 h-4 w-4" />
            Logout
          </button>
        </div>
      </div>
    </div>
  );
}
