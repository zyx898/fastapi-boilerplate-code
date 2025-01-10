# FastAPI Backend Template/Boilerplate 
# For Quick Start with FastAPI with MongoDB and Redis


## Setup

### Prerequisites
- Python 3.10 or higher

### Database
- Redis
- MongoDB


### Installation Steps
1. Create a virtual environment:
   ```bash
   python -m venv env
   ```

2. Activate the virtual environment:
   ```bash
   source env/bin/activate   # On Linux/macOS
   .\env\Scripts\activate    # On Windows
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   uvicorn backend.main:app --reload
   ```

5. Export Requirements (When adding new libraries to the project)
   ```bash
   pip freeze > requirements.txt
   ```






## Project Structure

### 🌐 API Layer
The API layer follows a modular and scalable architecture designed for optimal organization and maintainability.

#### /api
- **router.py**
  - Core router implementation
  - Handles API route registration and management
  - Provides unified access point for all endpoints

- **/endpoints**
  - 📦 **/products**
    - Extensible design for additional marketplace integrations
  
  - 🗂️ **/category** 
    - Supports seamless addition of new category providers

The API layer implements RESTful best practices with clear separation of concerns. Each endpoint module is self-contained with dedicated route handlers, input validation, and error handling.




---



### 🤖 Background Processing
Asynchronous task processing framework for data collection and analysis.

#### /background_task
- **/any_task_name**
  - **any_task_name.py** - Any task name

- **/any_task_name**
  - **any_task_name.py** - Any task name

The background task system is built for reliability and scalability, with robust error handling and automatic retries. New task types can be easily integrated through the modular architecture.


---

### 🔐 Core System Components
Core system functionality and configuration management.

#### /core
- **config.py**
  - Environment-specific configuration management
  - System-wide settings and parameters
  - Secure credential handling

- **initialization.py**
  - Application startup and shutdown procedures
  - Database connection management
  - Logging system initialization

- **loggerConfig.py**
  - Centralized logging configuration
  - Log rotation and retention policies
  - Error tracking and monitoring

---

### 📚 CRUD
- **any_crud.py**
  - Any CRUD operations
  - Anything that has to do with database operations for any_task_name

---

### 📚 Database
- **db/redis/redis_client.py**
  - Redis client configuration and connection
- **db/mongodb/mongodb_client.py**
  - MongoDB client configuration and connection


--- 

### Schemas
- **schemas/any_task_name.py**
  - Any data models and validation schemas


---

### Services
- **services/any_service.py**
  - Any service implementation

---

### Tests
- **tests/test_any_task_name.py**
  - Test any_task_name

---


### Dependencies
- **requirements.txt**
  - List of dependencies

---

### Main
- **main.py**
  - Application entry point
  - API server initialization
  - Background task scheduling

