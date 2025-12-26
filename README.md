# 🤖 AI-Based Software Setup Assistant

An intelligent, voice-enabled desktop application that automates software installation and environment setup for engineering students and freshers using a **multi-agent AI architecture**.

---

## 🚀 Project Overview

Installing development tools like Python, Git, and Java manually on multiple systems is time-consuming and error-prone, especially in labs and training environments.

This project solves that problem by introducing an **AI-powered software setup assistant** that:

* Detects system OS
* Checks existing installations
* Installs required software automatically
* Supports voice commands
* Allows scheduled installations

---

## ✨ Key Features

* 🔍 Automatic OS detection
* 🤖 Central AI agent with child agents (download, install, environment setup)
* 🎙 Voice-controlled installation (Python / Git)
* ⏰ Scheduler for delayed installation
* 🧠 Intelligent installation check (prevents reinstallation)
* 🎨 Modern dark-themed UI (CustomTkinter)
* ⚙ Theme switching & settings panel
* 📋 Live activity log on home screen

---

## 🧩 System Architecture

```
User
 ↓
Login UI
 ↓
Central AI Agent
 ↓
├── OS Detection Agent
├── Installation Check Agent
├── Download Agent
├── Install Agent
└── Environment Setup Agent
```

Each agent performs a specific task independently, ensuring modularity and scalability.

---

## 🛠 Tech Stack

* **Language:** Python 3.11+
* **GUI:** CustomTkinter
* **Voice Recognition:** SpeechRecognition
* **Multithreading:** threading module
* **OS Detection:** platform
* **Installer Check:** shutil.which()

---

## 🖥 Application Screens

* Login Page
* Home Dashboard (Activity Log)
* Software Installation Page
* Scheduler Page
* About Project Page
* Settings (Theme & Language)

---

## 📦 Installation & Usage

### 1️⃣ Clone the repository

```bash
git clone https://github.com/mukesh17804/AI-Software-Setup-Assistant.git
cd AI-Software-Setup-Assistant
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

> ⚠ **Note:**
> PyAudio installation may fail on Windows.
> Install using precompiled `.whl` if required.

### 3️⃣ Run the application

```bash
python bullet_final.py
```

---

## 🎓 Use Cases

* Engineering college computer labs
* Training institutes
* Freshers setting up development environments
* Demo of AI-based automation systems

---

## 🧪 Future Enhancements

* 🌐 Network-based lab-wide installation
* 🔐 Database-backed user authentication
* 📊 Installation analytics dashboard
* 📦 Real silent installer (.exe)
* 🌍 Full Tamil / multi-language UI
* ☁ Cloud-based agent control

---

## 👨‍💻 Developer

**Name:** *Mukesh Kanna S.(https://github.com/mukesh17804)*
**Role:** Student / AI Enthusiast
**Project Type:** Academic / Final Year / Portfolio Project

---

## 📜 License

This project is open-source and free to use for educational purposes.

---

⭐ If you like this project, give it a star!
