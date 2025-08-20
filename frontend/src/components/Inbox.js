import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from './Navbar';

const Inbox = () => {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    axios.get('http://127.0.0.1:8000/api/v1/messages/inbox/', {
      headers: { Authorization: `Token ${token}` }
    })
    .then(res => setMessages(res.data))
    .catch(err => console.error(err));
  }, []);

  const handleReply = (msg) => {
    localStorage.setItem('reply_to_id', msg.sender);
    localStorage.setItem('reply_to_username', msg.sender_username);
    localStorage.setItem('reply_to_subject', `Re: ${msg.subject}`);
    window.location.href = '/send-message';
  };

  const handleDelete = (id) => {
    const token = localStorage.getItem('token');
    if (!window.confirm('Are you sure you want to delete this message?')) return;

    axios.delete(`http://127.0.0.1:8000/api/v1/messages/delete/${id}/`, {
      headers: { Authorization: `Token ${token}` }
    })
    .then(() => {
      setMessages(prev => prev.filter(m => m.id !== id));
    })
    .catch(err => console.error('Delete failed:', err));
  };

  return (
    <>
      <Navbar />
      <div className="container py-4">
        <h3 className="mb-4">📥 Inbox</h3>
        {messages.length === 0 ? (
          <div className="alert alert-warning">No messages yet.</div>
        ) : (
          <div className="list-group">
            {messages.map(msg => (
              <div key={msg.id} className="list-group-item">
                <h5 className="mb-1">{msg.subject}</h5>
                <p className="mb-1">{msg.body}</p>
                <small>From: {msg.sender_username} • {new Date(msg.sent_at).toLocaleString()}</small>
                <div className="d-flex gap-2 mt-2">
                  <button className="btn btn-sm btn-outline-primary" onClick={() => handleReply(msg)}>Reply</button>
                  <button className="btn btn-sm btn-outline-danger" onClick={() => handleDelete(msg.id)}>Delete</button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
};

export default Inbox;
