import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="event-footer text-white mt-5">
      <div className="container py-4">
        <div className="row">
          <div className="col-md-4 mb-3">
            <h5 className="footer-logo">EventHive</h5>
            <p>Your all-in-one platform for hosting, managing, and celebrating events.</p>
          </div>
          <div className="col-md-4 mb-3">
            <h6>Quick Links</h6>
            <ul className="list-unstyled">
              <li><a href="/dashboard">Dashboard</a></li>
              <li><a href="/events">Events</a></li>
              <li><a href="/profile">Profile</a></li>
              <li><a href="/my-rsvps">My RSVPs</a></li>
            </ul>
          </div>
          <div className="col-md-4 mb-3">
            <h6>Contact</h6>
            <p>Email: <a href="mailto:support@eventhive.com">support@eventhive.com</a></p>
            <p>Phone: +234 801 234 5678</p>
          </div>
        </div>
        <div className="text-center pt-3 border-top">
          <small>© {new Date().getFullYear()} EventHive. All rights reserved.</small>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
