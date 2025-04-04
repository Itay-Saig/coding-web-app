# Real-Time Coding Web Application

This project is an interactive web application that allows users to work on coding exercises in real-time, with role-based interactions for mentors and students. It provides a platform where mentors can guide students through code blocks, and students can submit their code solutions to receive feedback instantly. The application is built using Flask for the backend and React for the frontend.

## :clipboard: Table of Contents
  * [Features](#dart-features)
  * [Tech Stack](#hammer_and_wrench-tech-stack)
  * [User Interface Preview](#iphone-user-interface-preview)
  * [Installation](#gear-installation)
  * [Usage](#computer-usage)
  * [File Structure](#open_file_folder-file-structure)

## :dart: Features

- **Real-Time Collaboration**: Mentors and students can join specific code blocks and interact in real time.
- **Role-Based System**: Mentors and students are assigned roles upon joining a code block, with mentors guiding students through the exercises.
- **Code Validation**: Students can submit their code, which is checked against a predefined solution. If the solution is correct, they receive a smiley notification.
- **Dynamic Code Block Management**: Code blocks are displayed on the frontend dynamically, and users can select which block to work on.
- **Socket Communication**: SocketIO is used for real-time communication between the frontend and backend.

## :hammer_and_wrench: Tech Stack

- **Backend**: Flask, Flask-SocketIO, Flask-CORS.
- **Frontend**: React, Socket.IO Client, CodeMirror.
- **Styling**: Styled Components.

The application integrates Flask with Socket.IO to enable real-time code collaboration, while React powers the interactive front end. CodeMirror provides a rich coding experience, and Styled Components ensures a modern, maintainable UI.

## :iphone: User Interface Preview

Below are previews of different sections of the application, showcasing key features and functionalities.

![](docs/lobby_screen.png)

**Fig. 1** | Lobby page for session management and code block selection. This serves as the entry point for both mentors and students.

---

![](docs/mentor_mode_screen.png)

**Fig. 2** | Mentor mode with real-time code review and guidance.

---

![](docs/student_mode_screen.png)

**Fig. 3** | Student mode for collaborative coding and feedback.

## :gear: Installation

### Prerequisites

Make sure you have the following installed:

- Python 3.x
- Node.js (for React development)

### Backend Setup

1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd <repo_directory>
   ```

2. Run the Flask server:
   ```bash
   python app.py
   ```

### Frontend Setup
- Navigate to the frontend directory:
  ```bash
  cd frontend
  ```

- Install the required Node.js packages:
  ```bash
  npm install
  ```
  
- Run the React development server:
  ```bash
  npm start
  ```

## :computer: Usage
- Open the frontend application in your browser. It will automatically connect to the backend via WebSockets.

- From the lobby, select a code block you wish to work on. You will be assigned a role (mentor or student).

- If you're a student, you can edit the code block using the integrated code editor. Submit your solution to check it against the predefined correct solution.

- If you're a mentor, you can observe students' progress and guide them if needed.

## :open_file_folder: File Structure
```bash
/codeing-web-app/      
│── /backend/           - Flask backend application.  
│   ├── app.py          - Main Flask server file.  
│  
│── /frontend/          - React frontend application.  
│   ├── /src/           - React component files.  
│   │   ├── Lobby.js  
│   │   ├── CodeBlock.js  
│   │   └── ...
```
