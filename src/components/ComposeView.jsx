import { useState } from 'react';

export default function ComposeView({ onSend, replyTo }) {
  const [to, setTo] = useState(replyTo?.sender || "");
  const [subject, setSubject] = useState(replyTo ? `Re: ${replyTo.subject}` : "");
  const [body, setBody] = useState("");

  const handleSend = () => {
    if (to && subject && body) {
      onSend({ sender: to, subject, body, date: new Date().toISOString() });
      setTo(""); setSubject(""); setBody("");
    }
  };

  return (
    <div className="max-w-4xl mx-auto animate-fadeIn">
      <h2 className="text-2xl font-bold mb-6">{replyTo ? "Reply" : "New Message"}</h2>

      <div className="mb-4 transition-all">
        <label className="block text-sm font-semibold mb-1">To:</label>
        <input className="w-full p-2 border rounded" value={to} onChange={(e) => setTo(e.target.value)} />
      </div>

      <div className="mb-4">
        <label className="block text-sm font-semibold mb-1">Subject:</label>
        <input className="w-full p-2 border rounded" value={subject} onChange={(e) => setSubject(e.target.value)} />
      </div>

      <div className="mb-6">
        <label className="block text-sm font-semibold mb-1">Message:</label>
        <textarea
          rows="10"
          className="w-full p-2 border rounded"
          placeholder="Write your message here..."
          value={body}
          onChange={(e) => setBody(e.target.value)}
        />
      </div>

      <button
        onClick={handleSend}
        className="bg-[#3869f2] hover:bg-blue-800 text-white px-6 py-2 rounded transition-all hover:scale-105"
      >
        Send
      </button>
    </div>
  );
}