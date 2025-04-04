import { useState } from 'react';
import Sidebar from '../components/Sidebar';
import Inbox from '../components/Inbox';
import Navbar from '../components/Navbar';
import EmailDetail from '../components/EmailDetail';
import ComposeView from '../components/ComposeView';

export default function Dashboard() {
  const [activeSection, setActiveSection] = useState("Inbox");
  const [selectedEmail, setSelectedEmail] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [replyEmail, setReplyEmail] = useState(null);

  const [emails, setEmails] = useState([
    {
      id: 1,
      sender: "john@example.com",
      subject: "Meeting Agenda",
      body: "Let's meet tomorrow at 10am.",
      starred: false,
      deleted: false,
    },
    {
      id: 2,
      sender: "sales@company.com",
      subject: "New Offers!",
      body: "Don't miss our limited-time deals.",
      starred: true,
      deleted: false,
    },
    {
      id: 3,
      sender: "support@service.com",
      subject: "Your Ticket Update",
      body: "Your issue has been resolved.",
      starred: false,
      deleted: false,
    },
  ]);

  // Toggle star
  const handleStar = (id) => {
    setEmails((prev) =>
      prev.map((email) =>
        email.id === id ? { ...email, starred: !email.starred } : email
      )
    );
  };

  // Toggle delete/restore
  const handleDelete = (id) => {
    setEmails((prev) =>
      prev.map((email) =>
        email.id === id ? { ...email, deleted: !email.deleted } : email
      )
    );
  };

  // Filter emails based on section and search
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

  // Send new email or reply
  const handleSendEmail = (newEmail) => {
    const newId = Math.max(...emails.map(e => e.id)) + 1;
    setEmails([
      { ...newEmail, id: newId, starred: false, deleted: false },
      ...emails,
    ]);
    setActiveSection("Inbox");
    setReplyEmail(null);
  };

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <Sidebar
        active={activeSection}
        onSelect={(section) => {
          setActiveSection(section);
          setSelectedEmail(null);
          setReplyEmail(null);
        }}
      />

      {/* Main content */}
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

      {/* Compose Button */}
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