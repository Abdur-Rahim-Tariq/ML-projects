import React, { useState } from "react";

// Replace this with your actual API base URL
const API_BASE = "http://localhost:8000/api";

// Helper function to make authenticated API calls
async function apiFetch(endpoint, options = {}) {
  const token = localStorage.getItem("token");
  const headers = {
    ...options.headers,
  };
  
  if (token && !(options.body instanceof FormData)) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  
  if (token && options.body instanceof FormData) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    throw new Error("Request failed");
  }

  return response.json();
}

export default function Dashboard({ onLogout }) {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  // Paste inside your Dashboard.jsx (or wherever you handle image upload)
async function handleUpload(e) {
  e.preventDefault();
  if (!file) return alert("Please select an image.");
  setLoading(true);

  const form = new FormData();
  form.append("image", file);

  try {
    const token = localStorage.getItem("token"); // get JWT
    if (!token) return alert("You must be logged in.");

    const res = await fetch(`${API_BASE}/upload/`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}` // send token
        // Do NOT set Content-Type for FormData
      },
      body: form,
    });

    if (!res.ok) {
      throw new Error("Upload failed");
    }

    const data = await res.json();
    setResult(data); // show detected items
  } catch (err) {
    alert("Upload failed. Make sure you are logged in and backend is running.");
  } finally {
    setLoading(false);
  }
}

  

  function handleDrag(e) {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }

  function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 p-4">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Header */}
        <div className="bg-slate-800 rounded-2xl shadow-2xl p-6 border border-slate-700">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-3xl font-bold text-white">Dashboard</h2>
              <p className="text-slate-400 mt-1">Upload and analyze images</p>
            </div>
            <button 
              onClick={onLogout}
              className="px-6 py-2 bg-slate-700 text-white rounded-lg font-medium hover:bg-slate-600 transition duration-200 border border-slate-600"
            >
              Logout
            </button>
          </div>
        </div>

        {/* Upload Section */}
        <div className="bg-slate-800 rounded-2xl shadow-2xl p-8 border border-slate-700">
          <h3 className="text-xl font-semibold text-white mb-6">Upload Image</h3>
          
          <div 
            className={`border-2 border-dashed rounded-xl p-8 text-center transition ${
              dragActive 
                ? "border-blue-500 bg-blue-500/10" 
                : "border-slate-600 hover:border-slate-500"
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <div className="space-y-4">
              <div className="flex justify-center">
                <svg className="w-16 h-16 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
              
              {file ? (
                <div className="space-y-2">
                  <p className="text-green-400 font-medium">{file.name}</p>
                  <p className="text-slate-400 text-sm">
                    {(file.size / 1024).toFixed(2)} KB
                  </p>
                </div>
              ) : (
                <div className="space-y-2">
                  <p className="text-slate-300">Drag and drop your image here</p>
                  <p className="text-slate-500 text-sm">or</p>
                </div>
              )}

              <div className="flex justify-center gap-3">
                <label className="px-6 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition duration-200 cursor-pointer">
                  Choose File
                  <input 
                    type="file" 
                    accept="image/*" 
                    onChange={e => setFile(e.target.files[0])}
                    className="hidden"
                  />
                </label>
                
                {file && (
                  <button 
                    onClick={() => setFile(null)}
                    className="px-6 py-2 bg-slate-700 text-white rounded-lg font-medium hover:bg-slate-600 transition duration-200"
                  >
                    Clear
                  </button>
                )}
              </div>
            </div>
          </div>

          <button 
            onClick={handleUpload}
            disabled={loading || !file}
            className="w-full mt-6 bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition duration-200 shadow-lg disabled:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? "Uploading..." : "Upload & Analyze"}
          </button>
        </div>

        {/* Results Section */}
        {result && (
          <div className="bg-slate-800 rounded-2xl shadow-2xl p-8 border border-slate-700">
            <h3 className="text-xl font-semibold text-white mb-4">Detection Results</h3>
            <div className="bg-slate-900 rounded-lg p-6 border border-slate-700">
              <pre className="text-slate-300 text-sm overflow-x-auto whitespace-pre-wrap">
                {JSON.stringify(result, null, 2)}
              </pre>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}