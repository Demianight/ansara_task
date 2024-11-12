# Task Tracker API

## Overview

This project is a simple task tracking API that enables users to create, manage, and update tasks, with support for detailed status tracking and comments. Users can create accounts, authenticate, and track task changes over time, while each task can have multiple statuses updated by various users. 

### Key Features

- **User Management**: Users can create accounts, log in, and obtain tokens to access protected endpoints.
- **Task Management**: Users can create, view, update, and delete tasks. Tasks are defined with descriptions and have status updates associated with specific users.
- **Status History**: Each task status can be changed, with all changes logged for tracking purposes. Users and timestamps are recorded to provide a complete status history.
- **Comments**: Users can comment on tasks, enabling discussion or additional task context. Comments can be deleted by authorized users (only in testing purposes).
  
## Authentication

All protected endpoints require JWT tokens. Users can obtain a token by submitting valid credentials via the login endpoint. <br>
Each user is assigned a token, which must be included in requests to access or modify data securely.

## API Endpoints Overview

### Users

- **Register**: Allows new users to register by providing a username and password.
- **Login**: Authenticates users and returns a token.

### Tasks

- **Create Task**: Allows authorized users to create tasks, including an initial description and status.
- **View Tasks**: Retrieve a list of all tasks or view individual tasks by ID.
- **Update Task**: Allows task owners or authorized users to modify tasks.
- **Delete Task**: Tasks can be deleted by authorized users if they are no longer needed.

### Task Status History

- **Add Status**: Users can update task status, which is logged with the user, date, and status.
- **Delete Status History**: Status history entries can be removed if they were made in error.

### Comments

- **Add Comment**: Users can add comments to tasks to provide additional context or discuss task details.
- **View Comments**: Allows users to view all comments associated with a task.
- **Delete Comment**: Authorized users can remove comments if necessary.

---

## Setup

This API is designed for deployment on a local server. To run the project:

Run ```docker-compose up --build```, it will pull, initialize and configure the db and Django app. </br>
Access endpoints via the base URL: http://127.0.0.1:8000/api
