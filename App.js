// ✅ App.js (React Frontend using OpenStreetMap + Leaflet markers)
import React, { useState } from "react";
import axios from "axios";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

import iconUrl from "leaflet/dist/images/marker-icon.png";
import iconShadow from "leaflet/dist/images/marker-shadow.png";

let DefaultIcon = L.icon({
  iconUrl,
  shadowUrl: iconShadow,
});
L.Marker.prototype.options.icon = DefaultIcon;

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [center, setCenter] = useState({ lat: 13.0827, lng: 80.2707 });

  const handleSearch = async () => {
    if (!query.trim()) {
      alert("Please enter a search term.");
      return;
    }

    setLoading(true);
    setResults([]);

    try {
      const response = await axios.post("http://localhost:5000/scrape", {
        query,
      });

      const data = response.data;
      setResults(data);

      if (data.length > 0 && data[0].lat && data[0].lng) {
        setCenter({ lat: data[0].lat, lng: data[0].lng });
      }
    } catch (error) {
      console.error("Error fetching data", error);
      alert("Something went wrong. Try again!");
    }

    setLoading(false);
  };

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">
        📍 <strong>Google Maps Scraper with OpenStreetMap</strong>
      </h2>

      <div className="input-group mb-4 justify-content-center">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="form-control w-50"
          placeholder="e.g. gyms in Coimbatore"
        />
        <button className="btn btn-success" onClick={handleSearch}>
          🔍 Search
        </button>
      </div>

      {loading && <p className="text-center text-muted">Scraping results...</p>}

      {results.length > 0 && (
        <>
          <div className="table-responsive mb-4">
            <table className="table table-bordered table-striped">
              <thead className="table-dark">
                <tr>
                  <th>Name</th>
                  <th>Address</th>
                  <th>Phone</th>
                  <th>Rating</th>
                  <th>Reviews</th>
                </tr>
              </thead>
              <tbody>
                {results.map((item, index) => (
                  <tr key={index}>
                    <td>{item.name}</td>
                    <td>{item.address}</td>
                    <td>{item.phone}</td>
                    <td>{item.rating}</td>
                    <td>{item.reviews}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="mb-5">
            <MapContainer
              center={[center.lat, center.lng]}
              zoom={13}
              style={{ height: "500px", width: "100%" }}
              scrollWheelZoom={true}
            >
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
              />
              {results.map((item, index) => (
                item.lat && item.lng && (
                  <Marker key={index} position={[item.lat, item.lng]}>
                    <Popup>
                      <strong>{item.name}</strong>
                      <br />
                      {item.address}<br />
                      {item.phone && <>📞 {item.phone}<br /></>}
                      {item.rating && <>⭐ {item.rating}<br /></>}
                      {item.reviews && <>📝 {item.reviews}</>}
                    </Popup>
                  </Marker>
                )
              ))}
            </MapContainer>
          </div>
        </>
      )}
    </div>
  );
}

export default App;
