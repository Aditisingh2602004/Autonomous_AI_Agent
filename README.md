# 🤖 Autonomous AI Agent

An intelligent autonomous agent that can execute multi-step workflows by combining API interactions, browser automation, and instruction-based decision making.

---

## 🚀 Features

* 🔐 **Automated Login**

  * Backend API authentication
  * Frontend login using Playwright (real browser automation)

* 🧠 **Instruction-Based Execution**

  * Reads instructions from local files or external sources
  * Dynamically decides which tool to execute

* ⚙️ **Tool-Driven Architecture**

  * Modular tools for different tasks
  * Agent selects and invokes tools automatically

* 🌐 **Browser Automation**

  * Uses Playwright to simulate real user interactions
  * Handles login, navigation, and data extraction

* 🔄 **Multi-Step Workflow Automation**

  * Example workflow:

    1. Read instructions
    2. Login
    3. Open dashboard
    4. Extract data
    5. Save results

---

## 🏗️ Project Structure

```
AUTONOMOUS_AGENT/
│
├── main.py              # Entry point
├── agent.py             # Core agent logic
├── tools.py             # Tool definitions
├── auth_manager.py      # Authentication handling
├── requirements.txt     # Dependencies
├── .gitignore           # Ignored files
│
├── instructions/        # Instruction files
│   └── platform.md
│
└── credentials/         # (Optional) local configs (not committed)
```

---

## ⚙️ Installation

### 1. Clone the repository

```
git clone https://github.com/Aditisingh2602004/Autonomous_AI_Agent.git
cd Autonomous_AI_Agent
```

---

### 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

### 4. Install Playwright

```
playwright install
```

---

## 🔐 Environment Setup

Create a `.env` file in the root directory:

```
USERNAME=your_username
PASSWORD=your_password
API_KEY=your_api_key
```

⚠️ Do NOT commit this file.

---

## ▶️ Usage

Run the agent:

```
python main.py
```

---

## 🧠 How It Works

1. The agent reads instructions (e.g., `instructions/platform.md`)
2. Based on the task, it selects the appropriate tool
3. Tools perform actions such as:

   * Logging in
   * Fetching data
   * Automating browser actions
4. Results are processed and stored

---

## 📌 Example Use Case

* Automated platform login
* Data extraction from dashboard
* Saving notes or results
* Executing workflows without manual intervention

---

## 🔧 Technologies Used

* Python
* Playwright
* LangChain (agent framework)
* REST APIs

---

## 🚀 Future Improvements

* Add UI dashboard
* Deploy as a web service
* Add memory and persistent state
* Improve decision-making logic

---

## 🤝 Contributing

Feel free to fork the repository and submit pull requests.

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 👤 Author

Developed by **Aditi Singh**

---
