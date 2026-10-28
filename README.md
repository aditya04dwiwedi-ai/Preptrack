# PLACEMENT PREPARATION & TRACKING SYSTEM

**B.Tech Mini Project — Session: 2026–27**  
**Department of Computer Science & Engineering (AIML)**  
**Lloyd Institute of Engineering & Technology (LIET), Greater Noida**  
*Affiliated to Dr. A.P.J. Abdul Kalam Technical University (AKTU), Lucknow, Uttar Pradesh*

---

## 👨‍🎓 Project Information (Synopsis Details)

| Attribute | Details |
| :--- | :--- |
| **Project Title** | Placement Preparation & Tracking System |
| **Student Name** | Aditya Dwivedi |
| **Roll Number** | 2501721530006 |
| **Section** | 2H |
| **Degree & Branch** | Bachelor of Technology in Computer Science & Engineering – AIML |
| **Institute** | Lloyd Institute of Engineering & Technology (LIET), Greater Noida |
| **Affiliating University** | Dr. A.P.J. Abdul Kalam Technical University (AKTU), Lucknow |
| **Project Guide** | Mr. Abhishek Suraj |
| **Assistant Professor** | Mr. Vishal Gupta |
| **Session** | 2026–27 |

---

## 📌 Problem Statement & Objectives

### Problem Statement
Students preparing for campus placements frequently manage multiple technical subjects, aptitude practice, mock tests, company application tracking, and personal goals across disparate tools or notes. Without an integrated tracking system, it is difficult to monitor subject-wise mastery, dynamically identify weak areas, evaluate placement readiness, and keep application stages organized.

### Project Objectives
1. **Develop a centralized web-based application** for managing and tracking student placement preparation.
2. **Maintain student profile data** including Name, Branch, Roll Number, and CGPA.
3. **Track preparation progress** across 5 core subjects: **Python, C, DSA, DBMS, and Aptitude** (0–100%).
4. **Calculate an overall preparation score** and classify placement readiness status:
   - **Score &ge; 75%**: Excellent (Placement Ready)
   - **50% &le; Score &lt; 75%**: Good (Steady Progress)
   - **Score &lt; 50%**: Needs Improvement (Focus Required)
5. **Identify weak areas dynamically**: Automatically flag any subject with preparation below 50% and display targeted recommendations.
6. **Provide a 5-question placement mock test** covering core concepts specified in the synopsis: **HTML, FIFO, Python comments, SQL, and LIFO**, with automated scoring, percentage calculation, and performance feedback. An extended question bank (116 questions across 9 categories, with Easy/Medium/Hard levels) supports topic-wise practice.
7. **Track company applications** through standardized pipeline stages: **Interested, Applied, Shortlisted, Interview, Selected, and Rejected**.
8. **Manage daily preparation goals** with Pending and Completed status tracking.
9. **Provide sample student records** (15 profiles) for academic demonstration, profile comparison and leaderboard ranking.

---

## 🔄 System Flow Architecture

As defined in the Mini Project Synopsis:

```
Student Profile 
       ↓
Preparation Progress (Python, C, DSA, DBMS, Aptitude)
       ↓
Placement Meter & Weak Area Finder (< 50% dynamic detection)
       ↓
Mock Test (HTML, FIFO, Python, SQL, LIFO) / Daily Goals
       ↓
Company Application Tracking (6 pipeline statuses)
       ↓
Sample Student Records (Demo & Comparison)
```

---

## 🛠️ Software & Hardware Requirements

### Software Requirements
- **Backend Language:** Python 3.8+ (Python 3.14 compatible)
- **Web Framework:** Flask 3.x
- **Frontend Structure:** HTML5 (Jinja2 Templates)
- **Styling & Components:** CSS3 & Bootstrap 5.3+
- **Frontend Interactivity:** JavaScript (ES6+ Fetch API)
- **Data Storage:** Python in-memory runtime variables, lists, and dictionaries (as specified in Synopsis page 9)

### Hardware Requirements
- **System:** Standard PC/Laptop (Windows 10/11, Linux, or macOS)
- **RAM:** 4 GB or higher
- **Storage:** 200 MB free disk space

---

## 🚀 How to Run the Project

### Option 1: One-Click Windows Launcher (Recommended)
Double-click **`run.bat`** in the project directory. It starts the Flask web server and automatically opens `http://127.0.0.1:5000` in your default web browser.

### Option 2: Terminal / Command Prompt
1. Open PowerShell or Command Prompt in this folder:
   ```powershell
   cd "C:\Users\Aditya\Desktop\placement_preparation_tracking"
   ```
2. Ensure Flask is installed:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
4. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

### Option 3: Direct Client-Side Execution
Double-click `index.html` to open directly in any modern browser. The frontend gracefully detects offline execution mode and maintains all interactive features locally.

---

