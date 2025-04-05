// src/pages/SignInPage.jsx

import React, { useEffect, useState } from "react";
import { gapi } from "gapi-script";

const CLIENT_ID = "409549734064-rd3k1tm08e9maj8ksnjrectjlb0pnr5n.apps.googleusercontent.com";

const SignInPage = ({ onLogin }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const initClient = () => {
      gapi.load("auth2", () => {
        gapi.auth2.init({
          clientId: CLIENT_ID,
          scope: "https://www.googleapis.com/auth/gmail.readonly profile email",
        });
      });
    };
    initClient();
  }, []);

  const handleSignIn = async () => {
    const auth2 = gapi.auth2.getAuthInstance();
    const googleUser = await auth2.signIn();

    const token = googleUser.getAuthResponse().access_token;
    const profile = googleUser.getBasicProfile();

    const userData = {
      token,
      name: profile.getName(),
      email: profile.getEmail(),
      imageUrl: profile.getImageUrl(),
    };

    setUser(userData);
    onLogin(userData); // Pass user info + token to parent
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      {!user ? (
        <div className="bg-white p-8 rounded-lg shadow-md text-center">
          <h2 className="text-2xl font-semibold mb-4">Sign in to continue</h2>
          <button
            onClick={handleSignIn}
            className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition"
          >
            Sign in with Google
          </button>
        </div>
      ) : (
        <div className="bg-white p-8 rounded-lg shadow-md text-center">
          <img
            src={user.imageUrl}
            alt="User"
            className="w-20 h-20 rounded-full mx-auto mb-4"
          />
          <h2 className="text-xl font-semibold">{user.name}</h2>
          <p>{user.email}</p>
          <p className="text-green-500 mt-2">Signed in successfully!</p>
        </div>
      )}
    </div>
  );
};

export default SignInPage;