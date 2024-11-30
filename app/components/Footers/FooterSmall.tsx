import React from "react";

interface FooterSmallProps {
  absolute?: boolean;
}

interface FooterLink {
  text: string;
  href: string;
}

const FooterLinkItem: React.FC<FooterLink> = ({ text, href }) => (
  <li>
    <a
      href={href}
      className="text-white hover:text-gray-400 text-sm font-semibold block py-1 px-3"
      target="_blank"
      rel="noopener noreferrer"
    >
      {text}
    </a>
  </li>
);

const FooterSmall: React.FC<FooterSmallProps> = ({ absolute = false }) => {
  const footerLinks: FooterLink[] = [
    { text: "About Us", href: "#" },
    { text: "Privacy Policy", href: "#" },
    { text: "Contact Us", href: "#" }
  ];

  return (
    <>
      <footer
        className={
          (absolute
            ? "absolute w-full bottom-0 bg-gray-900"
            : "relative") + " pb-6"
        }
      >
        <div className="container mx-auto px-4">
          <hr className="mb-6 border-b-1 border-gray-700" />
          <div className="flex flex-wrap items-center md:justify-between justify-center">
            <div className="w-full md:w-4/12 px-4">
              <div className="text-sm text-white font-semibold py-1 text-center md:text-left">
                Copyright {new Date().getFullYear()}{" "}
                <a
                  href="#"
                  className="text-white hover:text-gray-400 text-sm font-semibold py-1"
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

export default FooterSmall;
