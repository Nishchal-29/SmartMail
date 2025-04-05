import { useState, useEffect } from "react";
import { gapi } from "gapi-script";
import Sidebar from "../components/Sidebar";
import Inbox from "../components/Inbox";
import Navbar from "../components/Navbar";
import EmailDetail from "../components/EmailDetail";
import ComposeView from "../components/ComposeView";

export default function Dashboard({ accessToken }) {
  const [activeSection, setActiveSection] = useState("Inbox");
  const [selectedEmail, setSelectedEmail] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [replyEmail, setReplyEmail] = useState(null);
  const [emails, setEmails] = useState([]);

  // ✅ Initialize Gmail API
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

  // ✅ Fetch emails from Gmail
  const fetchEmails = async () => {
    try {
      const res = await gapi.client.gmail.users.messages.list({
        userId: "me",
        maxResults: 15,
      });

      const messages = res.result.messages || [];

      const emailData = await Promise.all(
        messages.map(async (msg) => {
          const detail = await gapi.client.gmail.users.messages.get({
            userId: "me",
            id: msg.id,
          });

          const headers = detail.result.payload.headers;
          const from = headers.find((h) => h.name === "From")?.value || "Unknown";
          const subject = headers.find((h) => h.name === "Subject")?.value || "(No Subject)";
          const body = detail.result.snippet;

          return {
            id: msg.id,
            sender: from,
            subject,
            body,
            starred: false,
            deleted: false,
          };
        })
      );

      setEmails(emailData);
    } catch (err) {
      console.error("Error fetching emails", err);
    }
  };

  // ⭐ Toggle star
  const handleStar = (id) => {
    setEmails((prev) =>
      prev.map((email) =>
        email.id === id ? { ...email, starred: !email.starred } : email
      )
    );
  };

  // 🗑️ Toggle delete
  const handleDelete = (id) => {
    setEmails((prev) =>
      prev.map((email) =>
        email.id === id ? { ...email, deleted: !email.deleted } : email
      )
    );
  };

  // 🔍 Filter emails based on section and search
  const filteredEmails = emails.filter((email) => {
    const matchesSearch =
      email.sender.toLowerCase().includes(searchQuery.toLowerCase()) ||
      email.subject.toLowerCase().includes(searchQuery.toLowerCase());

    if (activeSection === "Inbox") {
      return !email.deleted && matchesSearch;
    }
    if (activeSection === "Starred") {
      return email.starred && !email.deleted && matchesSearch;
    }
    if (activeSection === "Trash") {
      return email.deleted && matchesSearch;
    }
    return false;
  });

  // ✉️ Send email or reply (simulated for now)
  const handleSendEmail = (newEmail) => {
    const newId = Math.max(...emails.map((e) => parseInt(e.id) || 0), 0) + 1;
    setEmails([
      { ...newEmail, id: newId, starred: false, deleted: false },
      ...emails,
    ]);
    setActiveSection("Inbox");
    setReplyEmail(null);
  };

  return (
    <div className="flex h-screen">
      <Sidebar
        active={activeSection}
        onSelect={(section) => {
          setActiveSection(section);
          setSelectedEmail(null);
          setReplyEmail(null);
        }}
      />

      <div className="flex-1 flex flex-col overflow-hidden">
        <Navbar onSearch={setSearchQuery} />

        <div className="flex-1 overflow-auto p-6">
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
              onSelect={setSelectedEmail}
              onStar={handleStar}
              onDelete={handleDelete}
            />
          )}
        </div>
      </div>

      {activeSection !== "Compose" && (
        <button
          onClick={() => {
            setReplyEmail(null);
            setActiveSection("Compose");
          }}
          className="fixed bottom-6 right-6 bg-[#3869f2] hover:bg-blue-800 text-white px-6 py-3 rounded-full shadow-lg z-50"
        >
          Compose
        </button>
      )}
    </div>
  );
}
