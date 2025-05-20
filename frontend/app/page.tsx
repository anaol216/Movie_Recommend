"use client";

import React, { useState } from 'react';

type Recommendation = {
  video_id: number;
  video_type: string;
  music_type: string;
  tag: string;
};

export default function Home() {
  const [selectedId, setSelectedId] = useState('');
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(false);

  const handleFetch = async () => {
    if (!selectedId) return;
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/recommend/${selectedId}`);

      const data = await res.json();
      setRecommendations(data);
    } catch (error) {
      console.error('Failed to fetch recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="min-h-screen bg-gray-900 text-white px-4 relative flex items-center justify-center"
      style={{
        backgroundImage: "url('/background.jpg')",
        backgroundSize: 'cover',
        backgroundPosition: 'center',
      }}
    >
      {/* 🔲 Background Overlay */}
      <div className="absolute inset-0 bg-black opacity-50 z-0" />

      {/* 🔳 Foreground UI */}
      <div className="z-10 flex flex-col items-center">
        <h1 className="text-3xl font-bold mb-6">🎬 Movie Recommender</h1>

        <input
          type="text"
          placeholder="Enter Video ID"
          value={selectedId}
          onChange={(e) => setSelectedId(e.target.value)}
          className="p-2 rounded text-black w-64 mb-4 bg-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />

        <button
          onClick={handleFetch}
          className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded transition"
        >
          🔍 Show Recommendations
        </button>

        {loading && <p className="mt-4">Loading...</p>}

        <div className="mt-8 w-full max-w-xl">
          {recommendations.map((rec, i) => (
            <div key={i} className="bg-gray-800 rounded p-4 mb-4 shadow">
              <h2 className="text-xl font-semibold mb-2">🎬 Recommendation {i + 1}</h2>
              <p><strong>Video ID:</strong> {rec.video_id}</p>
              <p><strong>Video Type:</strong> {rec.video_type}</p>
              <p><strong>Music Type:</strong> {rec.music_type}</p>
              <p><strong>Tag:</strong> {rec.tag}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
