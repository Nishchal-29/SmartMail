import { useState, useEffect } from "react";
import { gapi } from "gapi-script";
import Sidebar from "../components/Sidebar";
import Inbox from "../components/Inbox";
import Navbar from "../components/Navbar";
import EmailDetail from "../components/EmailDetail";
import ComposeView from "../components/ComposeView";
import { getDatabase, ref, get } from "firebase/database"; // Realtime Database imports
import { initializeApp } from "firebase/app";

export default function Dashboard({ accessToken, user, onSignOut }) {
  const [activeSection, setActiveSection] = useState("Inbox");
  const [selectedEmail, setSelectedEmail] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [replyEmail, setReplyEmail] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [emails, setEmails] = useState([]);
  const [sentEmails, setSentEmails] = useState([]);

  // Load Gmail API
  useEffect(() => {
    const initGmail = async () => {
      try {
        await gapi.client.init({
          discoveryDocs: ["https://www.googleapis.com/discovery/v1/apis/gmail/v1/rest"],
        });

        gapi.auth.setToken({ access_token: accessToken });
        fetchEmails();
      } catch (err) {
        console.error("Failed to initialize Gmail API", err);
      }
    };

    gapi.load("client", initGmail);
  }, [accessToken]);

  const firebaseConfig = {
    apiKey: "AIzaSyDmAQQ0iHTq-RTAc2WeD1qoZxDRroCrkx8",
    authDomain: "smartmail-bc5f2.firebaseapp.com",
    databaseURL: "https://smartmail-bc5f2-default-rtdb.firebaseio.com",
    projectId: "smartmail-bc5f2",
    storageBucket: "smartmail-bc5f2.firebasestorage.app",
    messagingSenderId: "684319493774",
    appId: "1:684319493774:web:ceceae8ed48f1a8fa9c3df",
    measurementId: "G-Y3YV5J85JL"
  };

  // Initialize Firebase App
const app = initializeApp(firebaseConfig);

const fetchEmails = async () => {
  try {
    const db = getDatabase(app); // assumes Firebase App is already initialized
    const dbRef = ref(db, "/"); // root level
    const snapshot = await get(dbRef);

    if (snapshot.exists()) {
      const data = snapshot.val();
      const emailData = Object.keys(data).map((key) => ({
        id: key,
        sender: data[key].sender || "me",
        subject: data[key].email.substring(9,100) || "(No Subject)",
        body: data[key].email || "",
        read: data[key].read ?? true,        // default true if not present
        starred: data[key].starred ?? false, // default false
        deleted: data[key].deleted ?? false, // default false
        date: data[key].date || new Date().toISOString(),
      }));
      setEmails(emailData);
    } else {
      console.log("No emails found.");
      setEmails([]);
    }
  } catch (err) {
    console.error("Error fetching emails from Firebase", err);
  }
};


  // // Fetch Emails from Gmail
  // const fetchEmails = async () => {
  //   try {
  //     const res = await gapi.client.gmail.users.messages.list({
  //       userId: "me",
  //       maxResults: 15,
  //     });

  //     const messages = res.result.messages || [];

  //     const emailData = await Promise.all(
  //       messages.map(async (msg) => {
  //         const detail = await gapi.client.gmail.users.messages.get({
  //           userId: "me",
  //           id: msg.id,
  //         });

  //         const headers = detail.result.payload.headers;
  //         const from = headers.find((h) => h.name === "From")?.value || "Unknown";
  //         const subject = headers.find((h) => h.name === "Subject")?.value || "(No Subject)";
  //         let body = "";

  //         const parts = detail.result.payload.parts;
  //         if (parts) {
  //           const htmlPart = parts.find(part => part.mimeType === "text/html");
  //           if (htmlPart) {
  //             body = atob(htmlPart.body.data.replace(/-/g, '+').replace(/_/g, '/'));
  //           } else {
  //             const textPart = parts.find(part => part.mimeType === "text/plain");
  //             if (textPart) {
  //               body = atob(textPart.body.data.replace(/-/g, '+').replace(/_/g, '/'));
  //             }
  //           }
  //         } else if (detail.result.payload.body?.data) {
  //           body = atob(detail.result.payload.body.data.replace(/-/g, '+').replace(/_/g, '/'));
  //         }

  //         const isUnread = detail.result.labelIds.includes("UNREAD");

  //         return {
  //           id: msg.id,
  //           sender: from,
  //           subject,
  //           body,
  //           read: !isUnread,
  //           starred: false,
  //           deleted: false,
  //           date: new Date().toISOString(),
  //         };
  //       })
  //     );

  //     setEmails(emailData);
  //   } catch (err) {
  //     console.error("Error fetching emails", err);
  //   }
  // };

  // Email Handlers
  const handleToggleRead = (id) => {
    setEmails((prev) =>
      prev.map((email) =>
        email.id === id ? { ...email, read: !email.read } : email
      )
    );
  };

  const handleStar = (id) => {
    setEmails((prev) =>
      prev.map((email) =>
        email.id === id ? { ...email, starred: !email.starred } : email
      )
    );
  };

  const handleDelete = (id) => {
    setEmails((prev) =>
      prev.map((email) =>
        email.id === id ? { ...email, deleted: !email.deleted } : email
      )
    );
  };

  // const handleSendEmail = (newEmail) => {
  //   const newId = Math.max(0, ...emails.map(e => e.id), ...sentEmails.map(e => e.id)) + 1;

  //   const sent = {
  //     ...newEmail,
  //     id: newId,
  //     read: true,
  //     starred: false,
  //     deleted: false,
  //     date: new Date().toISOString(),
  //   };
  //   setSentEmails([sent, ...sentEmails]);

  //   if (!newEmail.replyTo) {
  //     const incoming = { ...sent, sender: "me@smartmail.com", read: false };
  //     setEmails([incoming, ...emails]);
  //   }

  //   setActiveSection("Inbox");
  //   setReplyEmail(null);
  // };

  const handleSendEmail = async (newEmail) => {
    try {
      const emailContent =
        `From: me\n` +
        `To: ${newEmail.to}\n` +
        `Subject: ${newEmail.subject}\n\n` +
        `${newEmail.body}`;

      const base64EncodedEmail = btoa(emailContent)
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=+$/, '');

      await gapi.client.gmail.users.messages.send({
        userId: 'me',
        resource: {
          raw: base64EncodedEmail,
        },
      });

      console.log("Email sent successfully!");

      const newId = Math.max(0, ...emails.map(e => parseInt(e.id, 10)), ...sentEmails.map(e => parseInt(e.id, 10))) + 1;

      const sent = { ...newEmail, id: newId, read: true, starred: false, deleted: false };
      setSentEmails([sent, ...sentEmails]);

      setActiveSection("Inbox");
      setReplyEmail(null);
    } catch (error) {
      console.error("Failed to send email", error);
    }
  };


  const handleSelectEmail = (email) => {
    if (!email.read) {
      setEmails((prev) =>
        prev.map((e) => (e.id === email.id ? { ...e, read: true } : e))
      );
    }
    setSelectedEmail(email);
  };

  // ✅ Filtered View
  const filteredEmails = (() => {
    const filter = (list) =>
      list.filter((email) =>
        email.sender.toLowerCase().includes(searchQuery.toLowerCase()) ||
        email.subject.toLowerCase().includes(searchQuery.toLowerCase())
      );

    switch (activeSection) {
      case "Inbox":
        return filter(emails.filter((e) => !e.deleted));
      case "Starred":
        return filter(emails.filter((e) => e.starred && !e.deleted));
      case "Trash":
        return filter(emails.filter((e) => e.deleted));
      case "Sent":
        return filter(sentEmails);
      default:
        return [];
    }
  })();

  const unreadCount = emails.filter((e) => !e.read && !e.deleted).length;

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <div className="hidden md:block">
        <Sidebar
          active={activeSection}
          onSelect={(section) => {
            setActiveSection(section);
            setSelectedEmail(null);
            setReplyEmail(null);
            setSidebarOpen(false);
          }}
          unreadCount={unreadCount}
        />
      </div>

      {/* Mobile Sidebar */}
      {sidebarOpen && (
        <div
          className="md:hidden fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={() => setSidebarOpen(false)}
        >
          <div className="absolute left-0 top-0 bg-[#3869f2] text-white w-64 h-full">
            <Sidebar
              active={activeSection}
              onSelect={(section) => {
                setActiveSection(section);
                setSelectedEmail(null);
                setReplyEmail(null);
                setSidebarOpen(false);
              }}
              unreadCount={unreadCount}
            />
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <Navbar
          onSearch={setSearchQuery}
          onMenuClick={() => setSidebarOpen(true)}
          onSignOut={onSignOut}
          user={user}
        />

        <div className="flex-1 overflow-auto p-6">
          <div className="animate-fadeIn">
            {activeSection === "Compose" ? (
              <ComposeView onSend={handleSendEmail} replyTo={replyEmail} />
            ) : selectedEmail ? (
              <EmailDetail
                email={selectedEmail}
                onBack={() => setSelectedEmail(null)}
                onReply={(email) => {
                  setReplyEmail(email);
                  setActiveSection("Compose");
                }}
              />
            ) : (
              <Inbox
                emails={filteredEmails}
                onSelect={handleSelectEmail}
                onStar={handleStar}
                onDelete={handleDelete}
                onToggleRead={handleToggleRead}
              />
            )}
          </div>
        </div>
      </div>

      {/* Compose Button */}
      {activeSection !== "Compose" && (
        <button
          onClick={() => {
            setReplyEmail(null);
            setActiveSection("Compose");
          }}
          className="fixed bottom-6 right-6 bg-[#3869f2] hover:bg-blue-800 text-white px-6 py-3 rounded-full shadow-lg z-50 transition-all duration-300 transform hover:scale-105 hover:shadow-xl"
        >
          Compose
        </button>
      )}
    </div>
  );
}