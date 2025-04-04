export default function Sidebar({ active, onSelect }) {
    const navItems = ["Inbox", "Starred", "Trash"];
  
    return (
      <div className="bg-[#3869f2] text-white w-64 h-full flex flex-col p-4">
        <h2 className="text-2xl font-bold text-center mb-6">SmartMail</h2>
  
        <ul className="space-y-3 flex-1">
          {navItems.map((item) => {
            const isActive = active === item;
  
            return (
              <li
                key={item}
                onClick={() => onSelect(item)}
                className={`cursor-pointer w-full rounded ${
                  isActive
                    ? "bg-white text-[#3869f2] font-semibold"
                    : "hover:bg-blue-600"
                }`}
              >
                <div className="w-full px-4 py-2">
                  {item === "Inbox" && "📥 Inbox"}
                  {item === "Starred" && "⭐ Starred"}
                  {item === "Trash" && "🗑️ Trash"}
                </div>
              </li>
            );
          })}
        </ul>
      </div>
    );
  }