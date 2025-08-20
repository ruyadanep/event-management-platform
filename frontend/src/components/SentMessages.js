import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from './Navbar';

const SentMessages = () => {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    axios.get('http://127.0.0.1:8000/api/v1/messages/sent/', {
      headers: { Authorization: `Token ${token}` }
    })
    .then(res => setMessages(res.data))
    .catch(err => console.error(err));
  }, []);

  return (
    <>
      <Navbar />
      <div className="container py-4">
        <h3 className="mb-4">📤 Sent Messages</h3>
        {messages.length === 0 ? (
          <div className="alert alert-info">You haven’t sent any messages yet.</div>
        ) : (
          <div className="list-group">
            {messages.map(msg => (
              <div key={msg.id} className="list-group-item">
                <h5>{msg.subject}</h5>
                <p>{msg.body}</p>
                <small>To: {msg.recipient_username} • {new Date(msg.sent_at).toLocaleString()}</small>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
};

export default SentMessages;
