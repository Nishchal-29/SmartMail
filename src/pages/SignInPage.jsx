// src/pages/SignInPage.jsx

import React, { useEffect, useState } from "react";
import { gapi } from "gapi-script";
import { TypeAnimation } from 'react-type-animation';

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
    <div className="h-screen flex items-center justify-center bg-gradient-to-b from-indigo-400 to-slate-50">
      
      {!user ? (
        <div className="bg-white p-8 pt-5 rounded-lg shadow-md text-center w-2/3 h-1/2 relative">
        <span className="absolute top-14 left-10 text-2xl" >
          <i className="fa-solid fa-envelope fa-2xl" style={{ color: "#3869f2" }}></i>
        </span>
      
        <TypeAnimation
          sequence={[
            'SmartMail',
            2500,
            ' ',
            () => {
              console.log('Sequence completed');
            },
          ]}
          wrapper="span"
          cursor={true}
          speed={1}
          repeat={Infinity}
          style={{ fontSize: '4em',color:"#3869f2", fontWeight: 'bold', display: 'inline-block' }}
        />
        <p className="px-10 pb-5">SmartMail is a platform that aims to transform email communication by integrating artificial intelligence into the regular mail, creating a seamless and intuitive user experience that enhances productivity and reshapes how users interact with their inbox.</p>
      
        <h1 className="text-4xl font-semibold mb-4 mt-10 text-left">Sign in</h1>
        <p className="text-left text-l">with your Google Account to continue to SmartMail.</p>
      
        <button
          onClick={handleSignIn}
          className="bg-blue-600 text-white px-16 py-4 rounded hover:bg-blue-700 transition absolute right-16 bottom-24">Sign in with Google</button>
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