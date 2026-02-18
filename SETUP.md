# Setup Guide - API Backend

This guide will help you set up and run the API Backend on your local machine.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package manager (comes with Python)
- **Git** (optional) - For cloning the repository

### Verify Python Installation

Open a terminal/command prompt and run:
```bash
python --version
# or
python3 --version
```

You should see Python 3.8 or higher.

---

## 🚀 Quick Start (Windows)

### Method 1: Using the Start Script (Easiest)

1. **Navigate to the project folder**
   ```bash
   cd "API Backend"
   ```

2. **Run the start script**
   ```bash
   start.bat
   ```

   This script will:
   - Create a virtual environment
   - Install all dependencies
   - Start the API server

3. **Access the API**
   - Server will be running at: `http://127.0.0.1:5000`
   - Health check: `http://127.0.0.1:5000/health`

### Method 2: Manual Setup

Follow the detailed steps below.

---

## 🔧 Manual Setup Steps

### Step 1: Create Virtual Environment

Creating a virtual environment isolates project dependencies.

```bash
# Navigate to project directory
cd "API Backend"

# Create virtual environment
python -m venv venv
```

### Step 2: Activate Virtual Environment

**Windows (Command Prompt):**
```bash
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

With the virtual environment activated:

```bash
pip install -r requirements.txt
```

This installs:
- Flask - Web framework
- Flask-JWT-Extended - JWT authentication
- Flask-CORS - Cross-origin resource sharing
- python-dotenv - Environment variable management
- email-validator - Email validation

### Step 4: Run the Server

```bash
python app.py
```

You should see:
```
============================================================
API Backend Server Starting...
============================================================
Environment: Development
Server: http://127.0.0.1:5000
Health Check: http://127.0.0.1:5000/health
============================================================
```

---

## ✅ Verify Installation

### Option 1: Browser

Open your browser and go to:
```
http://127.0.0.1:5000/health
```

You should see:
```json
{
  "status": "success",
  "data": {
    "status": "healthy",
    "timestamp": "2026-02-18T10:30:00.000000",
    "version": "1.0.0"
  },
  "message": "API is running successfully"
}
```

### Option 2: Automated Test Script

In a **new terminal** (keep the server running):

```bash
# Activate virtual environment first
venv\Scripts\activate

# Run test script
python test_api.py
```

This will run comprehensive tests and show results.

### Option 3: cURL Command

```bash
curl http://127.0.0.1:5000/health
```

### Option 4: Postman

1. Open Postman
2. Import the collection: `API_Backend_Postman_Collection.json`
3. Run the "Health Check" request

---

## 🛠️ Configuration (Optional)

### Environment Variables

If you want to customize settings:

1. **Copy the example environment file:**
   ```bash
   copy .env.example .env
   ```

2. **Edit `.env` file:**
   ```
   SECRET_KEY=your-strong-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key-here
   FLASK_ENV=development
   FLASK_DEBUG=1
   ```

3. **Generate secure keys:**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

---

## 📚 Testing the API

### Using Postman

1. **Import the Collection**
   - File → Import
   - Select: `API_Backend_Postman_Collection.json`

2. **Run Requests in Order:**
   - Health Check
   - Login - Admin (saves token automatically)
   - Get All Users
   - Create User
   - etc.

### Using Python Script

The included test script verifies all functionality:

```bash
python test_api.py
```

### Using cURL

See `sample_requests_responses.json` for example cURL commands.

---

## 🐛 Troubleshooting

### Port 5000 Already in Use

**Error:** `Address already in use`

**Solution 1:** Stop the process using port 5000

**Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

**Solution 2:** Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Virtual Environment Activation Issues (Windows PowerShell)

**Error:** `execution of scripts is disabled on this system`

**Solution:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Module Not Found Errors

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
1. Ensure virtual environment is activated
2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Dependencies Installation Fails

**Error during pip install**

**Solution:**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Try installing again
pip install -r requirements.txt
```

---

## 📂 Project Structure

```
API Backend/
│
├── app.py                              # Main Flask application
├── config.py                           # Configuration settings
├── models.py                           # Data models and storage
├── validators.py                       # Input validation
├── responses.py                        # Response helpers
├── auth.py                             # Authentication/authorization
│
├── requirements.txt                    # Python dependencies
├── README.md                           # Main documentation
├── SETUP.md                            # This file
│
├── test_api.py                         # Automated test script
├── start.bat                           # Windows quick start script
│
├── sample_requests_responses.json     # API examples
├── API_Backend_Postman_Collection.json # Postman collection
│
├── .env.example                        # Environment variables template
└── .gitignore                          # Git ignore rules
```

---

## 🔄 Stopping the Server

Press `Ctrl + C` in the terminal where the server is running.

---

## 🔄 Resetting Data

The API includes a reset endpoint to restore initial data:

```bash
curl -X POST http://127.0.0.1:5000/reset
```

This is useful between test runs.

---

## 📖 Next Steps

1. ✅ **Read the API Documentation** - See `README.md`
2. ✅ **Review Sample Requests** - See `sample_requests_responses.json`
3. ✅ **Import Postman Collection** - Start testing
4. ✅ **Run Automated Tests** - Verify everything works
5. ✅ **Start Building Your Tests** - Practice API testing!

---

## 💡 Tips for Development

### Keep Server Running While Testing

Run the server in one terminal and use another terminal for testing:

**Terminal 1:**
```bash
cd "API Backend"
venv\Scripts\activate
python app.py
```

**Terminal 2:**
```bash
cd "API Backend"
venv\Scripts\activate
python test_api.py
```

### Auto-reload on Code Changes

Flask's debug mode (enabled by default) automatically reloads when you change code.

### View Logs

The server terminal shows all requests and errors in real-time.

---

## 🎓 Learning Resources

### Recommended Testing Tools

- **Postman** - GUI-based API testing
- **pytest** - Python testing framework
- **requests** - Python HTTP library
- **RestAssured** - Java API testing
- **Cypress** - JavaScript E2E testing

### Topics to Practice

1. **Positive Testing** - Valid inputs, happy paths
2. **Negative Testing** - Invalid inputs, error cases
3. **Boundary Testing** - Edge cases
4. **Authentication Testing** - Token validation
5. **Authorization Testing** - Role-based access
6. **Response Validation** - Schema, status codes
7. **Performance Testing** - Load testing

---

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify Python and pip versions
3. Ensure all dependencies are installed
4. Check that port 5000 is available

---

## ✨ Success Indicators

You know everything is working when:

- ✅ Server starts without errors
- ✅ Health check returns 200 OK
- ✅ You can login and get a token
- ✅ CRUD operations work correctly
- ✅ Validation errors return proper status codes
- ✅ Authorization rules are enforced

---

**Happy Testing! 🚀**

Need help? Review the comprehensive documentation in `README.md`
