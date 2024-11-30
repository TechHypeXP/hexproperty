import React from "react";
import { createPopper } from "@popperjs/core";

interface NotificationLink {
  text: string;
}

const NotificationLink: React.FC<NotificationLink> = ({ text }) => (
  <a
    href="#pablo"
    className="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
    onClick={(e: React.MouseEvent<HTMLAnchorElement>) => e.preventDefault()}
  >
    {text}
  </a>
);

const Divider: React.FC = () => (
  <div className="h-0 my-2 border border-solid border-blueGray-100" />
);

const NotificationDropdown: React.FC = () => {
  const [dropdownPopoverShow, setDropdownPopoverShow] = React.useState<boolean>(false);
  const btnDropdownRef = React.useRef<HTMLAnchorElement>(null);
  const popoverDropdownRef = React.useRef<HTMLDivElement>(null);

  const notifications: NotificationLink[] = [
    { text: "Action" },
    { text: "Another action" },
    { text: "Something else here" },
    { text: "Seprated link" }
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
      <a
        className="text-blueGray-500 block py-1 px-3"
        href="#pablo"
        ref={btnDropdownRef}
        onClick={handleClick}
      >
        <i className="fas fa-bell"></i>
      </a>
      <div
        ref={popoverDropdownRef}
        className={
          (dropdownPopoverShow ? "block " : "hidden ") +
          "bg-white text-base z-50 float-left py-2 list-none text-left rounded shadow-lg min-w-48"
        }
      >
        {notifications.map((notification, index) => (
          <React.Fragment key={notification.text}>
            {index === 3 && <Divider />}
            <NotificationLink {...notification} />
          </React.Fragment>
        ))}
      </div>
    </>
  );
};

export default NotificationDropdown;
