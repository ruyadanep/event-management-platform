import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Navbar.css';
import axios from 'axios';


const Navbar = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) return;

    axios.get('http://127.0.0.1:8000/api/v1/user/', {
      headers: { Authorization: `Token ${token}` }
    })
    .then(res => setUser(res.data))
    .catch(() => setUser(null));
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <nav className="navbar navbar-expand-lg custom-navbar shadow-sm">
      <div className="container">
        <img src="/logo.svg" alt="" height="40" className="me-2" />
        <Link className="navbar-brand brand-logo" to="/dashboard">
          EventHive
        </Link>

        <button
          className="navbar-toggler border-0"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto align-items-center gap-2">
            {user && (
              <>
                <li className="nav-item">
                  <span className="nav-link custom-nav-link disabled">
                    👋 Hello, {user.username}
                  </span>
                </li>
                <li className="nav-item">
                  <Link className="nav-link custom-nav-link" to="/dashboard">Dashboard</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link custom-nav-link" to="/profile">Profile</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link custom-nav-link" to="/my-rsvps">My RSVPs</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link custom-nav-link" to="/rsvp">RSVP to Event</Link>
                </li>
                <li className="nav-item ms-2">
                  <button
                    className="btn btn-light btn-sm rounded-pill px-3 shadow-sm text-dark"
                    onClick={handleLogout}
                  >
                    Logout
                  </button>
                </li>
              </>
            )}
            {!user && (
              <li className="nav-item">
                <Link className="btn btn-light btn-sm px-3 rounded-pill shadow-sm text-dark" to="/login">
                  Login
                </Link>
              </li>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
