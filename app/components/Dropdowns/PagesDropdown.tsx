import React from "react";
import Link from "next/link";
import { createPopper } from "@popperjs/core";

interface DropdownLink {
  href: string;
  text: string;
}

interface DropdownSection {
  title: string;
  links: DropdownLink[];
}

const DropdownHeader: React.FC<{ title: string }> = ({ title }) => (
  <span className="text-sm pt-2 pb-0 px-4 font-bold block w-full whitespace-nowrap bg-transparent text-blueGray-400">
    {title}
  </span>
);

const DropdownLink: React.FC<DropdownLink> = ({ href, text }) => (
  <Link
    href={href}
    className="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
  >
    {text}
  </Link>
);

const Divider: React.FC = () => (
  <div className="h-0 mx-4 my-2 border border-solid border-blueGray-100" />
);

const PagesDropdown: React.FC = () => {
  const [dropdownPopoverShow, setDropdownPopoverShow] = React.useState<boolean>(false);
  const btnDropdownRef = React.useRef<HTMLAnchorElement>(null);
  const popoverDropdownRef = React.useRef<HTMLDivElement>(null);

  const sections: DropdownSection[] = [
    {
      title: "Admin Layout",
      links: [
        { href: "/admin/dashboard", text: "Dashboard" },
        { href: "/admin/settings", text: "Settings" },
        { href: "/admin/tables", text: "Tables" },
        { href: "/admin/maps", text: "Maps" }
      ]
    },
    {
      title: "Auth Layout",
      links: [
        { href: "/auth/login", text: "Login" },
        { href: "/auth/register", text: "Register" }
      ]
    },
    {
      title: "No Layout",
      links: [
        { href: "/landing", text: "Landing" },
        { href: "/profile", text: "Profile" }
      ]
    }
  ];

  const openDropdownPopover = (): void => {
    if (btnDropdownRef.current && popoverDropdownRef.current) {
      createPopper(btnDropdownRef.current, popoverDropdownRef.current, {
        placement: "bottom-start",
      });
    }
    setDropdownPopoverShow(true);
  };

  const closeDropdownPopover = (): void => {
    setDropdownPopoverShow(false);
  };

  const handleClick = (e: React.MouseEvent<HTMLAnchorElement>): void => {
    e.preventDefault();
    dropdownPopoverShow ? closeDropdownPopover() : openDropdownPopover();
  };

  return (
    <>
      <Link
        href="#pablo"
        ref={btnDropdownRef}
        onClick={handleClick}
        className="lg:text-white lg:hover:text-blueGray-200 text-blueGray-700 px-3 py-4 lg:py-2 flex items-center text-xs uppercase font-bold"
      >
        Demo Pages
      </Link>
      <div
        ref={popoverDropdownRef}
        className={
          (dropdownPopoverShow ? "block " : "hidden ") +
          "bg-white text-base z-50 float-left py-2 list-none text-left rounded shadow-lg min-w-48"
        }
      >
        {sections.map((section, index) => (
          <React.Fragment key={section.title}>
            {index > 0 && <Divider />}
            <DropdownHeader title={section.title} />
            {section.links.map((link) => (
              <DropdownLink key={link.href} {...link} />
            ))}
          </React.Fragment>
        ))}
      </div>
    </>
  );
};

export default PagesDropdown;
