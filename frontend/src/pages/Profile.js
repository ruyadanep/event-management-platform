import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

const Profile = () => {
  const [user, setUser] = useState(null);
  const [rsvpCount, setRsvpCount] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) return navigate('/login');

    // Fetch user profile
    axios.get('http://127.0.0.1:8000/api/v1/profile/', {
      headers: { Authorization: `Token ${token}` }
    })
    .then(res => setUser(res.data))
    .catch(err => console.error('User fetch error:', err));

    // Fetch RSVP count
    axios.get('http://127.0.0.1:8000/api/v1/attendance/', {
      headers: { Authorization: `Token ${token}` }
    })
    .then(res => setRsvpCount(res.data.length))
    .catch(err => console.error('RSVP fetch error:', err));
  }, [navigate]);

  if (!user) return <div className="text-center mt-5">Loading profile...</div>;

  return (
    <>
    
      <div className="container py-5">
        <div className="card shadow-sm p-4">
          <h3 className="mb-4 text-primary">👤 Profile Overview</h3>
          <ul className="list-group list-group-flush mb-4">
            <li className="list-group-item"><strong>Username:</strong> {user.username}</li>
            <li className="list-group-item"><strong>Email:</strong> {user.email}</li>
            <li className="list-group-item"><strong>User ID:</strong> {user.id}</li>
            <li className="list-group-item"><strong>Total RSVPs:</strong> {rsvpCount}</li>
          </ul>
          <button className="btn btn-outline-primary rounded-pill">Update Profile (Coming Soon)</button>
        </div>
      </div>
    </>
  );
};

export default Profile;
