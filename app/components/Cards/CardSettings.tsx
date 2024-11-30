import React from "react";

interface FormFieldProps {
  label: string;
  type: string;
  defaultValue: string;
  rows?: number;
}

const FormField: React.FC<FormFieldProps> = ({ label, type, defaultValue, rows }) => (
  <div className="relative w-full mb-3">
    <label
      className="block uppercase text-blueGray-600 text-xs font-bold mb-2"
      htmlFor="grid-password"
    >
      {label}
    </label>
    {type === "textarea" ? (
      <textarea
        className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
        rows={rows || 4}
        defaultValue={defaultValue}
      />
    ) : (
      <input
        type={type}
        className="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
        defaultValue={defaultValue}
      />
    )}
  </div>
);

interface UserInfo {
  username: string;
  email: string;
  firstName: string;
  lastName: string;
}

interface ContactInfo {
  address: string;
  city: string;
  country: string;
  postalCode: string;
}

interface AboutInfo {
  aboutMe: string;
}

interface CardSettingsProps {
  initialUserInfo?: UserInfo;
  initialContactInfo?: ContactInfo;
  initialAboutInfo?: AboutInfo;
}

const defaultUserInfo: UserInfo = {
  username: "lucky.jesse",
  email: "jesse@example.com",
  firstName: "Lucky",
  lastName: "Jesse"
};

const defaultContactInfo: ContactInfo = {
  address: "Bld Mihail Kogalniceanu, nr. 8 Bl 1, Sc 1, Ap 09",
  city: "New York",
  country: "United States",
  postalCode: "Postal Code"
};

const defaultAboutInfo: AboutInfo = {
  aboutMe: "A beautiful UI Kit and Admin for NextJS & Tailwind CSS. It is Free and Open Source."
};

const CardSettings: React.FC<CardSettingsProps> = ({
  initialUserInfo = defaultUserInfo,
  initialContactInfo = defaultContactInfo,
  initialAboutInfo = defaultAboutInfo
}) => {
  const handleSettingsClick = React.useCallback(() => {
    // Handle settings button click
    console.log("Settings clicked");
  }, []);

  return (
    <>
      <div className="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-blueGray-100 border-0">
        <div className="rounded-t bg-white mb-0 px-6 py-6">
          <div className="text-center flex justify-between">
            <h6 className="text-blueGray-700 text-xl font-bold">My account</h6>
            <button
              className="bg-blueGray-700 active:bg-blueGray-600 text-white font-bold uppercase text-xs px-4 py-2 rounded shadow hover:shadow-md outline-none focus:outline-none mr-1 ease-linear transition-all duration-150"
              type="button"
              onClick={handleSettingsClick}
            >
              Settings
            </button>
          </div>
        </div>
        <div className="flex-auto px-4 lg:px-10 py-10 pt-0">
          <form>
            <h6 className="text-blueGray-400 text-sm mt-3 mb-6 font-bold uppercase">
              User Information
            </h6>
            <div className="flex flex-wrap">
              <div className="w-full lg:w-6/12 px-4">
                <FormField
                  label="Username"
                  type="text"
                  defaultValue={initialUserInfo.username}
                />
              </div>
              <div className="w-full lg:w-6/12 px-4">
                <FormField
                  label="Email address"
                  type="email"
                  defaultValue={initialUserInfo.email}
                />
              </div>
              <div className="w-full lg:w-6/12 px-4">
                <FormField
                  label="First Name"
                  type="text"
                  defaultValue={initialUserInfo.firstName}
                />
              </div>
              <div className="w-full lg:w-6/12 px-4">
                <FormField
                  label="Last Name"
                  type="text"
                  defaultValue={initialUserInfo.lastName}
                />
              </div>
            </div>

            <hr className="mt-6 border-b-1 border-blueGray-300" />

            <h6 className="text-blueGray-400 text-sm mt-3 mb-6 font-bold uppercase">
              Contact Information
            </h6>
            <div className="flex flex-wrap">
              <div className="w-full lg:w-12/12 px-4">
                <FormField
                  label="Address"
                  type="text"
                  defaultValue={initialContactInfo.address}
                />
              </div>
              <div className="w-full lg:w-4/12 px-4">
                <FormField
                  label="City"
                  type="text"
                  defaultValue={initialContactInfo.city}
                />
              </div>
              <div className="w-full lg:w-4/12 px-4">
                <FormField
                  label="Country"
                  type="text"
                  defaultValue={initialContactInfo.country}
                />
              </div>
              <div className="w-full lg:w-4/12 px-4">
                <FormField
                  label="Postal Code"
                  type="text"
                  defaultValue={initialContactInfo.postalCode}
                />
              </div>
            </div>

            <hr className="mt-6 border-b-1 border-blueGray-300" />

            <h6 className="text-blueGray-400 text-sm mt-3 mb-6 font-bold uppercase">
              About Me
            </h6>
            <div className="flex flex-wrap">
              <div className="w-full lg:w-12/12 px-4">
                <FormField
                  label="About me"
                  type="textarea"
                  defaultValue={initialAboutInfo.aboutMe}
                  rows={4}
                />
              </div>
            </div>
          </form>
        </div>
      </div>
    </>
  );
};

export default CardSettings;
