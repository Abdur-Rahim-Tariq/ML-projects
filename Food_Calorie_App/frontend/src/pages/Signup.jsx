import React, { useState } from "react";


const API_BASE = "http://localhost:8000/api";

export default function Signup({ setPage }) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

 
async function handleSignup(e) {
  e.preventDefault();
  setMsg("");

  try {
    const res = await fetch(`${API_BASE}/register/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }),
    });

    const data = await res.json();

    if (res.ok) {
      setMsg("✅ Registered successfully! You can login now.");
    } else {
      setMsg(data.error || "❌ Registration failed.");
    }
  } catch (err) {
    console.error(err);
    setMsg("❌ Network error. Make sure the backend is running and CORS is allowed.");
  }
}


  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800 p-4">
      <div className="w-full max-w-md">
        <div className="bg-slate-800 rounded-2xl shadow-2xl p-8 space-y-6 border border-slate-700">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-white">Create Account</h2>
            <p className="text-slate-400 mt-2">Join us today</p>
          </div>

          {msg && (
            <div className={`p-4 rounded-lg text-sm ${
              msg.includes("✅") 
                ? "bg-emerald-50 text-emerald-700 border border-emerald-200" 
                : "bg-red-50 text-red-700 border border-red-200"
            }`}>
              {msg}
            </div>
          )}

          <div className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Username
              </label>
              <input
                value={username}
                onChange={e => setUsername(e.target.value)}
                required
                className="w-full px-4 py-3 rounded-lg border border-slate-600 bg-slate-700 text-white placeholder-slate-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                placeholder="johndoe"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                required
                className="w-full px-4 py-3 rounded-lg border border-slate-600 bg-slate-700 text-white placeholder-slate-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                placeholder="john@example.com"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                required
                className="w-full px-4 py-3 rounded-lg border border-slate-600 bg-slate-700 text-white placeholder-slate-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                placeholder="••••••••"
              />
            </div>

            <button 
              onClick={handleSignup}
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition duration-200 shadow-lg"
            >
              Sign Up
            </button>
          </div>

          <div className="text-center text-sm text-slate-600">
            Already have an account?{" "}
            <button 
              className="text-blue-400 font-medium hover:text-blue-300 hover:underline"
              onClick={() => setPage("login")}
            >
              Login
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}