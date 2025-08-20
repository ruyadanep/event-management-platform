# 🎉 Event Management Platform  

[![Next.js](https://img.shields.io/badge/Next.js-13-black?logo=next.js)](https://nextjs.org/)  
[![Django](https://img.shields.io/badge/Django-4.x-green?logo=django)](https://www.djangoproject.com/)  
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.x-38B2AC?logo=tailwind-css)](https://tailwindcss.com/)  
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-blue?logo=postgresql)](https://www.postgresql.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  

An **Event Management Platform** built with **Next.js (frontend)** and **Django (backend)**.  
Easily create, manage, and book events with a modern, responsive interface.  

---

## 🚀 Features  

- 🔐 Secure Authentication & Authorization (JWT / Session-based)  
- 📅 Create & Manage Events (title, description, location, date, tickets)  
- 🎟️ Event Registration & Ticketing System  
- 👥 User Profiles (organizers & attendees)  
- 🔍 Event Search & Filters  
- 📊 Admin Dashboard for analytics  
- 📱 Responsive UI with **TailwindCSS**  

---

## 🛠️ Tech Stack  

**Frontend:**  
- [Next.js](https://nextjs.org/) (React Framework)  
- [TailwindCSS](https://tailwindcss.com/) for styling  
- [Axios](https://axios-http.com/) for API requests  

**Backend:**  
- [Django](https://www.djangoproject.com/)  
- [Django REST Framework](https://www.django-rest-framework.org/)  
- [PostgreSQL](https://www.postgresql.org/) (can use MySQL/SQLite)  

**Others:**  
- JWT Authentication  
- Docker (optional)  

---

## ⚙️ Installation  

### 1. Clone the Repository  
```bash
git clone https://github.com/yourusername/event-management-platform.git
cd event-management-platform
```

### 2. Backend Setup (Django)  
```bash
cd backend
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
➡️ API available at: `http://127.0.0.1:8000/`  

### 3. Frontend Setup (Next.js)  
```bash
cd frontend
npm install
npm run dev
```
➡️ Frontend available at: `http://localhost:3000/`  

---

## 🔑 Environment Variables  

Create `.env` files:  

**Backend (`.env`):**  
```
SECRET_KEY=your_django_secret
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/eventdb
```

**Frontend (`.env.local`):**  
```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/api
```

---

## 📸 Screenshots (Optional)  

| Dashboard | Event Details | Booking |
|-----------|---------------|---------|
| ![Dashboard](screenshots/dashboard.png) | ![Event](screenshots/event.png) | ![Booking](screenshots/booking.png) |  

---

## 📌 Roadmap  

- [ ] Online Payments (paystack)  
- [ ] Google/Outlook Calendar Sync  
- [ ] Multi-language Support  
- [ ] Email & SMS Notifications  

---

## 🤝 Contributing  

Contributions are welcome! Fork the repo and submit a pull request.  

---

## 📜 License  

This project is licensed under the **MIT License**.  
