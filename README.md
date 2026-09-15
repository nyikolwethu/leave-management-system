# Leave Management System

A cloud-based **Leave Management System** designed to simplify the process of submitting, approving, rejecting, and tracking employee leave requests.

This project was developed as part of the **WeThinkCode_ WTC-F4CZJ38J elective proof of work**.

---

##  Overview

The Leave Management System provides employees and managers with a simple way to manage leave requests digitally.

### Employees can:

* Submit leave requests
* View their leave balance
* View previous leave requests
* Track the status of submitted requests

### Managers can:

* View pending leave requests
* Approve leave requests
* Reject leave requests
* Manage employee leave requests

The application uses a serverless backend with a web-based frontend and AWS cloud services.

---

##  Features

### Employee

* Employee authentication
* View leave balance
* Submit leave requests
* View leave request history
* Track request status

### Manager

* View pending leave requests
* Approve leave requests
* Reject requests
* Manage employee leave requests

---

##  Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript
* REST APIs

### Backend & Cloud

* AWS Lambda
* Amazon API Gateway
* Amazon Cognito
* AWS Amplify
* AWS SAM

### Development Tools

* Git
* GitHub
* Visual Studio Code
* PowerShell

---

##  Architecture

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
                    │  HTML / CSS / JS │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   API Gateway    │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │  Lambda  │   │  Lambda  │   │  Lambda  │
        │   Leave  │   │ Approval │   │  History │
        └──────────┘   └──────────┘   └──────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   AWS Services   │
                    └──────────────────┘
```

---

## 🔌 API Endpoints

The backend provides endpoints for managing employee leave.

| Method | Endpoint                 | Purpose                           |
| ------ | ------------------------ | --------------------------------- |
| POST   | `/leave`                 | Submit a leave request            |
| GET    | `/leave/{requestId}`     | Retrieve a leave request          |
| GET    | `/employee/{id}/balance` | Retrieve employee leave balance   |
| GET    | `/employee/{id}/history` | Retrieve employee leave history   |
| GET    | `/manager/{id}/pending`  | Retrieve pending manager requests |

---

##  Authentication

**Amazon Cognito** is used to provide authentication for users.

The application is designed to separate employee and manager functionality so users can access features relevant to their role.

---

## ☁️ Deployment

The frontend is designed to be deployed using **AWS Amplify** and connected to the GitHub repository.

Changes pushed to the configured GitHub branch can trigger the Amplify deployment pipeline.

The backend is deployed using **AWS Lambda** and exposed through **Amazon API Gateway**.

---

##  Project Structure

```text
leave-management-system/
│
├── backend/
│   ├── functions/
│   │   ├── approveRejectLeave/
│   │   ├── getLeaveBalance/
│   │   ├── getLeaveHistory/
│   │   ├── getPendingRequests/
│   │   ├── lowBalanceCheck/
│   │   └── submitLeave/
│   │
│   ├── seed_employees.py
│   └── template.yaml
│
├── frontend/
│   ├── css/
│   │   └── styles.css
│   │
│   ├── js/
│   │   ├── api.js
│   │   ├── app.js
│   │   └── config.js
│   │
│   └── index.html
│
├── .gitignore
└── README.md
```

---

##  Running the Frontend Locally

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/leave-management-system.git
```

Navigate into the project:

```bash
cd leave-management-system
```

Open the frontend:

```text
frontend/index.html
```

The frontend configuration can be found in:

```text
frontend/js/config.js
```

AWS API and Cognito configuration values should be added after the relevant AWS resources have been deployed.

---

## 📚 Learning Outcomes

Through this project, I gained practical experience with:

* Building a web application
* Developing frontend interfaces with HTML, CSS, and JavaScript
* Developing REST APIs
* Creating AWS Lambda functions
* Configuring Amazon API Gateway
* Working with AWS Amplify
* Working with Amazon Cognito
* Designing serverless application architecture
* Connecting frontend applications to cloud-based backend services
* Using Git and GitHub for version control
* Deploying and testing cloud-based applications

---

## 🚀 Future Improvements

Potential improvements include:

* Email notifications for leave decisions
* More detailed manager dashboards
* Improved role-based access control
* Automated leave balance calculations
* Database integration for persistent data storage
* Improved validation and error handling
* Automated testing
* CI/CD improvements
* Improved monitoring and logging

---

## 👤 Author

**Nyiko Shipalana**

WeThinkCode_ — WTC-F4CZJ38J

This demonstrates practical experience in frontend development, REST API development, AWS serverless services, authentication, deployment, and version control.