## 🌐 Flask REST API Documentation

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | Renders the main web dashboard template |
| `/api/data` | `GET` | Fetches complete dashboard data (Profile, Subjects, Summary, Companies, Goals, Sample Students, Test History, Suggestions, Progress History, Activity Summary, Achievements) |
| `/api/profile` | `POST` | Updates student profile details (Name, Branch, CGPA, Roll No) |
| `/api/subjects` | `POST` | Updates progress for the 5 subjects; returns recalculated placement score, readiness classification, and weak areas |
| `/api/mock-test` | `GET` | Retrieves mock test questions. Params: `category` (`Synopsis` default, `Python`, `C`, `DSA`, `DBMS`, `Aptitude`, `OOP`, `Operating Systems`, `Computer Networks`, `Logical Reasoning`, `All`), `count` (`5`, `10`, `15`; capped at bank size), `difficulty` (`Easy`/`Medium`/`Hard`). `Synopsis` always returns the same 5 questions (HTML, FIFO, Python comments, SQL, LIFO); other categories are randomised. Answer keys are never sent. |
| `/api/mock-test/submit` | `POST` | Evaluates answers on the backend; returns score, percentage, performance message, and review. Body: `answers`, `category`, optional `question_ids` (counts unanswered questions as wrong) |
| `/api/companies` | `POST` | Adds a new company application |
| `/api/companies/<id>` | `PUT` | Updates company status or notes |
| `/api/companies/<id>` | `DELETE` | Removes a company application |
| `/api/goals` | `POST` | Adds a new daily preparation goal |
| `/api/goals/<id>` | `PUT` | Toggles or sets goal status (`Completed` / `Pending`) |
| `/api/goals/<id>` | `DELETE` | Deletes a daily goal |
| `/api/sample-students` | `GET` | Returns sample student batch records |
| `/api/sample-students/load/<id>` | `POST` | Loads a sample student profile into the active tracker |
| `/api/reset` | `POST` | Resets all runtime data (including seeded test history and topic checklist) back to initial demo defaults |
| `/api/suggestions` | `GET` | Evaluates the student against 13 sample company hiring criteria; returns fit scores and gaps |
| `/api/leaderboard` | `GET` | Ranks the 15 sample students plus the active student by overall score |
| `/api/progress-history` | `GET` | 8 weekly subject-score snapshots (for growth charts) plus current live scores |
| `/api/activity` | `GET` | 84 days of study activity (`problems_solved`, `minutes_studied`) with current/longest streak and totals |
| `/api/topics` | `GET` | Topic checklist for all subjects (or `?subject=`) with completion statistics |
| `/api/topics/<subject>/<topic_id>` | `PUT` | Sets a topic status: `Not Started`, `In Progress` or `Completed` |
| `/api/resources` | `GET` | Curated study resources (`?subject=` optional) |
| `/api/achievements` | `GET` | 10 achievement badges with unlocked state and progress hints, evaluated from live data |
| `/api/interview-questions` | `GET` | 25 HR / Technical / Behavioural interview questions with tips (`?category=` optional) |
| `/api/placement-stats` | `GET` | Illustrative placement statistics for four batch years |
| `/api/chat` | `POST` | PrepBot AI mentor. Body: `message`, optional `history`. Student data is read server-side. Returns `reply`, `source` (`gemini` / `openai` / `local`), optional `notice` |
| `/api/chat/status` | `GET` | Reports whether an AI provider key is configured |
| `/community-chat` | `GET` | Opens the real-time, room-based student community chat |
| `/api/chatroom/events?room=<name>` | `GET` | Streams recent room history and new messages to connected browsers using Server-Sent Events |
| `/api/chatroom/messages` | `POST` | Publishes a message to its room. JSON body: `name`, `room`, `message` |

### Community chat

Open **Community Chat** from the dashboard or visit `/community-chat`, choose a display name and room, and send messages. Multiple browsers connected to the same room receive new messages in real time; different room names keep conversations separate. The chat uses the existing Flask server and browser-native Server-Sent Events, so it adds no Python dependency. The latest 100 messages per room are kept in process memory and are cleared when the server restarts. Display names are not authenticated, so this is a lightweight demo chat rather than a private or moderated service.

---

## 📂 Project Structure

```text
placement_preparation_tracking/
│
├── app.py                  # Python Flask backend server & REST API logic
├── datasets.py             # Extended in-memory sample datasets (questions, students, companies, etc.)
├── chatbot.py              # PrepBot AI chat routes (Gemini / OpenAI + offline fallback)
├── chat_server.py          # In-memory room chat with SSE message broadcasting
├── .env.example            # Template for API keys (copy to .env; never share .env)
├── test_api.py             # Endpoint + data-integrity test suite (python test_api.py)
├── test_chat.py            # Chatbot tests with a mocked AI provider (python test_chat.py)
├── test_chat_server.py     # Community chat route and broadcast tests
├── run.bat                 # One-click Windows startup script
├── requirements.txt        # Python dependency specification (Flask)
├── README.md               # Project synopsis documentation & guide
├── index.html              # Root web entry point with offline fallback
│
├── templates/
│   ├── index.html          # Flask Jinja2 dashboard template
│   └── chat.html           # Community chat page
│
└── static/
    ├── chatbot.css         # Floating chat widget styles
    ├── chatbot.js          # Chat widget logic (typing indicator, markdown, YouTube chips)
    ├── chatroom.js         # Real-time community chat client
    ├── chatroom.css        # Community chat styles
    ├── style.css           # Custom responsive styles & Bootstrap 5 theme
    └── app.js              # Client-side JavaScript connecting UI to Flask REST API
```

