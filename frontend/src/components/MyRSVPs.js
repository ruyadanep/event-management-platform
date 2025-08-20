import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Navbar from './Navbar';
import Footer from './Footer';

const MyRSVPs = () => {
  const [rsvps, setRsvps] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState('upcoming');
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) return navigate('/login');

    axios.get('http://127.0.0.1:8000/api/v1/attendance/', {
      headers: { Authorization: `Token ${token}` },
    })
    .then(res => {
      setRsvps(res.data);
      setLoading(false);
    })
    .catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, [navigate]);

  useEffect(() => {
    const now = new Date();
    let filteredData = rsvps;

    if (filter === 'upcoming') {
      filteredData = filteredData.filter(rsvp => new Date(rsvp.event.start_date) >= now);
    } else if (filter === 'past') {
      filteredData = filteredData.filter(rsvp => new Date(rsvp.event.end_date) < now);
    }

    if (search.trim()) {
      filteredData = filteredData.filter(rsvp =>
        rsvp.event.title.toLowerCase().includes(search.toLowerCase())
      );
    }

    setFiltered(filteredData);
  }, [search, filter, rsvps]);

  const downloadCSV = () => {
    const headers = ['Title', 'Description', 'Start Date', 'End Date', 'Location'];
    const rows = filtered.map(rsvp => [
      rsvp.event.title,
      rsvp.event.description,
      new Date(rsvp.event.start_date).toLocaleString(),
      new Date(rsvp.event.end_date).toLocaleString(),
      rsvp.event.location
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.map(item => `"${item}"`).join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'my_rsvps.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleCancel = (rsvpId) => {
    const token = localStorage.getItem('token');
    if (!window.confirm("Are you sure you want to cancel this RSVP?")) return;

    axios.delete(`http://127.0.0.1:8000/api/v1/attendance/cancel/${rsvpId}/`, {
      headers: { Authorization: `Token ${token}` }
    })
    .then(() => {
      setRsvps(prev => prev.filter(r => r.id !== rsvpId));
    })
    .catch(err => {
      console.error('Cancellation failed:', err);
      alert('Something went wrong.');
    });
  };

  if (loading) return <div className="text-center mt-5">Loading your RSVPs...</div>;

  return (
    <>
      <Navbar />
      <div className="container py-5">
        <h2 className="mb-4 text-primary">My RSVPs</h2>

        <div className="row mb-4">
          <div className="col-md-6">
            <input
              type="text"
              className="form-control"
              placeholder="🔍 Search by event title..."
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
          </div>
          <div className="col-md-6">
            <select
              className="form-select"
              value={filter}
              onChange={e => setFilter(e.target.value)}
            >
              <option value="upcoming">Upcoming Events</option>
              <option value="past">Past Events</option>
              <option value="all">All Events</option>
            </select>
          </div>
        </div>

        <div className="text-end mb-3">
          <button className="btn btn-outline-secondary" onClick={downloadCSV}>
            ⬇️ Download CSV
          </button>
        </div>

        {filtered.length === 0 ? (
          <div className="alert alert-info">No events match your filter.</div>
        ) : (
          <div className="table-responsive">
            <table className="table table-bordered table-hover">
              <thead className="table-light">
                <tr>
                  <th>Event Title</th>
                  <th>Description</th>
                  <th>Start Date</th>
                  <th>End Date</th>
                  <th>Location / Action</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((rsvp, index) => (
                  <tr key={index}>
                    <td>{rsvp.event.title}</td>
                    <td>{rsvp.event.description}</td>
                    <td>{new Date(rsvp.event.start_date).toLocaleString()}</td>
                    <td>{new Date(rsvp.event.end_date).toLocaleString()}</td>
                    <td>
                      {rsvp.event.location}
                      <br />
                      <button
                        className="btn btn-sm btn-outline-danger mt-2"
                        onClick={() => handleCancel(rsvp.id)}
                      >
                        Cancel
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </>
  );
};

export default MyRSVPs;
