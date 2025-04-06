// import { useState } from 'react';

// export default function ComposeModal({ onClose, onSend }) {
//   const [to, setTo] = useState("");
//   const [subject, setSubject] = useState("");
//   const [body, setBody] = useState("");

//   const handleSend = () => {
//     if (to && subject && body) {
//       onSend({ sender: to, subject, body });
//       onClose();
//     }
//   };

//   return (
//     <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-10">
//       <div className="bg-white w-96 p-6 rounded shadow-lg">
//         <h2 className="text-xl font-bold mb-4">New Message</h2>
//         <input
//           placeholder="To"
//           className="w-full mb-2 p-2 border"
//           value={to}
//           onChange={(e) => setTo(e.target.value)}
//         />
//         <input
//           placeholder="Subject"
//           className="w-full mb-2 p-2 border"
//           value={subject}
//           onChange={(e) => setSubject(e.target.value)}
//         />
//         <textarea
//           rows="5"
//           className="w-full p-2 border mb-4"
//           placeholder="Write your message here..."
//           value={body}
//           onChange={(e) => setBody(e.target.value)}
//         />
//         <div className="flex justify-end space-x-2">
//           <button onClick={onClose} className="text-gray-600">Cancel</button>
//           <button onClick={handleSend} className="bg-[#3869f2] text-white px-4 py-2 rounded">Send</button>
//         </div>
//       </div>
//     </div>
//   );
// }