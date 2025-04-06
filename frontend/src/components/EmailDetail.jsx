// // import { useState } from 'react';

// // export default function EmailDetail({ email, onBack, onReply }) {
// //   const [simplified, setSimplified] = useState("");

// //   const handleSimplify = () => {
// //     const simple = email.body.length > 60
// //       ? email.body.slice(0, 60) + "..."
// //       : email.body;
// //     setSimplified(simple);
// //   };

// //   return (
// //     <div className="flex flex-col h-full">
// //       <div>
// //         <button onClick={onBack} className="text-blue-600 mb-4">&larr; Back</button>
// //         <h2 className="text-2xl font-bold mb-2">{email.subject}</h2>
// //         <p className="text-sm text-gray-500 mb-4">From: {email.sender}</p>
// //         <div className="text-gray-800 mb-6" dangerouslySetInnerHTML={{ __html: email.body }} />

// //         {simplified && (
// //           <div className="bg-yellow-100 p-4 rounded mb-6">
// //             <strong>Summarized:</strong> {simplified}
// //           </div>
// //         )}
// //       </div>

// //       {/* Button group fixed to bottom */}
// //       <div className="mt-auto pt-6 flex gap-3">
// //         <button
// //           onClick={() => onReply(email)}
// //           className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
// //         >
// //           Reply
// //         </button>
// //         <button
// //           onClick={() => alert("Prompt-based reply coming soon...")}
// //           className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
// //         >
// //           Prompt-Based Reply
// //         </button>
// //         <button
// //           onClick={handleSimplify}
// //           className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
// //         >
// //           Simplify
// //         </button>
// //       </div>
// //     </div>
// //   );
// // }

// import { useState } from "react";

// export default function EmailDetail({ email, onBack, onReply }) {
//   const [simplifiedText, setSimplifiedText] = useState(null);
//   const [loading, setLoading] = useState(false);

//   // const handleSimplify = async () => {
//   //   try {
//   //     setLoading(true);
//   //     const res = await fetch("http://localhost:8000/simplify", {
//   //       method: "POST",
//   //       headers: { "Content-Type": "application/json" },
//   //       body: JSON.stringify({ body: email.body }),
//   //     });

//   //     const data = await res.json();
//   //     setSimplifiedText(data.summary);
//   //   } catch (error) {
//   //     console.error("Simplify failed:", error);
//   //   } finally {
//   //     setLoading(false);
//   //   }
//   // };
//   const handleSimplify = async () => {
//   if (!email?.body) {
//     console.error("Email body is missing.");
//     return;
//   }

//   setLoading(true);
//   try {
//     const res = await fetch("http://localhost:8000/simplify", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ body: email.body })
//     });

//     const data = await res.json();
//     setSimplifiedText(data.summary || "No summary returned.");
//   } catch (err) {
//     console.error("Simplify API call failed:", err);
//   } finally {
//     setLoading(false);
//   }
// };

//   if (!email) return null;

//   return (
//     <div className="p-6">
//       <button onClick={onBack} className="mb-4 text-blue-600 hover:underline">← Back</button>

//       <h2 className="text-xl font-bold mb-2">{email.subject}</h2>
//       <p className="text-gray-600 mb-2">From: {email.sender}</p>

//       <div
//         className="text-gray-800 mb-6"
//         dangerouslySetInnerHTML={{ __html: email.body }}
//       ></div>

//       <div className="flex gap-4 mb-4">
//         <button
//           onClick={() => onReply(email)}
//           className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition"
//         >
//           Reply
//         </button>

//         <button
//           onClick={handleSimplify}
//           className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
//         >
//           {loading ? "Simplifying..." : "Simplify"}
//         </button>
//       </div>

//       {simplifiedText && (
//         <div className="p-4 bg-gray-100 border rounded">
//           <h3 className="font-semibold mb-2">Simplified Email:</h3>
//           <p>{simplifiedText}</p>
//         </div>
//       )}
//     </div>
//   );
// }

// // ----------------------
// // import { useState } from "react";

// // export default function EmailDetail({ email, onBack, onReply }) {
// //   const [simplifiedText, setSimplifiedText] = useState(null);
// //   const [smartReply, setSmartReply] = useState(null);
// //   const [loading, setLoading] = useState(false);
// //   const [replyLoading, setReplyLoading] = useState(false);

