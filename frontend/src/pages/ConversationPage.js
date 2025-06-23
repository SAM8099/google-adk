import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function ConversationPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const navigate = useNavigate();

  // Optional: Simulate initial conversation
  useEffect(() => {
    setMessages([
      { sender: 'tutor', text: 'Hello! Please answer my questions.' }
    ]);
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message
    setMessages((prev) => [...prev, { sender: 'user', text: input }]);
    // Simulate tutor response
    setMessages((prev) => [...prev, { sender: 'tutor', text: 'Thank you! Next question...' }]);
    setInput('');
  };

  const handleExit = () => {
    if (window.confirm('Are you sure you want to exit the session?')) {
      navigate('/');
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <h2>DSA Tutoring Session</h2>
      <div style={{ border: '1px solid #ccc', padding: '10px', height: '300px', overflowY: 'scroll', marginBottom: '10px' }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{ textAlign: msg.sender === 'tutor' ? 'left' : 'right', margin: '5px 0' }}>
            <b>{msg.sender === 'tutor' ? 'Tutor' : 'You'}:</b> {msg.text}
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} style={{ display: 'flex', marginBottom: '10px' }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your answer here"
          required
          style={{ flex: '1', padding: '10px', marginRight: '10px' }}
        />
        <button type="submit" style={{ padding: '10px 20px', background: '#4CAF50', color: 'white', border: 'none', borderRadius: '4px' }}>
          Send
        </button>
      </form>
      <button
        onClick={handleExit}
        style={{ padding: '10px 20px', background: '#f44336', color: 'white', border: 'none', borderRadius: '4px', width: '100%' }}
      >
        Exit Session
      </button>
    </div>
  );
}

export default ConversationPage;
