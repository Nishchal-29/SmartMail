// import { useState } from 'react';

// export default function EmailDetail({ email, onBack, onReply }) {
//   const [simplified, setSimplified] = useState("");

//   const handleSimplify = () => {
//     const simple = email.body.length > 60
//       ? email.body.slice(0, 60) + "..."
//       : email.body;
//     setSimplified(simple);
//   };

//   return (
//     <div className="flex flex-col h-full">
//       <div>
//         <button onClick={onBack} className="text-blue-600 mb-4">&larr; Back</button>
//         <h2 className="text-2xl font-bold mb-2">{email.subject}</h2>
//         <p className="text-sm text-gray-500 mb-4">From: {email.sender}</p>
//         <div className="text-gray-800 mb-6" dangerouslySetInnerHTML={{ __html: email.body }} />

//         {simplified && (
//           <div className="bg-yellow-100 p-4 rounded mb-6">
//             <strong>Summarized:</strong> {simplified}
//           </div>
//         )}
//       </div>

//       {/* Button group fixed to bottom */}
//       <div className="mt-auto pt-6 flex gap-3">
//         <button
//           onClick={() => onReply(email)}
//           className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
//         >
//           Reply
//         </button>
//         <button
//           onClick={() => alert("Prompt-based reply coming soon...")}
//           className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
//         >
//           Prompt-Based Reply
//         </button>
//         <button
//           onClick={handleSimplify}
//           className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
//         >
//           Simplify
//         </button>
//       </div>
//     </div>
//   );
// }
import React, { useState } from "react";

export default function EmailDetail({ email, onBack, onReply }) {
  const [simplifiedText, setSimplifiedText] = useState(null);

  const handleSimplify = async () => {
    try {
      console.log("Sending to simplify:", email.body); // DEBUG

      const res = await fetch("http://localhost:8000/simplify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ body: email.body }),
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const data = await res.json();
      console.log("Simplified response:", data); // DEBUG
      setSimplifiedText(data.summary);
    } catch (error) {
      console.error("Simplify failed:", error);
    }
  };

  if (!email) return null;

  return (
    <div className="p-6">
      {/* Back Button */}
      <button onClick={onBack} className="mb-4 text-blue-600 hover:underline">
        ← Back
      </button>

      {/* Email Subject + Sender */}
      <h2 className="text-xl font-bold mb-2">{email.subject}</h2>
      <p className="text-gray-600 mb-2">From: {email.sender}</p>

      {/* Email Body Rendered as HTML */}
      <div
        className="text-gray-800 mb-6"
        dangerouslySetInnerHTML={{ __html: email.body }}
      ></div>

      {/* Action Buttons */}
      <div className="flex gap-4 mb-4">
        <button
          onClick={() => onReply(email)}
          className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition"
        >
          Reply
        </button>

        <button
          onClick={handleSimplify}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
        >
          Simplify
        </button>
      </div>

      {/* Simplified Result */}
      {simplifiedText && (
        <div className="p-4 bg-gray-100 border rounded">
          <h3 className="font-semibold mb-2">Simplified Email:</h3>
          <p>{simplifiedText}</p>
        </div>
      )}
    </div>
  );
}