// //   const handleSimplify = async () => {
// //     try {
// //       setLoading(true);
// //       const res = await fetch("http://localhost:8000/simplify", {
// //         method: "POST",
// //         headers: { "Content-Type": "application/json" },
// //         body: JSON.stringify({ body: email.body }),
// //       });

// //       const data = await res.json();
// //       setSimplifiedText(data.summary);
// //     } catch (error) {
// //       console.error("Simplify failed:", error);
// //       setSimplifiedText("Failed to simplify email.");
// //     } finally {
// //       setLoading(false);
// //     }
// //   };

// //   const handleSmartReply = async () => {
// //     try {
// //       setReplyLoading(true);
// //       const res = await fetch("http://localhost:8000/generate-email", {
// //         method: "POST",
// //         headers: { "Content-Type": "application/json" },
// //         body: JSON.stringify({ prompt: email.body }),
// //       });

// //       const data = await res.json();
// //       setSmartReply(data.body || "No reply generated.");
// //     } catch (err) {
// //       console.error("Smart reply failed:", err);
// //       setSmartReply("Failed to generate reply.");
// //     } finally {
// //       setReplyLoading(false);
// //     }
// //   };

// //   if (!email) return null;

// //   return (
// //     <div className="p-6">
// //       <button onClick={onBack} className="mb-4 text-blue-600 hover:underline">← Back</button>

// //       <h2 className="text-xl font-bold mb-2">{email.subject}</h2>
// //       <p className="text-gray-600 mb-2">From: {email.sender}</p>

// //       <div
// //         className="text-gray-800 mb-6"
// //         dangerouslySetInnerHTML={{ __html: email.body }}
// //       ></div>

// //       <div className="flex gap-4 mb-4">
// //         <button
// //           onClick={() => onReply(email)}
// //           className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition"
// //         >
// //           Reply
// //         </button>

// //         <button
// //           onClick={handleSimplify}
// //           className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
// //         >
// //           {loading ? "Simplifying..." : "Simplify"}
// //         </button>

// //         <button
// //           onClick={handleSmartReply}
// //           className="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600 transition"
// //         >
// //           {replyLoading ? "Generating..." : "Smart Reply"}
// //         </button>
// //       </div>

// //       {simplifiedText && (
// //         <div className="p-4 bg-gray-100 border rounded mt-4">
// //           <h3 className="font-semibold mb-2">Simplified Email:</h3>
// //           <p>{simplifiedText}</p>
// //         </div>
// //       )}

// //       {smartReply && (
// //         <div className="p-4 mt-4 bg-purple-50 border-l-4 border-purple-400 rounded">
// //           <h3 className="font-semibold text-purple-800 mb-2">AI-Crafted Response:</h3>
// //           <p className="text-gray-800 whitespace-pre-wrap">{smartReply}</p>
// //         </div>
// //       )}
// //     </div>
// //   );
// // }

// _________________________________________
import { useState } from "react";

export default function EmailDetail({ email, onBack, onReply }) {
  const [simplifiedText, setSimplifiedText] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSimplify = async () => {
    if (!email?.body) {
      console.error("No email body to simplify.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/simplify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ body: email.body }) // Must match FastAPI model
      });

      const data = await res.json();
      setSimplifiedText(data.summary || "No summary returned.");
    } catch (err) {
      console.error("Simplify API call failed:", err);
      setSimplifiedText("Error summarizing the email.");
    } finally {
      setLoading(false);
    }
  };

  if (!email) return null;

  return (
    <div className="p-6">
      <button onClick={onBack} className="mb-4 text-blue-600 hover:underline">← Back</button>

      <h2 className="text-xl font-bold mb-2">{email.subject}</h2>
      <p className="text-gray-600 mb-2">From: {email.sender}</p>

      <div
        className="text-gray-800 mb-6"
        dangerouslySetInnerHTML={{ __html: email.body }}
      ></div>

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
          {loading ? "Simplifying..." : "Simplify"}
        </button>
      </div>

      {simplifiedText && (
        <div className="p-4 bg-gray-100 border rounded">
          <h3 className="font-semibold mb-2">Simplified Email:</h3>
          <p>{simplifiedText}</p>
        </div>
      )}
    </div>
  );
}