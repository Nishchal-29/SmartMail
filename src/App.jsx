// App.jsx
import './index.css';
import React, { useState } from "react";
import SignInPage from "./pages/SignInPage";
import Dashboard from "./pages/Dashboard";

const App = () => {
  const [user, setUser] = useState(null);

  return (
    <>
      {!user ? (
        <SignInPage onLogin={setUser} />
      ) : (
        <Dashboard accessToken={user.token} user={user} />
      )}
    </>
  );
};

export default App;
