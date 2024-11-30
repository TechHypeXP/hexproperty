import React from "react";
import Link from "next/link";
import PagesDropdown from "../Dropdowns/PagesDropdown";

interface SocialLink {
  href: string;
  icon: string;
  label: string;
}

const SocialLink: React.FC<SocialLink> = ({ href, icon, label }) => (
  <a
    className="lg:text-white lg:hover:text-gray-200 text-gray-700 px-3 py-4 lg:py-2 flex items-center text-xs uppercase font-bold"
    href={href}
    target="_blank"
    rel="noopener noreferrer"
  >
    <i className={`lg:text-gray-200 text-gray-400 ${icon} text-lg leading-lg`} />
    <span className="lg:hidden inline-block ml-2">{label}</span>
  </a>
);

export default function AuthNavbar() {
  const [navbarOpen, setNavbarOpen] = React.useState(false);

  const socialLinks: SocialLink[] = [
    {
      href: "https://github.com/hexproperty",
      icon: "fab fa-github",
      label: "Github",
    },
    {
      href: "https://twitter.com/hexproperty",
      icon: "fab fa-twitter",
      label: "Tweet",
    },
  ];

  return (
    <>
      <nav className="top-0 absolute z-50 w-full flex flex-wrap items-center justify-between px-2 py-3 navbar-expand-lg">
        <div className="container px-4 mx-auto flex flex-wrap items-center justify-between">
          <div className="w-full relative flex justify-between lg:w-auto lg:static lg:block lg:justify-start">
            <Link
              href="/"
              className="text-white text-sm font-bold leading-relaxed inline-block mr-4 py-2 whitespace-nowrap uppercase"
            >
              HexProperty
            </Link>
            <button
              className="cursor-pointer text-xl leading-none px-3 py-1 border border-solid border-transparent rounded bg-transparent block lg:hidden outline-none focus:outline-none"
              type="button"
              onClick={() => setNavbarOpen(!navbarOpen)}
            >
              <i className="text-white fas fa-bars"></i>
            </button>
          </div>
          <div
            className={
              "lg:flex flex-grow items-center bg-white lg:bg-opacity-0 lg:shadow-none" +
              (navbarOpen ? " block rounded shadow-lg" : " hidden")
            }
          >
            <ul className="flex flex-col lg:flex-row list-none mr-auto">
              <li className="flex items-center">
                <a
                  className="lg:text-white lg:hover:text-gray-200 text-gray-700 px-3 py-4 lg:py-2 flex items-center text-xs uppercase font-bold"
                  href="#"
                >
                  <i className="lg:text-gray-200 text-gray-400 far fa-file-alt text-lg leading-lg mr-2" />{" "}
                  Docs
                </a>
              </li>
            </ul>
            <ul className="flex flex-col lg:flex-row list-none lg:ml-auto">
              {socialLinks.map((link) => (
                <li className="flex items-center" key={link.label}>
                  <SocialLink {...link} />
                </li>
              ))}
              <li className="flex items-center">
                <button
                  className="bg-white text-gray-800 active:bg-gray-100 text-xs font-bold uppercase px-4 py-2 rounded shadow hover:shadow-md outline-none focus:outline-none lg:mr-1 lg:mb-0 ml-3 mb-3"
                  type="button"
                  style={{ transition: "all .15s ease" }}
                >
                  <i className="fas fa-arrow-alt-circle-right"></i> Get Started
                </button>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </>
  );
}
