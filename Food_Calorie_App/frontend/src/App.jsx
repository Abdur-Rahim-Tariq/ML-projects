import React, { useState } from "react";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";

export default function App() {
  const [user, setUser] = useState(localStorage.getItem("token") ? true : false);
  const [page, setPage] = useState(user ? "dashboard" : "login");

  function handleLogout() {
    localStorage.removeItem("token");
    setUser(false);
    setPage("login");
  }

  if (page === "login") return <Login setUser={setUser} setPage={setPage} />;
  if (page === "signup") return <Signup setPage={setPage} />;
  if (page === "dashboard") return <Dashboard onLogout={handleLogout} />;
}
