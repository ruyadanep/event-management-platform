import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import RSVPForm from './components/RSVPForm'; // adjust path if needed
import Login from './components/Login';
import Navbar from './components/Navbar';
import MyRSVPs from './components/MyRSVPs';
import Dashboard from './pages/Dashboard'; // ✅ from pages
import Profile from './pages/Profile';     // ✅ from pages
import Events from './components/Events'; // adjust if your folder is named `components`
import Inbox from './components/Inbox';
import MessageForm from './components/MessageForm'; 
import SentMessages from './components/SentMessages';  // ✅ adjust path if needed






function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/my-rsvps" element={<MyRSVPs />} /> {/* ✅ New route */}
        <Route path="/events" element={<Events />} />
        <Route path="/rsvp" element={<RSVPForm />} />
        <Route path="/inbox" element={<Inbox />} />
        <Route path="/send-message" element={<MessageForm />} />
        <Route path="/sent" element={<SentMessages />} />



      </Routes>
    </Router>
  );
}

export default App;
