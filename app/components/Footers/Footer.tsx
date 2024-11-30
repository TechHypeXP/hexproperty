import React from "react";

interface SocialButton {
  icon: string;
  color: string;
}

interface FooterLink {
  text: string;
  href: string;
}

interface FooterSection {
  title: string;
  links: FooterLink[];
}

const SocialButton: React.FC<SocialButton> = ({ icon, color }) => (
  <button
    className={`bg-white text-${color} shadow-lg font-normal h-10 w-10 items-center justify-center align-center rounded-full outline-none focus:outline-none mr-2`}
    type="button"
    aria-label={`Follow us on ${icon.replace('fab fa-', '')}`}
  >
    <i className={icon}></i>
  </button>
);

const FooterLinkItem: React.FC<FooterLink> = ({ text, href }) => (
  <li>
    <a
      className="text-gray-700 hover:text-gray-900 font-semibold block pb-2 text-sm"
      href={href}
      target="_blank"
      rel="noopener noreferrer"
    >
      {text}
    </a>
  </li>
);

const FooterLinkSection: React.FC<FooterSection> = ({ title, links }) => (
  <div className="w-full lg:w-4/12 px-4 ml-auto">
    <span className="block uppercase text-gray-600 text-sm font-semibold mb-2">
      {title}
    </span>
    <ul className="list-unstyled">
      {links.map((link) => (
        <FooterLinkItem key={link.text} {...link} />
      ))}
    </ul>
  </div>
);

const Footer: React.FC = () => {
  const socialButtons: SocialButton[] = [
    { icon: "fab fa-twitter", color: "blue-400" },
    { icon: "fab fa-facebook-square", color: "blue-600" },
    { icon: "fab fa-github", color: "gray-900" }
  ];

  const footerSections: FooterSection[] = [
    {
      title: "Useful Links",
      links: [
        { text: "About Us", href: "#" },
        { text: "Blog", href: "#" },
        { text: "Github", href: "#" }
      ]
    },
    {
      title: "Other Resources",
      links: [
        { text: "Terms & Conditions", href: "#" },
        { text: "Privacy Policy", href: "#" },
        { text: "Contact Us", href: "#" }
      ]
    }
  ];

  return (
    <>
      <footer className="relative bg-gray-300 pt-8 pb-6">
        <div className="container mx-auto px-4">
          <div className="flex flex-wrap text-center lg:text-left">
            <div className="w-full lg:w-6/12 px-4">
              <h4 className="text-3xl font-semibold">HexProperty</h4>
              <h5 className="text-lg mt-0 mb-2 text-gray-700">
                Modern property management solution for landlords and tenants.
              </h5>
              <div className="mt-6 lg:mb-0 mb-6">
                {socialButtons.map((button) => (
                  <SocialButton key={button.icon} {...button} />
                ))}
              </div>
            </div>
            <div className="w-full lg:w-6/12 px-4">
              <div className="flex flex-wrap items-top mb-6">
                {footerSections.map((section) => (
                  <FooterLinkSection key={section.title} {...section} />
                ))}
              </div>
            </div>
          </div>
          <hr className="my-6 border-gray-400" />
          <div className="flex flex-wrap items-center md:justify-between justify-center">
            <div className="w-full md:w-4/12 px-4 mx-auto text-center">
              <div className="text-sm text-gray-600 font-semibold py-1">
                Copyright {new Date().getFullYear()} HexProperty. All rights reserved.
              </div>
            </div>
          </div>
        </div>
      </footer>
    </>
  );
};

export default Footer;
