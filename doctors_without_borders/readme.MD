# Healthcare Appointment System API

## Overview
This is a RESTful API-first healthcare appointment system built using Django Rest Framework (DRF). The system enables patients to book appointments, allows doctors to manage consultations, supports real-time chat, and provides notifications. Future plans include implementing video consultations and a frontend using React.

## Features
### User Management
- Custom user model (`CustomUser`) with additional fields (e.g., `bio`, `profile_picture`, `role`, `phone_number`).
- Authentication using Django Rest Framework's token authentication.
- Role-based access control (Doctor, Patient).

### Appointments
- Patients can book appointments with available doctors.
- Doctors can view their assigned appointments.
- CRUD operations for managing appointments.
- Status tracking (Scheduled, Completed, Cancelled).

### Consultations
- Doctors can document consultations including:
  - Medical history
  - Examination findings
  - Investigations
  - Treatment plan
  - Prescriptions
  - Review dates
- Only assigned doctors can create consultations for their patients.
- Role-based filtering ensures proper access control.

### Notifications
- Automated notifications for:
  - New appointments
  - Consultation updates
- Uses Django signals to trigger notifications.
- Notifications marked as read upon viewing.

### Real-Time Chat
- WebSocket-based real-time chat using Django Channels.
- Patients and doctors can communicate via chat.
- Future support planned for video calls.

## Project Structure
```
/healthcare_project
│── users/                # User authentication and management
│── appointments/         # Appointments and consultations
│── notifications/        # Notification system
│── chat/                 # WebSocket-based real-time chat
│── healthcare_project/   # Core project files
│── manage.py             # Django management script
```

## Technologies Used
- **Backend:** Django, Django Rest Framework
- **Database:** PostgreSQL
- **Real-time:** Django Channels, WebSockets
- **Authentication:** DRF Token Authentication
- **Notifications:** Django Signals
- **Frontend (Planned):** React

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/healthcare-appointment-system.git
   cd healthcare-appointment-system
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Apply database migrations:
   ```sh
   python manage.py migrate
   ```
5. Create a superuser:
   ```sh
   python manage.py createsuperuser
   ```
6. Start the development server:
   ```sh
   python manage.py runserver
   ```

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/users/` | GET, POST | User registration and list |
| `/api/appointments/` | GET, POST | Book and list appointments |
| `/api/appointments/{id}/` | GET, PATCH, DELETE | Manage specific appointments |
| `/api/consultations/` | GET, POST | Create and list consultations |
| `/api/consultations/{id}/` | GET, PATCH, DELETE | Manage specific consultations |
| `/api/notifications/` | GET | View notifications |
| `/ws/chat/` | WebSocket | Real-time chat |

## Next Steps
- Implement video consultations using WebRTC.
- Build the frontend using React.
- Enhance the chat system with message persistence.

## Contributing
Feel free to contribute by submitting a pull request or opening an issue!

## License
This project is licensed under the MIT License.

---

### Notes
- Ensure WebSockets are running for real-time features.
- Use the Django admin panel to manage users and appointments.

---
**Developed by:** Your Name / Your Team

