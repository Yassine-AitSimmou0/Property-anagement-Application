# Property Management Application

## Overview

The Property Management Application is a web-based solution for managing properties, tenants, and payments. It allows users to add, update, and delete properties, manage tenant information, and handle payment transactions. The application provides a RESTful API for backend operations and a React frontend for user interactions.

## Features

- **Properties Management:** Add, update, and delete property records. Manage property details including name, address, type, number of units, and rental cost.
- **Tenants Management:** Add, update, and delete tenant records. Manage tenant details including name, email, and associated property.
- **Payments Management:** Record and update payments, mark payments as settled, and delete payment records.

## Tech Stack

- **Frontend:**

  - React.js with TypeScript
  - Axios for API calls
  - Material-UI for UI components
  - React-Toastify for notifications

- **Backend:**

  - Flask with Flask-RESTx for RESTful API development
  - Flask-SQLAlchemy for ORM
  - PostgreSQL for database management
  - Marshmallow for schema validation

- **DevOps:**
  - Docker for containerization
  - Docker Compose for managing multi-container applications

## Project Structure

- **Backend:**

  - `app.py` - Initializes Flask, database, and API.
  - `models.py` - Defines SQLAlchemy models for Properties, Tenants, and Payments.
  - `routes/` - Contains Flask-RESTx route definitions for managing API endpoints.
  - `services/` - Contains service classes for handling business logic.
  - `validation/` - Contains Marshmallow schemas for data validation.

- **Frontend:**
  - `src/` - Contains React application source code.
  - `api/` - Contains Axios configuration and API service functions.
  - `components/` - Contains React components for UI.
  - `pages/` - Contains page components and routing logic.

## Setup and Installation

# Note: Make sure you have Docker and Docker Compose installed on your system.

# Note: Those secrets are not important for this project, but in a real-world scenario, you should never commit secrets to the repository.

# Note: The frontend may have some unfinished features.

# Clone the repository

```SHELL

$ git clone https://github.com/Yassine-AitSimmou0/Property-anagement-Application.git
```

# Change the directory

```SHELL

$ cd Property-Management-Application
```

# Run the application

```SHELL
$ docker-compose up --build
```

# To log in to the dashboard, use the following credentials:

- **email:** admin@test.com
- **Password:** adminadmin

# Access the application

Open your browser and visit `http://localhost:3000` to access the Property Management Application.
Open your browser and visit `http://localhost:5000` to access the API documentation.

# If you want to add more properties, tenants, or payments, you can use a script to populate the database with sample data.

```SHELL
docker exec -it property-management-app-backend-1 python generate_random_data.py
```
