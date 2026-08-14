# Leave Management System

A cloud-based Leave Management System built to simplify the process of submitting, approving, rejecting, and tracking employee leave requests.

This project was developed as part of the **WeThinkCode_ WTC-F4CZ** elective proof of work.

## Overview

The Leave Management System provides employees and managers with a simple way to manage leave requests digitally.

Employees can:

* Submit leave requests
* View their leave balance
* View previous leave requests
* Track the status of submitted requests

Managers can:

* View pending leave requests
* Approve leave requests
* Reject leave requests

The application uses a serverless backend and a web-based frontend hosted through AWS services.

## Features

### Employee

* Employee login
* View leave balance
* Submit leave requests
* View leave request history
* Track request status

### Manager

* View pending leave requests
* Approve requests
* Reject requests
* Manage employee leave requests

## Technologies Used

### Frontend

* HTML
* CSS
* JavaScript
* React
* Vite

### Backend & Cloud

* AWS Lambda
* Amazon API Gateway
* Amazon Cognito
* AWS Amplify
* AWS services for serverless application deployment

### Development Tools

* Git
* GitHub
* Visual Studio Code
* npm

## Architecture

The application follows a serverless architecture.

```text
                    ┌──────────────────┐
                    │      User        │
                    │ Employee/Manager │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Frontend      │
                    │ React / Vite     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   API Gateway    │
                    └────────┬─────────┘
                             │
             ┌───────────────┼───────────────┐
             ▼               ▼               ▼
       ┌──────────┐    ┌──────────┐    ┌──────────┐
       │  Lambda  │    │  Lambda  │    │  Lambda  │
       │  Leave   │    │ Approval │    │  History │
       └──────────┘    └──────────┘    └──────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   AWS Services   │
                    └──────────────────┘
```

## API Endpoints

The backend provides endpoints for managing employee leave.

| Method | Endpoint                 | Purpose                           |
| ------ | ------------------------ | --------------------------------- |
| POST   | `/leave`                 | Submit a leave request            |
| GET    | `/leave/{requestId}`     | Retrieve a leave request          |
| GET    | `/employee/{id}/balance` | Retrieve employee leave balance   |
| GET    | `/employee/{id}/history` | Retrieve employee leave history   |
| GET    | `/manager/{id}/pending`  | Retrieve pending manager requests |

## Authentication

Amazon Cognito is used to provide authentication for users.

The application is designed to separate employee and manager functionality so that users can access the features relevant to their role.

## Deployment

The frontend is deployed using **AWS Amplify** and connected to the GitHub repository.

Changes pushed to the configured GitHub branch can trigger the Amplify deployment pipeline.

The backend is deployed using AWS Lambda and exposed through Amazon API Gateway.

## Project Structure

```text
leave-management-system/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── api/
│   │
│   ├── package.json
│   └── ...
│
├── README.md
└── ...
```

## Running the Frontend Locally

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/leave-management-system.git
```

Navigate into the frontend directory:

```bash
cd leave-management-system/frontend
```

Install the dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The application will then be available through the local development URL shown by Vite.

## Learning Outcomes

Through this project I gained practical experience with:

* Building a web application
* Developing a React frontend
* Working with REST APIs
* Creating AWS Lambda functions
* Configuring API Gateway
* Using AWS Amplify for deployment
* Working with authentication using Amazon Cognito
* Connecting a frontend application to cloud-based backend services
* Using Git and GitHub for version control
* Deploying and testing a cloud-based application

## Future Improvements

Potential improvements include:

* Email notifications for leave decisions
* More detailed manager dashboards
* Improved role-based access control
* Automated leave balance calculations
* Database integration for persistent data storage
* Improved validation and error handling
* Automated testing
* CI/CD improvements

## Author

**Nyiko Shipalana**

WeThinkCode_ — WTC-F4CZJ38J

This project demonstrates practical experience in full-stack development, serverless cloud services, API development, authentication, deployment, and version control.
