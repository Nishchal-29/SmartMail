// src/components/GmailComponent.jsx
import React, { useEffect, useState } from "react";
import { gapi } from "gapi-script";
import { format } from "express/lib/response";

const GmailComponent = ({ accessToken }) => {
  const [emails, setEmails] = useState([]);

  useEffect(() => {
    const initializeGmailApi = async () => {
      try {
        await gapi.client.init({
          discoveryDocs: ["https://www.googleapis.com/discovery/v1/apis/gmail/v1/rest"],
        });

        gapi.auth.setToken({ access_token: accessToken });

        fetchEmails();
      } catch (error) {
        console.error("Gmail API init error", error);
      }
    };

    gapi.load("client", initializeGmailApi);
  }, [accessToken]);

  const fetchEmails = async () => {
    try {
      const response = await gapi.client.gmail.users.messages.list({
        userId: "me",
        maxResults: 10,
      });

      const messages = response.result.messages || [];

      const emailData = await Promise.all(
        messages.map(async (msg) => {
          const detail = await gapi.client.gmail.users.messages.get({
            userId: "me",
            id: msg.id,
            format: "full"
          });

          const getBodyFromPayload = (payload) => {
            const parts = payload.parts || [];
          
            const getTextPart = (partList) => {
              for (const part of partList) {
                if (part.mimeType === "text/plain" && part.body?.data) {
                  return part.body.data;
                } else if (part.parts) {
                  const nested = getTextPart(part.parts);
                  if (nested) return nested;
                }
              }
              return null;
            };
          
            const encodedBody =
              payload.body?.data || getTextPart(parts) || "Body not found";
          
            const decoded = atob(encodedBody.replace(/-/g, "+").replace(/_/g, "/"));
            return decoded;
          };

          const fullEmails = await Promise.all(
            messages.map(async (msg) => {
              const detail = await gapi.client.gmail.users.messages.get({
                userId: GMAIL_USER_ID,
                id: msg.id,
                format: "full",
              });
          
              const headers = detail.result.payload.headers.reduce((acc, h) => {
                acc[h.name] = h.value;
                return acc;
              }, {});

          const from = headers.find((h) => h.name === "From")?.value || "Unknown";
          const subject = headers.find((h) => h.name === "Subject")?.value || "(No Subject)";
          const body = detail.result;

          return {
            id: detail.result.id,
            sender: headers["From"] || "Unknown",
            subject: headers["Subject"] || "(No subject)",
            snippet: detail.result.snippet,
            labelIds: detail.result.labelIds,
            body: getBodyFromPayload(detail.result.payload).substring(0,150), 
          };
        })
      );
        })
      );

      setEmails(emailData);
    } catch (error) {
      console.error("Error fetching emails:", error);
    }
  };

  return (
    <div>
      <h2>Your Gmail Inbox</h2>
      <ul>
        {emails.map((email) => (
          <li key={email.id} className="mb-4 border-b pb-2">
            <strong>From:</strong> {email.sender} <br />
            <strong>Subject:</strong> {email.subject} <br />
            <p>{email.body}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default GmailComponent;
