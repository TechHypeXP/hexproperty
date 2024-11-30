import React from "react";

interface MapStyle {
  featureType: string;
  elementType: string;
  stylers: Array<{ [key: string]: string | number }>;
}

interface MapOptions {
  zoom: number;
  center: google.maps.LatLng;
  scrollwheel: boolean;
  zoomControl: boolean;
  styles: MapStyle[];
}

const MapExample: React.FC = () => {
  const mapRef = React.useRef<HTMLDivElement | null>(null);

  React.useEffect(() => {
    if (!mapRef.current || !window.google) return;

    const google = window.google;
    const map = mapRef.current;
    const lat = "40.748817";
    const lng = "-73.985428";
    const myLatlng = new google.maps.LatLng(lat, lng);
    
    const mapOptions: MapOptions = {
      zoom: 12,
      center: myLatlng,
      scrollwheel: false,
      zoomControl: true,
      styles: [
        {
          featureType: "administrative",
          elementType: "labels.text.fill",
          stylers: [{ color: "#444444" }],
        },
        {
          featureType: "landscape",
          elementType: "all",
          stylers: [{ color: "#f2f2f2" }],
        },
        {
          featureType: "poi",
          elementType: "all",
          stylers: [{ visibility: "off" }],
        },
        {
          featureType: "road",
          elementType: "all",
          stylers: [{ saturation: -100 }, { lightness: 45 }],
        },
        {
          featureType: "road.highway",
          elementType: "all",
          stylers: [{ visibility: "simplified" }],
        },
        {
          featureType: "road.arterial",
          elementType: "labels.icon",
          stylers: [{ visibility: "off" }],
        },
        {
          featureType: "transit",
          elementType: "all",
          stylers: [{ visibility: "off" }],
        },
        {
          featureType: "water",
          elementType: "all",
          stylers: [{ color: "#cbd5e0" }, { visibility: "on" }],
        },
      ],
    };

    const googleMap = new google.maps.Map(map, mapOptions);

    const marker = new google.maps.Marker({
      position: myLatlng,
      map: googleMap,
      animation: google.maps.Animation.DROP,
      title: "Notus NextJS!",
    });

    const contentString = `
      <div class="info-window-content">
        <h2>Notus NextJS</h2>
        <p>A free Admin for Tailwind CSS, React, React Hooks, and NextJS.</p>
      </div>
    `;

    const infowindow = new google.maps.InfoWindow({
      content: contentString,
    });

    marker.addListener("click", () => {
      infowindow.open(googleMap, marker);
    });
  }, []);

  return (
    <>
      <div className="relative w-full rounded h-600-px">
        <div className="rounded h-full" ref={mapRef} />
      </div>
    </>
  );
};

// Add Google Maps types to the Window interface
declare global {
  interface Window {
    google: typeof google;
  }
}

export default MapExample;
