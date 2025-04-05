import React, { useState, useEffect } from "react";
import SignInPage from "./pages/SignInPage";
import Dashboard from "./pages/Dashboard";

function App() {
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    const storedUser = localStorage.getItem("userData");
    if (storedUser) {
      setUserData(JSON.parse(storedUser));
    }
  }, []);

  const handleLogin = (data) => {
    setUserData(data);
    localStorage.setItem("userData", JSON.stringify(data)); // Save to localStorage
  };

  const handleSignOut = () => {
    const auth2 = window.gapi.auth2.getAuthInstance();
    auth2.signOut().then(() => {
      setUserData(null);
      localStorage.removeItem("userData");
    });
  };

  return userData ? (
    <Dashboard
      accessToken={userData.token}
      user={userData}
      onSignOut={handleSignOut}
    />
  ) : (
    <SignInPage onLogin={handleLogin} />
  );
}

export default App;