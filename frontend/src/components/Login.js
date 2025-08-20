import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Footer from './Footer';

const Login = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('/api/v1/login/', {
        username,
        password,
      });
      const { token } = res.data;
      localStorage.setItem('token', token);
      setToken(token);
      setError('');
      navigate('/dashboard');
    } catch (err) {
      setError('Invalid credentials');
    }
  };

  return (
    <div className="d-flex justify-content-center align-items-center min-vh-100 bg-light">
      <div className="card shadow-sm p-4" style={{ maxWidth: '400px', width: '100%' }}>
        <h2 className="text-center mb-4" style={{ color: '#4B0082' }}>EventHive Login</h2>
        <form onSubmit={handleLogin}>
          <div className="mb-3">
            <label className="form-label fw-semibold">Username</label>
            <input
              type="text"
              className="form-control"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              style={{ borderColor: '#4B0082' }}
            />
          </div>
          <div className="mb-3">
            <label className="form-label fw-semibold">Password</label>
            <input
              type="password"
              className="form-control"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              style={{ borderColor: '#4B0082' }}
            />
          </div>
          <button className="btn w-100 text-white" style={{ backgroundColor: '#4B0082' }} type="submit">
            Login
          </button>
          {error && <p className="text-danger text-center mt-3">{error}</p>}
        </form>
        {token && (
          <div className="alert alert-success mt-3">
            <strong>Token:</strong> {token}
          </div>
        )}
        <p className="text-center mt-4 small" style={{ color: '#FF6F61' }}>
          Powered by EventHive
        </p>
      </div>
    </div>
  );
};

export default Login;
