import React from "react";
import Link from "next/link";

interface DropdownLink {
  href: string;
  text: string;
}

interface DropdownSection {
  title: string;
  links: DropdownLink[];
}

const DropdownHeader: React.FC<{ title: string }> = ({ title }) => (
  <span className="text-sm pt-2 pb-0 px-4 font-bold block w-full whitespace-nowrap bg-transparent text-gray-500">
    {title}
  </span>
);

const DropdownLink: React.FC<DropdownLink> = ({ href, text }) => (
  <Link
    href={href}
    className="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-gray-800"
  >
    {text}
  </Link>
);

const Divider: React.FC = () => (
  <div className="h-0 mx-4 my-2 border border-solid border-gray-200" />
);

const IndexDropdown: React.FC = () => {
  const [dropdownPopoverShow, setDropdownPopoverShow] = React.useState(false);

  const toggleDropdown = (e: React.MouseEvent) => {
    e.preventDefault();
    setDropdownPopoverShow(!dropdownPopoverShow);
  };

  const sections: DropdownSection[] = [
    {
      title: "Properties",
      links: [
        { href: "/admin/dashboard", text: "Dashboard" },
        { href: "/admin/settings", text: "Settings" },
      ]
    },
    {
      title: "Auth",
      links: [
        { href: "/auth/login", text: "Login" },
        { href: "/auth/register", text: "Register" }
      ]
    }
  ];

  return (
    <>
      <a
        className="hover:text-gray-600 text-gray-800 px-3 py-4 lg:py-2 flex items-center text-xs uppercase font-bold"
        href="#"
        onClick={toggleDropdown}
      >
        Menu <i className="fas fa-chevron-down ml-1"></i>
      </a>
      <div
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

export default IndexDropdown;
