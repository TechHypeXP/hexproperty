import React from "react";

interface FooterLink {
  text: string;
  href: string;
}

const FooterLinkItem: React.FC<FooterLink> = ({ text, href }) => (
  <li>
    <a
      href={href}
      className="text-gray-700 hover:text-gray-900 text-sm font-semibold block py-1 px-3"
    >
      {text}
    </a>
  </li>
);

const FooterAdmin: React.FC = () => {
  const footerLinks: FooterLink[] = [
    { text: "About Us", href: "#" },
    { text: "Blog", href: "#" },
    { text: "Contact", href: "#" }
  ];

  return (
    <>
      <footer className="block py-4">
        <div className="container mx-auto px-4">
          <hr className="mb-4 border-b-1 border-gray-300" />
          <div className="flex flex-wrap items-center md:justify-between justify-center">
            <div className="w-full md:w-4/12 px-4">
              <div className="text-sm text-gray-600 font-semibold py-1 text-center md:text-left">
                Copyright {new Date().getFullYear()}{" "}
                <a
                  href="#"
                  className="text-gray-600 hover:text-gray-800 text-sm font-semibold py-1"
                >
                  HexProperty
                </a>
              </div>
            </div>
            <div className="w-full md:w-8/12 px-4">
              <ul className="flex flex-wrap list-none md:justify-end justify-center">
                {footerLinks.map((link) => (
                  <FooterLinkItem key={link.text} {...link} />
                ))}
              </ul>
            </div>
          </div>
        </div>
      </footer>
    </>
  );
};

export default FooterAdmin;
