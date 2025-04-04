import { useState } from 'react';

export default function EmailDetail({ email, onBack, onReply }) {
  const [simplified, setSimplified] = useState("");

  const handleSimplify = () => {
    const simple = email.body.length > 60
      ? email.body.slice(0, 60) + "..."
      : email.body;
    setSimplified(simple);
  };

  return (
    <div className="flex flex-col h-full">
      <div>
        <button onClick={onBack} className="text-blue-600 mb-4">&larr; Back</button>
        <h2 className="text-2xl font-bold mb-2">{email.subject}</h2>
        <p className="text-sm text-gray-500 mb-4">From: {email.sender}</p>
        <p className="text-gray-800 mb-6">{email.body}</p>

        {simplified && (
          <div className="bg-yellow-100 p-4 rounded mb-6">
            <strong>Simplified:</strong> {simplified}
          </div>
        )}
      </div>

      {/* Button group fixed to bottom */}
      <div className="mt-auto pt-6 flex gap-3">
        <button
          onClick={() => onReply(email)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
        >
          Reply
        </button>
        <button
          onClick={() => alert("Prompt-based reply coming soon...")}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
        >
          Prompt-Based Reply
        </button>
        <button
          onClick={handleSimplify}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
        >
          Simplify
        </button>
      </div>
    </div>
  );
}