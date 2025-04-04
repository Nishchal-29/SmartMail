export default function Navbar({ onSearch }) {
    return (
      <div className="bg-white shadow px-6 py-3 flex justify-between items-center h-16">
        <h1 className="text-lg font-semibold text-blue-700"> </h1>
        <input
          type="text"
          placeholder="Search emails..."
          onChange={(e) => onSearch(e.target.value)}
          className="border border-gray-300 rounded px-4 py-2 w-[45rem]"
        />
        <button className="bg-[#3869f2] hover:bg-blue-800 text-white px-4 py-2 rounded">
          User ID
        </button>
      </div>
    );
  }