# 📝 To-Do List App  

## 📌 Overview  
This is a **full-stack To-Do List web application** built using **FastAPI, MongoDB, and React**. Users can create, manage, and prioritize tasks, with the ability to mark tasks as completed using checkboxes.  

## 🛠 Tech Stack  
- **Backend:** FastAPI (Python) + MongoDB  
- **Frontend:** React (JavaScript)  
- **Database:** MongoDB Atlas (or local MongoDB instance)  

## 🚀 Features  
✅ Add tasks with a **priority level** (`High`, `Medium`, `Low`)  
✅ Mark tasks as **completed** using checkboxes  
✅ Remove tasks dynamically  
✅ Sort tasks by **priority** in the database  
✅ REST API endpoints for easy integration  

## 🔧 Installation  

### **Backend Setup** (FastAPI + MongoDB)  
1. Clone the repository:  
   ```bash
   git clone <repository-url>
   cd todo-list-app
   ```  
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  
3. Start FastAPI server:  
   ```bash
   uvicorn main:app --reload
   ```  

### **Frontend Setup** (React)  
1. Navigate to frontend directory:  
   ```bash
   cd frontend
   ```  
2. Install dependencies:  
   ```bash
   npm install
   ```  
3. Start development server:  
   ```bash
   npm start
   ```  

## 🔌 API Endpoints  

| Method | Endpoint        | Description                  |
|--------|---------------|------------------------------|
| `GET`  | `/tasks`      | Retrieve all tasks          |
| `POST` | `/tasks`      | Create a new task           |
| `PUT`  | `/tasks/{id}` | Update task completion status |
| `DELETE` | `/tasks/{id}` | Remove a task by ID        |

## 🛣 Roadmap  
- **Add due dates and deadlines for tasks**  
- **Implement user authentication**  
- **Enhance UI with animations and styling**  
- **Deploy backend and frontend to cloud services**  

## 📜 License  
This project is licensed under MIT. Feel free to use and contribute!  

