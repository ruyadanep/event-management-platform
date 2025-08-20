import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar from './Navbar';

const MessageForm = () => {
  const [recipients, setRecipients] = useState([]);
  const [recipientId, setRecipientId] = useState(localStorage.getItem('reply_to_id') || '');
  const [subject, setSubject] = useState(localStorage.getItem('reply_to_subject') || '');
  const [body, setBody] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    axios.get('http://127.0.0.1:8000/api/v1/users/', {
      headers: { Authorization: `Token ${token}` }
    })
    .then(res => setRecipients(res.data.filter(u => u.username !== localStorage.getItem('username'))))
    .catch(err => console.error(err));
  }, []);

  const handleSubmit = e => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    axios.post('http://127.0.0.1:8000/api/v1/messages/send/', {
      recipient: recipientId,
      subject,
      body
    }, {
      headers: { Authorization: `Token ${token}` }
    })
    .then(() => {
      setMessage('✅ Message sent!');
      setRecipientId('');
      setSubject('');
      setBody('');
      localStorage.removeItem('reply_to_id');
      localStorage.removeItem('reply_to_subject');
      localStorage.removeItem('reply_to_username');
    })
    .catch(() => setMessage('❌ Failed to send message.'));
  };

  return (
    <>
      <Navbar />
      <div className="container py-4">
        <h3 className="mb-4">📤 Send a Message</h3>
        {localStorage.getItem('reply_to_username') && (
          <div className="alert alert-info">
            Replying to <strong>{localStorage.getItem('reply_to_username')}</strong>
          </div>
        )}
        {message && <div className="alert alert-info">{message}</div>}
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Recipient</label>
            <select className="form-select" value={recipientId} onChange={e => setRecipientId(e.target.value)} required>
              <option value="">-- Select Recipient --</option>
              {recipients.map(user => (
                <option key={user.id} value={user.id}>{user.username}</option>
              ))}
            </select>
          </div>
          <div className="mb-3">
            <label className="form-label">Subject</label>
            <input type="text" className="form-control" value={subject} onChange={e => setSubject(e.target.value)} required />
          </div>
          <div className="mb-3">
            <label className="form-label">Message</label>
            <textarea className="form-control" rows="4" value={body} onChange={e => setBody(e.target.value)} required />
          </div>
          <button className="btn btn-primary">Send</button>
        </form>
      </div>
    </>
  );
};

export default MessageForm;
