import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from './Navbar';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

const RSVPForm = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) return navigate('/login');

    axios.get('http://127.0.0.1:8000/api/v1/events/', {
      headers: { Authorization: `Token ${token}` }
    })
    .then(res => {
      setEvents(res.data);
      setLoading(false);
    })
    .catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, [navigate]);

  const handleRSVP = (eventId) => {
    const token = localStorage.getItem('token');
    axios.post('http://127.0.0.1:8000/api/v1/attendance/', {
      event: eventId
    }, {
      headers: { Authorization: `Token ${token}` }
    })
    .then(() => {
      showToast("🎉 RSVP successful!");
    })
    .catch(() => {
      showToast("⚠️ Already RSVP’d or something went wrong.", true);
    });
  };

  const showToast = (msg, isError = false) => {
    const toastContainer = document.createElement("div");
    toastContainer.className = `toast align-items-center text-white ${isError ? 'bg-danger' : 'bg-success'} border-0 position-fixed top-0 end-0 m-4`;
    toastContainer.setAttribute('role', 'alert');
    toastContainer.setAttribute('aria-live', 'assertive');
    toastContainer.setAttribute('aria-atomic', 'true');
    toastContainer.innerHTML = `
      <div class="d-flex">
        <div class="toast-body">
          ${msg}
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
    `;
    document.body.appendChild(toastContainer);

    const toast = new bootstrap.Toast(toastContainer);
    toast.show();

    setTimeout(() => {
      toastContainer.remove();
    }, 4000);
  };

  if (loading) return <div className="text-center mt-5">Loading events...</div>;

  return (
    <>
      <Navbar />
      <div className="container py-5">
        <h2 className="mb-4 text-primary">Available Events</h2>
        {events.length === 0 ? (
          <div className="alert alert-warning">No upcoming events found.</div>
        ) : (
          <div className="row">
            {events.map(event => (
              <div className="col-md-6 mb-4" key={event.id}>
                <div className="card shadow-sm">
                  <div className="card-body">
                    <h5 className="card-title">{event.title}</h5>
                    <p className="card-text">{event.description}</p>
                    <p><strong>Date:</strong> {new Date(event.start_date).toLocaleString()} to {new Date(event.end_date).toLocaleString()}</p>
                    <p><strong>Location:</strong> {event.location}</p>
                    <button className="btn btn-primary" onClick={() => handleRSVP(event.id)}>RSVP</button>
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

export default RSVPForm;
