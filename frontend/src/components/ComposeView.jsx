import { useState, useEffect } from "react";

export default function ComposeView({ onSend, replyTo }) {
  const [to, setTo] = useState("");
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [prompt, setPrompt] = useState(""); // for new email
  const [userPrompt, setUserPrompt] = useState(""); // for smart reply
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

  const handleSmartReply = async () => {
    if (!replyTo?.body) return;
    setSmartReplyLoading(true);
    try {
      const res = await fetch("http://localhost:8000/smart-reply", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt: replyTo.body,
          user_prompt: userPrompt || "",
        }),
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

      {replyTo && (
        <>
          <div className="mb-4 bg-gray-50 border p-3 rounded shadow-inner">
            <label className="block text-sm font-semibold mb-1">Optional prompt to guide reply:</label>
            <textarea
              rows="3"
              className="w-full border rounded p-2"
              placeholder="e.g. make it more empathetic, add apology, etc."
              value={userPrompt}
              onChange={(e) => setUserPrompt(e.target.value)}
            />
          </div>

          <button
            onClick={handleSmartReply}
            className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700 mb-6 mr-6 transition"
            disabled={smartReplyLoading}
          >
            {smartReplyLoading ? "Generating Reply..." : "Generate Smart Reply"}
           </button> 
        </>
      )}

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

      <button
        onClick={handleSend}
        className="bg-[#3869f2] hover:bg-blue-800 text-white px-6 py-2 rounded transition-all hover:scale-105"
      >
        Send
      </button>
    </div>
  );
}