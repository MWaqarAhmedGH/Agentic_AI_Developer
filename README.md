# 🤖 Agentic AI Developer: Enterprise Roadmap

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![SQLModel](https://img.shields.io/badge/Database-SQLite%20/%20SQLModel-green.svg)](https://sqlmodel.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Welcome to the **Agentic AI Developer** project. This repository contains a comprehensive suite of AI agents ranging from basic function-calling scripts to complex, autonomous multi-agent systems. Developed as part of the **Nexe-Agent Internship Program**, this project demonstrates mastery in agentic reasoning, memory management, and collaborative AI architectures.

---

## 📂 Project Architecture

The project is structured into three progressive complexity levels:

### 🥉 [Beginner: Core Foundations](./beginner/)
*   **Tool-Calling Agent:** Implementation of dynamic function routing and structured JSON communication.
*   **AI Calculator:** An agent with session-based **Conversation Memory** capable of complex arithmetic and state persistence.

### 🥈 [Intermediate: Integration & Knowledge](./intermediate/)
*   **Multi-Tool Agent:** A service-oriented agent integrated with a **Persistent SQLite Database**, Web Search simulation, and validated Email services.
*   **RAG Assistant:** A Retrieval-Augmented Generation system using semantic chunking and keyword-based retrieval for grounded, factual answering.

### 🥇 [Advanced: Autonomy & Orchestration](./advanced/)
*   **Autonomous Business Agent:** Features a custom **Reasoning Engine** that performs goal-to-plan decomposition and maintains detailed execution logs.
*   **Multi-Agent System (MAS):** A collaborative environment featuring a **Manager Agent**, **Researcher**, and **Writer** interacting via a dedicated Communication Layer.

---

## 🚀 Getting Started

### Prerequisites
*   Python 3.9+
*   `pip install sqlmodel pydantic`

### Installation
```bash
git clone https://github.com/MWaqarAhmedGH/Agentic_AI_Developer.git
cd Agentic_AI_Developer
```

### Running the Agents
| Level | Task | Command |
| :--- | :--- | :--- |
| **Beginner** | Calculator | `python beginner/calculator_agent/agent.py` |
| **Intermediate** | Multi-Tool | `python intermediate/multi_tool_agent/agent.py` |
| **Intermediate** | RAG Assistant | `python intermediate/rag_assistant/agent.py` |
| **Advanced** | Autonomous Agent | `python advanced/autonomous_business_agent/agent.py` |
| **Advanced** | Multi-Agent System | `python advanced/multi_agent_system/agent.py` |

---

## 🛠️ Key Technical Features
*   **Persistence:** Real-world database integration using SQLModel.
*   **Reliability:** Strict Pydantic data validation and Regex-based email verification.
*   **Observability:** Comprehensive execution logs with timestamps for autonomous auditing.
*   **Scalability:** Modular, class-based architecture allowing for easy integration of new tools.

---

## 👨‍💻 Author
**[Your Name / MWaqarAhmedGH]**  
*Agentic AI Developer Intern at Nexe-Agent*

---
*This project was completed under the guidance of Nexe-Agent leadership. All logic and architecture are verified for production-standard agentic workflows.*
