import { useState, useEffect } from "react";

export default function ComposeView({ onSend, replyTo }) {
  const [to, setTo] = useState("");
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [prompt, setPrompt] = useState("");
  const [loadingPrompt, setLoadingPrompt] = useState(false);
  const [smartReplyLoading, setSmartReplyLoading] = useState(false);

  useEffect(() => {
    if (replyTo) {
      setTo(replyTo.sender);
      setSubject("Re: " + replyTo.subject);
    }
  }, [replyTo]);

  const handleSend = () => {
    onSend({ to, subject, body, replyTo });
  };

  // Compose from user-entered prompt
const handleGenerateFromPrompt = async () => {
  if (!prompt) return;
  setLoadingPrompt(true);
  try {
    const res = await fetch("http://localhost:8000/compose-email", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });
    const data = await res.json();
    if (data.response) setBody(data.response);
  } catch (err) {
    console.error("Prompt-based email generation failed:", err);
  } finally {
    setLoadingPrompt(false);
  }
};

// Smart reply to existing email
const handleSmartReply = async () => {
  if (!replyTo?.body) return;
  setSmartReplyLoading(true);
  try {
    const res = await fetch("http://localhost:8000/smart-reply", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: replyTo.body }),
    });
    const data = await res.json();
    if (data.response) setBody(data.response);
  } catch (error) {
    console.error("Smart reply generation failed:", error);
  } finally {
    setSmartReplyLoading(false);
  }
};

  return (
    <div className="max-w-4xl mx-auto animate-fadeIn">
      <h2 className="text-2xl font-bold mb-6">{replyTo ? "Reply" : "New Message"}</h2>

      <div className="mb-4">
        <label className="block text-sm font-semibold mb-1">To:</label>
        <input
          className="w-full p-2 border rounded"
          value={to}
          onChange={(e) => setTo(e.target.value)}
          type="email"
        />
      </div>

      <div className="mb-4">
        <label className="block text-sm font-semibold mb-1">Subject:</label>
        <input
          className="w-full p-2 border rounded"
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
        />
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

      {/* Smart Reply button */}
      {replyTo && (
        <button
          onClick={handleSmartReply}
          className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700 mb-4 mr-3 transition"
          disabled={smartReplyLoading}
        >
          {smartReplyLoading ? "Generating..." : "Smart Reply"}
        </button>
      )}

      {/* AI Prompt-to-Email Generator */}
      {!replyTo && (
        <div className="mb-6 bg-gray-50 p-4 border rounded shadow-inner">
          <label className="block text-sm font-semibold mb-2">✨ Generate with AI (optional):</label>
          <textarea
            rows="3"
            className="w-full p-2 border rounded mb-2"
            placeholder="e.g., write a leave request for April 2-6..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
          <button
            onClick={handleGenerateFromPrompt}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition"
            disabled={loadingPrompt}
          >
            {loadingPrompt ? "Generating..." : "Generate Email"}
          </button>
        </div>
      )}

      {/* Send Button */}
      <button
        onClick={handleSend}
        className="bg-[#3869f2] hover:bg-blue-800 text-white px-6 py-2 rounded transition-all hover:scale-105"
      >
        Send
      </button>
    </div>
  );
}