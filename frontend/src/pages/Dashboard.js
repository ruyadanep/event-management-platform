import Navbar from '../components/Navbar';
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const [rsvpCount, setRsvpCount] = useState(0);
  const [upcomingEvents, setUpcomingEvents] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) return navigate('/login');

    const headers = { Authorization: `Token ${token}` };

    // Fetch user profile
    axios.get('http://127.0.0.1:8000/api/v1/profile/', { headers })
      .then(res => setUser(res.data))
      .catch(() => navigate('/login'));

    // Fetch RSVPs
    axios.get('http://127.0.0.1:8000/api/v1/attendance/', { headers })
      .then(res => setRsvpCount(res.data.length));

    // Fetch upcoming events
    axios.get('http://127.0.0.1:8000/api/v1/events/', { headers })
      .then(res => {
        const upcoming = res.data.filter(event =>
          new Date(event.start_date) >= new Date()
        );
        setUpcomingEvents(upcoming.slice(0, 3));
      });
  }, [navigate]);

  if (!user) return <div className="text-center mt-5">Loading dashboard...</div>;

  return (
    <>
      <Navbar />
      <div className="container py-5">
        <h2 className="mb-4">Welcome back, <span className="text-primary">{user.username}</span> 👋</h2>

        <div className="row mb-5">
          <div className="col-md-4 mb-3">
            <div className="card text-center shadow-sm border-0">
              <div className="card-body">
                <h5 className="card-title">🎟 RSVPs</h5>
                <p className="display-6 fw-bold text-primary">{rsvpCount}</p>
                <p className="text-muted">Total events you RSVP’d to</p>
              </div>
            </div>
          </div>

          <div className="col-md-4 mb-3">
            <div className="card text-center shadow-sm border-0">
              <div className="card-body">
                <h5 className="card-title">📅 Upcoming Events</h5>
                <p className="display-6 fw-bold text-success">{upcomingEvents.length}</p>
                <p className="text-muted">Happening soon</p>
              </div>
            </div>
          </div>

          <div className="col-md-4 mb-3">
            <div className="card text-center shadow-sm border-0">
              <div className="card-body">
                <h5 className="card-title">👤 Profile</h5>
                <p className="fw-bold">{user.email}</p>
                <p className="text-muted">User ID: {user.id}</p>
              </div>
            </div>
          </div>
        </div>

        <h4 className="mb-3">Upcoming Events</h4>
        {upcomingEvents.length === 0 ? (
          <div className="alert alert-info">No upcoming events.</div>
        ) : (
          <div className="row">
            {upcomingEvents.map(event => (
              <div className="col-md-6 mb-4" key={event.id}>
                <div className="card shadow-sm h-100">
                  <div className="card-body">
                    <h5 className="card-title">{event.title}</h5>
                    <p className="card-text">{event.description}</p>
                    <p><strong>Date:</strong> {new Date(event.start_date).toLocaleString()} - {new Date(event.end_date).toLocaleString()}</p>
                    <p><strong>Location:</strong> {event.location}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
};

export default Dashboard;
