import React, { useState, useEffect } from "react";

const API_BASE = "http://localhost:8000/api";

async function apiFetch(endpoint, options = {}) {
  const token = localStorage.getItem("token");
  const headers = { ...options.headers };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const response = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
  if (!response.ok) throw new Error("Request failed");
  return response.json();
}

export default function Dashboard({ onLogout }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [detectedItems, setDetectedItems] = useState([]);
  const [records, setRecords] = useState([]);
  const [tab, setTab] = useState("daily");
  const [imagePreview, setImagePreview] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [dailyTotal, setDailyTotal] = useState(0);
  const [monthlyTotal, setMonthlyTotal] = useState(0);

  useEffect(() => {
    fetchRecords(tab);
    fetchSummaryTotals();
  }, [tab]);

  async function handleUpload(e) {
    e.preventDefault();
    if (!file) return alert("Please select an image first.");
    setLoading(true);

    const form = new FormData();
    form.append("image", file);

    try {
      const data = await apiFetch("/upload/", { method: "POST", body: form });

      if (!data.detected_items || data.detected_items.length === 0) {
        alert("No food items detected.");
        setDetectedItems([]);
      } else {
        setDetectedItems(
          data.detected_items.map((name) => ({
            food_item: name,
            servings: "",
            weight_in_grams: "",
          }))
        );
      }
    } catch (err) {
      console.error(err);
      alert("Error detecting food items. Check backend.");
    } finally {
      setLoading(false);
    }
  }

  async function handleCalculateAndSave() {
    const invalid = detectedItems.some(
      (item) => !item.servings || !item.weight_in_grams
    );
    if (invalid) return alert("Please fill servings and weight for all items.");

    try {
      await apiFetch("/save_record/", {
        method: "POST",
        body: JSON.stringify({ items: detectedItems }),
        headers: { "Content-Type": "application/json" },
      });

      alert("Calories calculated and saved!");
      setDetectedItems([]);
      setFile(null);
      setImagePreview(null);
      fetchRecords(tab);
      fetchSummaryTotals();
    } catch (err) {
      console.error(err);
      alert("Error saving calorie data.");
    }
  }

  async function fetchRecords(currentTab) {
    try {
      const data = await apiFetch(`/records/?tab=${currentTab}`);
      setRecords(data);
    } catch (err) {
      console.error(err);
    }
  }

  async function fetchSummaryTotals() {
    try {
      const dailyData = await apiFetch(`/records/?tab=daily`);
      const monthlyData = await apiFetch(`/records/?tab=monthly`);

      const dailySum = dailyData.reduce(
        (acc, r) => acc + (r.total_calories || 0),
        0
      );
      const monthlySum = monthlyData.reduce(
        (acc, r) => acc + (r.total_calories || 0),
        0
      );

      setDailyTotal(dailySum);
      setMonthlyTotal(monthlySum);
    } catch (err) {
      console.error("Error fetching summary totals:", err);
    }
  }

  function updateItem(index, field, value) {
    setDetectedItems((prev) =>
      prev.map((item, i) => (i === index ? { ...item, [field]: value } : item))
    );
  }

  function handleFileChange(e) {
    const f = e.target.files[0];
    setFile(f);
    if (f) setImagePreview(URL.createObjectURL(f));
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
      const f = e.dataTransfer.files[0];
      setFile(f);
      setImagePreview(URL.createObjectURL(f));
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-bold text-white">Calorie Tracker</h1>
            <p className="text-slate-400 mt-2">Upload meals and track your nutrition</p>
          </div>
          <button
            onClick={onLogout}
            className="px-5 py-2.5 bg-slate-800/50 backdrop-blur text-white rounded-xl hover:bg-slate-700/50 border border-slate-700/50 transition"
          >
            Logout
          </button>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700/50 shadow-xl">
            <h4 className="text-slate-400 text-sm mb-1">Today's Calories</h4>
            <p className="text-3xl font-semibold text-blue-400">{dailyTotal.toFixed(0)} cal</p>
          </div>
          <div className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700/50 shadow-xl">
            <h4 className="text-slate-400 text-sm mb-1">This Month's Calories</h4>
            <p className="text-3xl font-semibold text-green-400">{monthlyTotal.toFixed(0)} cal</p>
          </div>
        </div>

        {/* Upload Section */}
        <div className="bg-slate-800/40 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border border-slate-700/50">
          <h3 className="text-xl font-semibold text-white mb-6">Upload Meal Photo</h3>

          <div
            className={`border-2 border-dashed rounded-2xl p-10 text-center transition-all ${
              dragActive
                ? "border-blue-500 bg-blue-500/5"
                : "border-slate-600/50 hover:border-slate-500/50 bg-slate-900/20"
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            {imagePreview ? (
              <div className="space-y-4">
                <img
                  src={imagePreview}
                  alt="Preview"
                  className="max-h-48 max-w-full mx-auto rounded-xl object-contain shadow-lg"
                />
                <p className="text-green-400 font-medium text-sm">{file?.name}</p>
                <button
                  onClick={() => {
                    setFile(null);
                    setImagePreview(null);
                  }}
                  className="text-slate-400 hover:text-white text-sm transition"
                >
                  Remove
                </button>
              </div>
            ) : (
              <div className="space-y-4">
                <svg
                  className="w-16 h-16 text-slate-500 mx-auto"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1.5}
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
                <div>
                  <p className="text-slate-300 mb-2">Drag and drop your meal photo here</p>
                  <p className="text-slate-500 text-sm mb-4">or</p>
                  <label className="cursor-pointer px-6 py-3 bg-blue-600 text-white rounded-xl inline-block hover:bg-blue-700 transition shadow-lg">
                    Browse Files
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleFileChange}
                      className="hidden"
                    />
                  </label>
                </div>
              </div>
            )}
          </div>

          <button
            onClick={handleUpload}
            disabled={loading || !file}
            className="w-full mt-6 bg-blue-600 text-white py-3.5 rounded-xl hover:bg-blue-700 disabled:bg-slate-700/50 disabled:cursor-not-allowed transition shadow-lg font-medium"
          >
            {loading ? "Analyzing..." : "Detect Food Items"}
          </button>
        </div>

        {/* Detected Items */}
        {detectedItems.length > 0 && (
          <div className="bg-slate-800/40 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border border-slate-700/50">
            <h3 className="text-xl font-semibold text-white mb-6">Detected Items</h3>
            <div className="space-y-4">
              {detectedItems.map((item, i) => (
                <div key={i} className="bg-slate-900/40 rounded-xl p-5 border border-slate-700/30">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
                    <div>
                      <p className="text-sm text-slate-400 mb-1">Food Item</p>
                      <p className="text-white font-medium">{item.food_item}</p>
                    </div>
                    <div>
                      <label className="text-sm text-slate-400 block mb-2">Servings</label>
                      <input
                        type="number"
                        min="1"
                        value={item.servings}
                        onChange={(e) => updateItem(i, "servings", e.target.value)}
                        className="w-full px-4 py-2.5 bg-slate-800 border border-slate-600 rounded-lg text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                        placeholder="1"
                      />
                    </div>
                    <div>
                      <label className="text-sm text-slate-400 block mb-2">Weight (grams)</label>
                      <input
                        type="number"
                        min="1"
                        value={item.weight_in_grams}
                        onChange={(e) => updateItem(i, "weight_in_grams", e.target.value)}
                        className="w-full px-4 py-2.5 bg-slate-800 border border-slate-600 rounded-lg text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                        placeholder="100"
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <button
              onClick={handleCalculateAndSave}
              className="mt-6 w-full bg-green-600 text-white py-3.5 rounded-xl hover:bg-green-700 transition shadow-lg font-medium"
            >
              Save & Calculate Calories
            </button>
          </div>
        )}

        {/* Past Records */}
        <div className="bg-slate-800/40 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border border-slate-700/50">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl font-semibold text-white">Meal History</h3>
            <div className="flex gap-2">
              {["daily", "weekly", "monthly"].map((t) => (
                <button
                  key={t}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                    tab === t
                      ? "bg-blue-600 text-white shadow-lg"
                      : "bg-slate-800/50 text-slate-400 hover:text-white hover:bg-slate-700/50"
                  }`}
                  onClick={() => setTab(t)}
                >
                  {t.charAt(0).toUpperCase() + t.slice(1)}
                </button>
              ))}
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="text-left border-b border-slate-700/50">
                  <th className="pb-3 text-sm font-medium text-slate-400">Date</th>
                  <th className="pb-3 text-sm font-medium text-slate-400">Food</th>
                  <th className="pb-3 text-sm font-medium text-slate-400 text-center">Servings</th>
                  <th className="pb-3 text-sm font-medium text-slate-400 text-center">Weight (g)</th>
                  <th className="pb-3 text-sm font-medium text-slate-400 text-right">Calories</th>
                </tr>
              </thead>
              <tbody>
                {records.length > 0 ? (
                  records.map((r) => (
                    <tr key={r.id} className="border-b border-slate-700/30 hover:bg-slate-900/20">
                      <td className="py-4 text-slate-300 text-sm">
                        {new Date(r.date).toLocaleDateString()}
                      </td>
                      <td className="py-4 text-white font-medium">{r.food_item}</td>
                      <td className="py-4 text-slate-300 text-center">{r.servings}</td>
                      <td className="py-4 text-slate-300 text-center">{r.weight_in_grams}</td>
                      <td className="py-4 text-blue-400 font-semibold text-right">
                        {r.total_calories?.toFixed(0)} cal
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={5} className="py-8 text-center text-slate-500">
                      No records found
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}