---

## 🤖 PrepBot - AI Chat Assistant

A floating chat widget (bottom-right) that can:
1. **Analyse progress** - reads your live profile, subject scores, overall score, weak areas, goals and mock tests, then gives motivation and a study plan.
2. **Solve doubts and fix errors** - explain concepts or paste an error/code and get a corrected version.
3. **Recommend tutorials** - suggests topics and clickable YouTube *search* queries for weak subjects.

### Enable the AI (2 minutes)
1. Get a free key from [Google AI Studio](https://aistudio.google.com/) (or an OpenAI key).
2. Copy `.env.example` to `.env` and paste the key after `GEMINI_API_KEY=`.
3. Restart `python app.py` and open the chat. The header shows *AI mentor online*.

| Variable | Purpose | Default |
| :--- | :--- | :--- |
| `AI_PROVIDER` | `gemini` or `openai` | `gemini` |
| `GEMINI_API_KEY` / `OPENAI_API_KEY` | Your secret key (stays on the server) | empty |
| `GEMINI_MODEL` / `OPENAI_MODEL` | Model name. PrepBot auto-falls back to other Gemini models if this one is missing | `gemini-flash-latest` / `gpt-4o-mini` |

**Without a key** the chatbot still works in *demo mode*: it analyses progress and suggests videos from your data, but detailed doubt-solving needs the AI key. It also falls back to demo mode if the AI service is busy or offline.

**Privacy and safety:** the key is read from the server environment and never sent to the browser. Your progress snapshot and chat messages are sent to the AI provider, so do not paste passwords or personal information. Free-tier usage may be used by the provider to improve its products. Requests are limited to 20 per minute per client.

The chatbot needs the Flask server. If `index.html` is opened directly (Option 3), it shows a message asking you to start the server.

---

## 🗂️ Sample Datasets (In-Memory)

All data lives in Python lists/dictionaries as specified in the synopsis. Company names, package (CTC) figures, placement statistics and student records are **illustrative sample data** for academic demonstration only.

| Dataset | Size | Notes |
| :--- | :--- | :--- |
| Core synopsis mock test | 5 questions | HTML, FIFO, Python comments, SQL, LIFO (fixed order) |
| Tracked-subject question banks | 15 per subject (75 total) | Python, C, DSA, DBMS, Aptitude; Easy / Medium / Hard |
| Quiz-only categories | 10 each (40 total) | OOP, Operating Systems, Computer Networks, Logical Reasoning (do not affect the Placement Meter) |
| Sample students | 15 | Mixed branches, CGPA 6.5–9.5, all three readiness bands |
| Company suggestion criteria | 13 companies | Product, IT services, AI/ML startup, fintech, edtech, consulting |
| Company pipeline (default) | 8 applications | All six statuses represented |
| Daily goals (default) | 8 goals | Category and priority fields |
| Progress history | 8 weekly snapshots | Ends at the default subject scores |
| Activity log | 84 days | Streak and totals computed on request |
| Seeded mock-test history | 6 attempts | Newest is 4/5 (80%) |
| Topic checklist | 45 topics (9 per subject) | Not Started / In Progress / Completed |
| Study resources | 27 links | Well-known sites (top-level or long-standing URLs) |
| Achievements | 10 badges | Evaluated from live state |
| Interview questions | 25 | HR 8, Technical 10, Behavioural 7 |
| Placement statistics | 4 batch years | Illustrative |

### Running the tests
```bash
python test_api.py
```
Exercises every endpoint with Flask's test client and validates the datasets.

---

## 📚 Synopsis References

1. **Grinberg, M.** *Flask Web Development: Developing Web Applications with Python*, O’Reilly Media.
2. **Python Software Foundation**, *Python Documentation*, official documentation: `https://docs.python.org`.
3. **Pallets Projects**, *Flask Documentation*, official documentation: `https://flask.palletsprojects.com`.
4. **Bootstrap**, *Bootstrap Documentation*, official documentation for Bootstrap 5: `https://getbootstrap.com`.
5. **Mozilla Developer Network (MDN)**, *HTML, CSS and JavaScript Documentation*, web development reference material: `https://developer.mozilla.org`.
6. General research and study material on student placement preparation, progress tracking, and online assessment systems.
