# 🎬 Quiz Game Website

A fun and interactive quiz game where players guess the name of a random movie based on hints and AI-powered responses. Built using **HTML, CSS, JavaScript, Bootstrap, Python, Flask, SQLite3, and Gemini API**.

---

## 🚀 Features
- 📝 **Guess the Movie**: Players receive a hint and must guess the movie.
- ❓ **Ask Questions**: Players can ask about the movie (e.g., plot, director, main actor, release year, etc.) to help them guess.
- 🎯 **Limited Guesses**: Players get **5 guesses** before the game ends.
- 🤖 **AI-Powered Answers**: Gemini API provides concise answers to player queries.
- 🏆 **Leaderboard**: Tracks users' scores.
- 🔢 **Scoring System**: Fewer questions asked = higher score.
- 🎨 **Simple & Clean UI**: Minimalist design with Bootstrap styling.

---

## 🛠️ Tech Stack
### **Frontend**
- HTML, CSS, JavaScript
- Bootstrap

### **Backend**
- Python, Flask
- SQLite3 (Database)
- Gemini API (AI functionality)

---

## 🔍 Game Logic & Functionality
1. When a player starts the game, a **random movie** is selected using the **Gemini API**.
2. A **hint** is generated for the movie.
3. The player can **ask unlimited questions** about the movie.
4. If the player thinks they know the answer, they can submit a guess.
5. If correct, they win 🎉. If wrong, they lose **one of their 5 guesses**.
6. If all guesses are used, they lose the game.

---

## 📊 Scoring System
- Score is calculated based on the number of questions asked:
  ```
  score = 100 - (number_of_questions * 10)
  ```
- If a player asks **9 or more** questions, they receive only **10 points**.

---

## 🎨 Design Choices
- **Minimalistic UI**: Simple color scheme with Bootstrap styling.
- **Desktop-Only Experience**: Since mobile users have access to numerous quiz apps, the game is optimized for desktops only.

---

## 📜 How to Run Locally
### **1️⃣ Clone the Repository**
```bash
$ git clone https://github.com/yourusername/quiz-game.git
$ cd quiz-game
```
### **2️⃣ Set Up a Virtual Environment** (Optional but recommended)
```bash
$ python -m venv venv
$ source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
### **3️⃣ Install Dependencies**
```bash
$ pip install -r requirements.txt
```
### **4️⃣ Create an `api.env` File**
Inside your project folder, create a file named `api.env` and add your API key:
```bash
API_KEY=your_api_key_here
```
### **6️⃣ Run the Flask App**
```bash
$ flask run
```
### **7️⃣ Open in Browser**
Go to `http://127.0.0.1:5000/` and start playing! 🎮

---

## 🌟 Final Thoughts
This project is a fun way to test movie knowledge while experimenting with AI integration. Hope you enjoy playing it! 🚀

If you like this project, feel free to **star ⭐ the repository** and contribute! 😊

