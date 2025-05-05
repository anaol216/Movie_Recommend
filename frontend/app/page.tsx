// pages/index.tsx

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
      const res = await fetch(`http://localhost:8000/recommend?video_id=${selectedId}`);
      const data = await res.json();
      setRecommendations(data);
    } catch (error) {
      console.error('Failed to fetch recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center px-4">
      <h1 className="text-3xl font-bold mb-6">🎬 Movie Recommender</h1>

      <input
        type="text"
        placeholder="Enter Video ID"
        value={selectedId}
        onChange={(e) => setSelectedId(e.target.value)}
        className="p-2 rounded text-black w-64 mb-4"
      />

      <button
        onClick={handleFetch}
        className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded"
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
  );
}
