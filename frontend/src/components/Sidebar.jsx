export default function Sidebar({ active, onSelect, unreadCount = 0 }) {
    const navItems = [
      { name: "Inbox", icon: "fa-inbox" },
      { name: "Starred", icon: "fa-star" },
      { name: "Trash", icon: "fa-trash" },
      { name: "Sent", icon: "fa-paper-plane" },
    ];
  
    return (
      <div className="bg-[#3869f2] text-white w-64 h-full flex flex-col p-4">
        <h3 className="text-3xl font-bold text-center mb-10 transition-transform hover:scale-105"><i className="fa-solid fa-envelope"></i> InboXpert</h3>
  
        <ul className="space-y-3 flex-1">
          {navItems.map(({ name, icon }) => {
            const isActive = active === name;
            return (
              <li
                key={name}
                onClick={() => onSelect(name)}
                className={`cursor-pointer w-full rounded transition-all duration-300 ${
                  isActive ? "bg-white text-[#3869f2] font-semibold" : "hover:bg-blue-600"
                }`}
              >
                <div className="flex items-center justify-between px-4 py-2 w-full">
                <span className="flex items-center gap-2">
  <i className={`fa-solid ${icon}`}></i>
  {name}
</span>
                  {name === "Inbox" && unreadCount > 0 && (
                    <span className="bg-white text-[#3869f2] text-xs font-bold px-2 py-0.5 rounded-full shadow">
                      {unreadCount}
                    </span>
                  )}
                </div>
              </li>
            );
          })}
        </ul>
      </div>
    );
  }