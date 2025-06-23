import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function ProblemSettingPage() {
  const [problem, setProblem] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!problem.trim()) return;

    try {
      // For demo, we skip the API call and just navigate
      // In a real app, call your backend here
      // await fetch('/set_problem', ...)
      navigate('/conversation');
    } catch (error) {
      alert('Error setting problem');
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <h2>Set Your DSA Problem</h2>
      <form onSubmit={handleSubmit} style={{ marginTop: '20px' }}>
        <input
          type="text"
          value={problem}
          onChange={(e) => setProblem(e.target.value)}
          placeholder="Enter your problem"
          required
          style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
        />
        <button type="submit" style={{ padding: '10px 20px', background: '#4CAF50', color: 'white', border: 'none', borderRadius: '4px' }}>
          Start Tutoring
        </button>
      </form>
    </div>
  );
}

export default ProblemSettingPage;
