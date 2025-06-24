import React, { useState } from 'react';
import './styles.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [featureInput, setFeatureInput] = useState('');

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages([...messages, userMessage]);
    setInput('');

    try {
      const response = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      });
      const data = await response.json();
      if (data.message) {
        setMessages((prev) => [...prev, { role: 'assistant', content: data.message }]);
      } else {
        console.error('Error:', data.error);
      }
    } catch (error) {
      console.error('Fetch error:', error);
    }
  };

  const proposeFeature = async () => {
    if (!featureInput.trim()) return;

    try {
      const response = await fetch('http://localhost:5000/api/propose_feature', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ feature: featureInput }),
      });
      const data = await response.json();
      alert(data.message + ` Change ID: ${data.change_id}`);
      setFeatureInput('');
    } catch (error) {
      console.error('Feature proposal error:', error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Sarah AI Chat</h1>
      <div className="chat-box border p-4 h-96 overflow-y-auto mb-4">
        {messages.map((msg, index) => (
          <div key={index} className={`mb-2 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
            <span className={`inline-block p-2 rounded ${msg.role === 'user' ? 'bg-blue-200' : 'bg-gray-200'}`}>
              {msg.content}
            </span>
          </div>
        ))}
      </div>
      <div className="flex mb-4">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-grow border p-2 rounded-l"
          placeholder="Type your message..."
        />
        <button onClick={sendMessage} className="bg-blue-500 text-white p-2 rounded-r">
          Send
        </button>
      </div>
      <div className="flex">
        <input
          type="text"
          value={featureInput}
          onChange={(e) => setFeatureInput(e.target.value)}
          className="flex-grow border p-2 rounded-l"
          placeholder="Propose a new feature..."
        />
        <button onClick={proposeFeature} className="bg-green-500 text-white p-2 rounded-r">
          Propose Feature
        </button>
      </div>
    </div>
  );
}

export default App;
