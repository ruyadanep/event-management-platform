import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from './Navbar';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

const Events = () => {
  const [events, setEvents] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    axios.get('http://127.0.0.1:8000/api/v1/events/', {
      headers: { Authorization: `Token ${token}` },
    })
    .then(res => setEvents(res.data))
    .catch(err => console.error(err));
  }, []);

  const openModal = (event) => {
    setSelectedEvent(event);
    const modal = new window.bootstrap.Modal(document.getElementById('eventModal'));
    modal.show();
  };

  const handleRSVP = () => {
    const token = localStorage.getItem('token');
    axios.post('http://127.0.0.1:8000/api/v1/attendance/rsvp/', {
      event: selectedEvent.id
    }, {
      headers: { Authorization: `Token ${token}` }
    })
    .then(() => {
      const updated = events.map(e =>
        e.id === selectedEvent.id ? { ...e, has_rsvped: true } : e
      );
      setEvents(updated);
      setSelectedEvent({ ...selectedEvent, has_rsvped: true });
    })
    .catch(err => {
      console.error(err);
      alert('RSVP failed. Please try again.');
    });
  };

  return (
    <>
      <Navbar />
      <div className="container py-5">
        <h2 className="mb-4 text-primary">All Events</h2>
        {events.length === 0 ? (
          <div className="alert alert-warning">No events available.</div>
        ) : (
          <div className="row row-cols-1 row-cols-md-2 g-4">
            {events.map(event => (
              <div key={event.id} className="col">
                <div
                  className="card h-100 shadow-sm event-card"
                  onClick={() => openModal(event)}
                  style={{ cursor: 'pointer' }}
                >
                  <div className="card-body">
                    <h5 className="card-title">
                      {event.title}
                      {event.has_rsvped && (
                        <span className="badge bg-success ms-2">✓ RSVP’d</span>
                      )}
                    </h5>
                    <p className="card-text">{event.description.slice(0, 100)}...</p>
                    <ul className="list-unstyled small text-muted">
                      <li><strong>Starts:</strong> {new Date(event.start_date).toLocaleString()}</li>
                      <li><strong>Ends:</strong> {new Date(event.end_date).toLocaleString()}</li>
                    </ul>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Event Modal */}
      <div
        className="modal fade"
        id="eventModal"
        tabIndex="-1"
        aria-labelledby="eventModalLabel"
        aria-hidden="true"
      >
        <div className="modal-dialog modal-lg modal-dialog-centered">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title" id="eventModalLabel">
                {selectedEvent?.title}
                {selectedEvent?.has_rsvped && (
                  <span className="badge bg-success ms-2">✓ RSVP’d</span>
                )}
              </h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" />
            </div>
            <div className="modal-body">
              <p><strong>Description:</strong> {selectedEvent?.description}</p>
              <p><strong>Location:</strong> {selectedEvent?.location}</p>
              <p><strong>Start Date:</strong> {new Date(selectedEvent?.start_date).toLocaleString()}</p>
              <p><strong>End Date:</strong> {new Date(selectedEvent?.end_date).toLocaleString()}</p>
            </div>
            <div className="modal-footer">
              <button className="btn btn-secondary" data-bs-dismiss="modal">
                Close
              </button>
              {!selectedEvent?.has_rsvped && (
                <button className="btn btn-primary" onClick={handleRSVP}>
                  RSVP Now
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Events;
