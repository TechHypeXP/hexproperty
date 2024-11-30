import React from "react";

interface ProfileStats {
  count: number;
  label: string;
}

interface ProfileData {
  name: string;
  location: string;
  position: string;
  education: string;
  bio: string;
  imageSrc: string;
  stats: ProfileStats[];
}

const profileData: ProfileData = {
  name: "Jenna Stones",
  location: "Los Angeles, California",
  position: "Solution Manager - Creative Tim Officer",
  education: "University of Computer Science",
  bio: "An artist of considerable range, Jenna the name taken by Melbourne-raised, Brooklyn-based Nick Murphy writes, performs and records all of his own music, giving it a warm, intimate feel with a solid groove structure. An artist of considerable range.",
  imageSrc: "/img/team-2-800x800.jpg",
  stats: [
    { count: 22, label: "Friends" },
    { count: 10, label: "Photos" },
    { count: 89, label: "Comments" }
  ]
};

export default function CardProfile(): JSX.Element {
  const handleShowMore = (e: React.MouseEvent<HTMLAnchorElement>): void => {
    e.preventDefault();
  };

  return (
    <>
      <div className="relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-xl rounded-lg mt-16">
        <div className="px-6">
          <div className="flex flex-wrap justify-center">
            <div className="w-full px-4 flex justify-center">
              <div className="relative">
                <img
                  alt="Profile"
                  src={profileData.imageSrc}
                  className="shadow-xl rounded-full h-auto align-middle border-none absolute -m-16 -ml-20 lg:-ml-16 max-w-150-px"
                />
              </div>
            </div>
            <div className="w-full px-4 text-center mt-20">
              <div className="flex justify-center py-4 lg:pt-4 pt-8">
                {profileData.stats.map((stat, index) => (
                  <div key={index} className={`${index < profileData.stats.length - 1 ? 'mr-4 ' : 'lg:mr-4 '}p-3 text-center`}>
                    <span className="text-xl font-bold block uppercase tracking-wide text-blueGray-600">
                      {stat.count}
                    </span>
                    <span className="text-sm text-blueGray-400">{stat.label}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
          <div className="text-center mt-12">
            <h3 className="text-xl font-semibold leading-normal mb-2 text-blueGray-700 mb-2">
              {profileData.name}
            </h3>
            <div className="text-sm leading-normal mt-0 mb-2 text-blueGray-400 font-bold uppercase">
              <i className="fas fa-map-marker-alt mr-2 text-lg text-blueGray-400"></i>{" "}
              {profileData.location}
            </div>
            <div className="mb-2 text-blueGray-600 mt-10">
              <i className="fas fa-briefcase mr-2 text-lg text-blueGray-400"></i>
              {profileData.position}
            </div>
            <div className="mb-2 text-blueGray-600">
              <i className="fas fa-university mr-2 text-lg text-blueGray-400"></i>
              {profileData.education}
            </div>
          </div>
          <div className="mt-10 py-10 border-t border-blueGray-200 text-center">
            <div className="flex flex-wrap justify-center">
              <div className="w-full lg:w-9/12 px-4">
                <p className="mb-4 text-lg leading-relaxed text-blueGray-700">
                  {profileData.bio}
                </p>
                <a
                  href="#pablo"
                  className="font-normal text-lightBlue-500"
                  onClick={handleShowMore}
                >
                  Show more
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
