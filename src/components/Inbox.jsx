export default function Inbox({ emails, onSelect, onStar, onDelete }) {
    return (
      <div>
        <h2 className="text-xl font-bold mb-4">Messages</h2>
        <ul>
          {emails.map((email) => (
            <li
              key={email.id}
              className="p-4 border-b hover:bg-gray-100 group relative"
            >
              <div onClick={() => onSelect(email)} className="cursor-pointer">
                <div className="font-semibold">{email.sender}</div>
                <div className="text-gray-600">{email.subject}</div>
              </div>
  
              <div className="absolute right-4 top-1/2 transform -translate-y-1/2 flex gap-3 opacity-0 group-hover:opacity-100">
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
          ))}
        </ul>
      </div>
    );
  }