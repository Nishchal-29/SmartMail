import { format, isToday, isYesterday } from "date-fns";

export default function Inbox({ emails, onSelect, onStar, onDelete, onToggleRead }) {
  const grouped = {
    Today: [],
    Yesterday: [],
    Earlier: [],
  };

  emails.forEach((email) => {
    const date = new Date(email.date || Date.now());
    if (isToday(date)) grouped.Today.push(email);
    else if (isYesterday(date)) grouped.Yesterday.push(email);
    else grouped.Earlier.push(email);
  });

  const renderEmail = (email) => {
    const isUnread = !email.read;

    return (
      <li
        key={email.id}
        className={`group relative p-4 border-b cursor-pointer animate-slideIn transition-all duration-300 ease-in-out ${
          isUnread ? "bg-white hover:bg-gray-100" : "bg-gray-50 hover:bg-gray-100"
        }`}
      >
        <div onClick={() => onSelect(email)}>
          <div className="flex items-center gap-2">
            <div
              className={`h-2 w-2 rounded-full ${
                isUnread ? "bg-purple-500" : "bg-transparent"
              }`}
            ></div>
            <div
              className={`${
                isUnread ? "font-bold text-gray-900" : "font-normal text-gray-700"
              }`}
            >
              {email.sender}
            </div>
          </div>
          <div className={isUnread ? "font-medium text-gray-800" : "text-gray-600"}>
            {email.subject}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="absolute right-4 top-1/2 transform -translate-y-1/2 flex gap-3 opacity-0 group-hover:opacity-100">
          <button
            onClick={() => onToggleRead(email.id)}
            title={email.read ? "Mark as Unread" : "Mark as Read"}
            className="text-sm text-gray-500 hover:text-blue-600"
          >
            {email.read ? "📖" : "📩"}
          </button>
          <button
            onClick={() => onStar(email.id)}
            title={email.starred ? "Unstar" : "Star"}
            className={`hover:text-yellow-500 ${
              email.starred ? "text-yellow-500" : "text-gray-400"
            }`}
          >
            ⭐
          </button>
          <button
            onClick={() => onDelete(email.id)}
            title={email.deleted ? "Restore" : "Delete"}
            className={`hover:text-red-500 ${
              email.deleted ? "text-red-500" : "text-gray-400"
            }`}
          >
            🗑️
          </button>
        </div>
      </li>
    );
  };

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Messages</h2>
      {Object.entries(grouped).map(([label, list]) =>
        list.length > 0 ? (
          <div key={label} className="mb-6 animate-fadeIn">
            <h3 className="text-md font-semibold text-gray-600 mb-2">{label}</h3>
            <ul>{list.map(renderEmail)}</ul>
          </div>
        ) : null
      )}
    </div>
  );
}