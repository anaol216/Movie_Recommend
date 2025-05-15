# 🎬 Movie Recommendation System

A full-stack web application that recommends movies to users based on their preferences using a Machine Learning model in Python and a modern frontend built with Next.js.

---

## 🧠 How the Recommendation Model Works

The recommendation engine is built using **collaborative filtering** and/or **content-based filtering** techniques with libraries like `scikit-learn` or `Surprise`.


---

## ⚙️ Technologies Used

| Layer     | Technology           |
|-----------|----------------------|
| Backend   | Python, FastAPI|
| ML Model  | Scikit-learn, Surprise, Pandas |
| Frontend  | Next.js, TypeScript, Tailwind CSS |
| Data      | KuaiRand Dataset (or similar) |

---

## 🚀 Getting Started

---

### 1️⃣ Backend Setup (Python + FastAPI)

```bash
# Navigate to the backend folder (if separated)
cd backend

# Create virtual environment
python -m venv venv
# On Windows: 
venv\Scripts\activate 
# on macos 
source venv/bin/activate  

# Install dependencies
pip install -r ../requirements.txt


#If you don't have Jupyter
pip install notebook

#start the jupyter
jupyter notebook

# Run FastAPI server
uvicorn app:app --reload
cd frontend

# Install dependencies
npm install

# Run Next.js dev server
npm run dev


