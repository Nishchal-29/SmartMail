import { useState, useRef, useEffect } from "react";

export default function Navbar({ onSearch, onMenuClick, onSignOut, user }) {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef();

  // Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setDropdownOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="bg-white shadow px-6 py-3 flex justify-between items-center h-16 relative">
      {/* Mobile Menu Button */}
      <button onClick={onMenuClick} className="md:hidden text-2xl mr-4">☰</button>

      {/* Logo */}
      <h1 className="text-lg font-semibold text-blue-700 transition-transform hover:scale-105">
         
      </h1>

      {/* Search */}
      <input
        type="text"
        placeholder="Search emails..."
        onChange={(e) => onSearch(e.target.value)}
        className="border border-gray-300 rounded px-4 py-2 w-[45rem] transition duration-300 hidden md:block"
      />

      {/* User Dropdown */}
      <div className="relative ml-4" ref={dropdownRef}>
        <button
          onClick={() => setDropdownOpen(!dropdownOpen)}
          className="bg-[#3869f2] hover:bg-blue-800 text-white px-4 py-2 rounded transition-all flex items-center gap-2"
        >
          <img
            src={user?.imageUrl}
            alt="User"
            className="w-7 h-7 rounded-full border border-white"
          />
          <span>{user?.name?.split(" ")[0]} ▾</span>
        </button>

        {dropdownOpen && (
          <div className="absolute right-0 mt-2 w-40 bg-white text-gray-800 border rounded shadow-lg z-50 animate-fadeIn">
            <ul className="py-1">
              <li
                onClick={onSignOut}
                className="px-4 py-2 hover:bg-gray-100 cursor-pointer text-sm"
              >
                 Sign Out
              </li>
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}