import React from "react";
import Link from "next/link";
import { createPopper, Instance, Placement } from "@popperjs/core";

interface UserAction {
  text: string;
  divider?: boolean;
  onClick?: () => void;
  href?: string;
}

interface UserActionLinkProps extends UserAction {
  className?: string;
}

const UserActionLink: React.FC<UserActionLinkProps> = ({ text, href, onClick, className = "" }) => (
  <Link
    href={href}
    className={`text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700 hover:bg-blueGray-100 ${className}`}
    onClick={(e: React.MouseEvent<HTMLAnchorElement>) => {
      e.preventDefault();
      onClick?.();
    }}
  >
    {text}
  </Link>
);

const Divider: React.FC = () => (
  <div className="h-0 my-2 border border-solid border-blueGray-100" role="separator" />
);

interface UserDropdownProps {
  imageUrl?: string;
  altText?: string;
}

const UserDropdown: React.FC<UserDropdownProps> = ({ 
  imageUrl = "/img/team-1-800x800.jpg",
  altText = "User profile"
}) => {
  const [dropdownPopoverShow, setDropdownPopoverShow] = React.useState<boolean>(false);
  const btnDropdownRef = React.useRef<HTMLAnchorElement>(null);
  const popoverDropdownRef = React.useRef<HTMLDivElement>(null);
  const [popperInstance, setPopperInstance] = React.useState<Instance | null>(null);

  const actions: UserAction[] = [
    { text: "Action", href: "/admin/dashboard" },
    { text: "Another action", href: "/admin/settings" },
    { text: "Something else here", href: "/admin/something" },
    { text: "Separated link", divider: true, href: "/admin/separated" }
  ];

  const openDropdownPopover = (): void => {
    if (btnDropdownRef.current && popoverDropdownRef.current) {
      const instance = createPopper(btnDropdownRef.current, popoverDropdownRef.current, {
        placement: "bottom-start" as Placement,
        modifiers: [
          {
            name: 'offset',
            options: {
              offset: [0, 10],
            },
          },
        ],
      });
      setPopperInstance(instance);
    }
    setDropdownPopoverShow(true);
  };

  const closeDropdownPopover = (): void => {
    popperInstance?.destroy();
    setPopperInstance(null);
    setDropdownPopoverShow(false);
  };

  const handleClick = (e: React.MouseEvent<HTMLAnchorElement>): void => {
    e.preventDefault();
    dropdownPopoverShow ? closeDropdownPopover() : openDropdownPopover();
  };

  React.useEffect(() => {
    const handleClickOutside = (event: MouseEvent): void => {
      if (
        dropdownPopoverShow &&
        btnDropdownRef.current &&
        popoverDropdownRef.current &&
        !btnDropdownRef.current.contains(event.target as Node) &&
        !popoverDropdownRef.current.contains(event.target as Node)
      ) {
        closeDropdownPopover();
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [dropdownPopoverShow]);

  return (
    <>
      <div
        className="items-center flex"
        ref={btnDropdownRef}
        onClick={handleClick}
        aria-expanded={dropdownPopoverShow}
        aria-haspopup="true"
      >
        <span className="w-12 h-12 text-sm text-white bg-blueGray-200 inline-flex items-center justify-center rounded-full">
          <img
            alt={altText}
            className="w-full rounded-full align-middle border-none shadow-lg"
            src={imageUrl}
          />
        </span>
      </div>
      <div
        ref={popoverDropdownRef}
        className={
          (dropdownPopoverShow ? "block " : "hidden ") +
          "bg-white text-base z-50 float-left py-2 list-none text-left rounded shadow-lg min-w-48"
        }
        role="menu"
        aria-orientation="vertical"
        aria-labelledby="user-menu"
      >
        {actions.map((action, index) => (
          <React.Fragment key={`${action.text}-${index}`}>
            {action.divider && <Divider />}
            <UserActionLink {...action} />
          </React.Fragment>
        ))}
      </div>
    </>
  );
};

export default UserDropdown;
