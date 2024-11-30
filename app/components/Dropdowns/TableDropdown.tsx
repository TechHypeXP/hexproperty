import React from "react";
import { createPopper } from "@popperjs/core";

interface TableAction {
  text: string;
}

const TableActionLink: React.FC<TableAction> = ({ text }) => (
  <a
    href="#pablo"
    className="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
    onClick={(e: React.MouseEvent<HTMLAnchorElement>) => e.preventDefault()}
  >
    {text}
  </a>
);

const TableDropdown: React.FC = () => {
  const [dropdownPopoverShow, setDropdownPopoverShow] = React.useState<boolean>(false);
  const btnDropdownRef = React.useRef<HTMLAnchorElement>(null);
  const popoverDropdownRef = React.useRef<HTMLDivElement>(null);

  const actions: TableAction[] = [
    { text: "Action" },
    { text: "Another action" },
    { text: "Something else here" }
  ];

  const openDropdownPopover = (): void => {
    if (btnDropdownRef.current && popoverDropdownRef.current) {
      createPopper(btnDropdownRef.current, popoverDropdownRef.current, {
        placement: "left-start",
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
        className="text-blueGray-500 py-1 px-3"
        href="#pablo"
        ref={btnDropdownRef}
        onClick={handleClick}
      >
        <i className="fas fa-ellipsis-v"></i>
      </a>
      <div
        ref={popoverDropdownRef}
        className={
          (dropdownPopoverShow ? "block " : "hidden ") +
          "bg-white text-base z-50 float-left py-2 list-none text-left rounded shadow-lg min-w-48"
        }
      >
        {actions.map((action) => (
          <TableActionLink key={action.text} {...action} />
        ))}
      </div>
    </>
  );
};

export default TableDropdown;
