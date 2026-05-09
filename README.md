# Task Management System

A comprehensive Task Management System built with Flask, PostgreSQL, REST APIs, WebSockets, and analytics using Pandas & NumPy.

## Features

### 1. **Authentication System**
- User Registration with email validation
- User Login with secure password hashing
- Logout Functionality
- Session management

### 2. **REST API Development**
- ✅ Add Task
- ✅ Update Task
- ✅ Delete Task
- ✅ Get All Tasks
- ✅ Get Single Task
- ✅ Filter by Status and Priority

### 3. **PostgreSQL Integration**
- Persistent user and task data storage
- Properly organized database schema
- Indexed queries for optimal performance
- Foreign key relationships

### 4. **Analytics Module**
Using Pandas & NumPy:
- Total Tasks Count
- Completed Tasks Count
- Pending Tasks Count
- Completion Percentage
- Priority Distribution
- Status Distribution
- Average Completion Time
- Tasks by Week
- Daily Trends

### 5. **WebSocket Feature**
- Real-time task updates
- Live notifications
- Instant UI refresh on task changes
- Room-based user isolation

### 6. **Responsive Frontend**
- Clean and intuitive HTML/CSS UI
- Mobile-responsive design
- Task management interface
- Analytics dashboard
- Real-time updates

## Tech Stack

- **Backend**: Flask, Python
- **Database**: PostgreSQL
- **APIs**: REST
- **Real-time**: WebSockets (Socket.IO)
- **Data Analysis**: Pandas, NumPy
- **Frontend**: HTML5, CSS3, JavaScript
- **Server**: Flask-SocketIO

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 10+
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/ankitsaini2015/task-management-system.git
cd task-management-system
```

### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup PostgreSQL Database

1. Create a database:
```sql
CREATE DATABASE task_management;
```

2. Run the schema:
```bash
psql -U postgres -d task_management -f migrations/schema.sql
```

### Step 5: Environment Configuration

Create a `.env` file in the root directory:
```
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_URL=postgresql://user:password@localhost:5432/task_management
DEBUG=True
```

### Step 6: Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /login` - Login user
- `GET /logout` - Logout user

### Tasks
- `GET /api/tasks` - Get all tasks (with optional filters)
  - Query params: `status`, `priority`
- `GET /api/tasks/<task_id>` - Get specific task
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/<task_id>` - Update task
- `DELETE /api/tasks/<task_id>` - Delete task

### Analytics
- `GET /api/analytics/summary` - Get analytics summary
- `GET /api/analytics/trends` - Get task trends

## WebSocket Events

### Client to Server
- `task_created` - Notify task creation
- `task_updated` - Notify task update
- `task_deleted` - Notify task deletion
- `get_notifications` - Request notifications
- `analytics_request` - Request analytics update

### Server to Client
- `connection_response` - Connection confirmation
- `task_update` - Real-time task update
- `notifications` - Notification data
- `analytics_update` - Analytics data

## Project Structure

```
task-management-system/
├── app.py                 # Main application factory
├── config.py              # Configuration settings
├── database.py            # Database models
├── auth.py                # Authentication routes
├── tasks.py               # Task API routes
├── analytics.py           # Analytics routes
├── websocket_events.py    # WebSocket event handlers
├── main.py                # Main routes (dashboard, tasks page)
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── migrations/
│   └── schema.sql         # Database schema
├── static/
│   ├── css/
│   │   └── style.css      # Main stylesheet
│   └── js/
│       ├── tasks.js       # Task management JS
│       └── websocket.js   # WebSocket client
├── templates/
│   ├── base.html          # Base template
│   ├── register.html      # Registration page
│   ├── login.html         # Login page
│   ├── dashboard.html     # Dashboard page
│   ├── tasks.html         # Tasks page
│   ├── 404.html           # 404 error page
│   └── 500.html           # 500 error page
└── README.md              # This file
```

## Usage Guide

### 1. Register a New Account
- Navigate to `/register`
- Fill in username, email, and password
- Password must be at least 6 characters with uppercase and digit
- Click "Register"

### 2. Login
- Navigate to `/login`
- Enter your credentials
- Click "Login"

### 3. Dashboard
- View your task statistics
- See real-time analytics
- Quick access to add tasks

### 4. Manage Tasks
- View all your tasks
- Filter by status or priority
- Create new tasks
- Edit existing tasks
- Delete tasks
- Change task status

### 5. View Analytics
- Total tasks overview
- Completion statistics
- Priority distribution
- Daily trends

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    priority VARCHAR(20) DEFAULT 'medium',
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    due_date TIMESTAMP
);
```

## Key Technologies & Concepts

### Flask
- Blueprints for modular organization
- Session management
- Error handling
- CORS support

### PostgreSQL
- Relational data modeling
- Indexes for performance
- Foreign key constraints
- Transaction support

### REST API
- CRUD operations
- Proper HTTP status codes
- JSON request/response
- Error handling

### WebSockets
- Real-time bidirectional communication
- Room-based message broadcasting
- Event-driven architecture

### Pandas & NumPy
- Data aggregation and analysis
- Statistical computations
- DataFrame operations
- Time-series analysis

## Performance Optimization

- Database indexes on frequently queried columns
- Lazy loading relationships
- Query filtering at database level
- Efficient WebSocket room management
- Caching analytics results

## Security Features

- Password hashing with Werkzeug
- Session-based authentication
- CSRF protection
- SQL injection prevention via ORM
- XSS protection via template escaping

## Troubleshooting

### Connection Refused
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env file
- Verify database credentials

### Module Not Found
- Activate virtual environment
- Run `pip install -r requirements.txt`
- Check Python version (3.8+)

### WebSocket Connection Issues
- Check if Socket.IO is properly initialized
- Ensure CORS settings are correct
- Check browser console for errors

## Demo

For a demonstration of all features, please refer to the demo video.

## Future Enhancements

- Task categories and tags
- Recurring tasks
- Task assignments
- Team collaboration
- File attachments
- Email notifications
- Mobile app
- Dark mode
- Task templates
- Advanced filtering and search

## Contributing

Feel free to fork this repository and submit pull requests.

## License

MIT License - feel free to use this project for any purpose.

## Support

For issues and questions, please create an issue in the GitHub repository.

## Author

Ankit Saini
- GitHub: [@ankitsaini2015](https://github.com/ankitsaini2015)

---

**Created**: 2026-05-09

**Status**: ✅ Complete and Running
