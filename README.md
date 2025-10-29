<div align="center"><a name="readme-top"></a>

# 💬 Texte — A Python × Qt Instant Messenger

[![Python](https://img.shields.io/badge/Python-3.9%2B-528ec5?logo=python&logoColor=white&labelColor=0d1117&style=flat)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt-6.x-f39c12?logo=qt&logoColor=white&labelColor=0d1117&style=flat)](https://riverbankcomputing.com/software/pyqt/intro)
[![Networking](https://img.shields.io/badge/Protocol-UDP%20%7C%20TCP-lightgrey?logo=wireshark&logoColor=white&labelColor=0d1117&style=flat)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-2ECC71?labelColor=0d1117&style=flat)](https://choosealicense.com/licenses/mit/)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/sabneet-bains/Texte-Messenger)

**Messaging redefined — minimal, modular, and modern.**  
<sup>*A cross-platform instant messenger integrating PyQt6, UDP/TCP networking, and real-time GUI communication systems.*</sup>

<img src="https://github.com/sabneet95/Texte-Messenger/blob/master/messaging.png" alt="Texte GUI Screenshot" width="800">

</div>

> [!NOTE]
> <sup>Part of the <b>Foundational & Academic</b> collection — demonstrating cross-layer software design from GUI to network protocol.</sup>


## 🧭 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Repository Structure](#-repository-structure)
- [Development Environment](#-development-environment)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [Contributing](#-contributing)
- [Future Work](#-future-work)
- [Author](#-author)
- [License](#-license)


## 🧠 Overview
**Texte** is a Python-based instant messenger designed with **PyQt6** for its GUI layer and **UDP/TCP** for networking.  
It showcases modular software engineering — combining **event-driven design**, **socket programming**, and **user interface architecture**.

Built for both educational and experimental use, *Texte* demonstrates real-time communication mechanics and can serve as a foundation for distributed systems research or prototype messaging apps.

> [!TIP]
> Core modules (client and server) are completely decoupled — ideal for extension into cloud or multi-user systems.

<div align="right">

[![Back to Top](https://img.shields.io/badge/-⫛_TO_TOP-0d1117?style=flat)](#readme-top)

</div>


## ⚙️ Key Features

| Category | Description |
|:----------|:-------------|
| **Modern Qt GUI** | Clean, high-DPI interface with tabs, animations, and dynamic panels. |
| **Protocol Support** | Switch seamlessly between **UDP** and **TCP** at runtime. |
| **Real-Time Messaging** | Message logs, timestamps, and file attachment capability. |
| **User Panels** | Dedicated panes for server setup, login, and chat configuration. |
| **Extensible Architecture** | Modular design supports security, logging, and user database integration. |

> [!NOTE]
> The GUI follows **Model-View-Controller** principles: interface (View), message logic (Model), and network backend (Controller).

<div align="right">

[![Back to Top](https://img.shields.io/badge/-⫛_TO_TOP-0d1117?style=flat)](#readme-top)

</div>


## 🧱 Architecture

| Component | Role | Technology |
|:-----------|:-----|:------------|
| **Client (`client.py`)** | Qt application handling user interface, networking I/O, and threading. | **PyQt6**, **socket**, **asyncio** |
| **Server (`server.py`)** | Lightweight backend managing UDP/TCP sessions, message routing, and user registration. | **Python 3.9+**, **socket**, **threading** |
| **Communication Layer** | Transport abstraction supporting both connection-oriented and connectionless protocols. | **TCP / UDP** |
| **UI Framework** | Event-driven widgets and signal-slot architecture. | **Qt (PyQt6)** |

> [!TIP]
> All major components (GUI, network core, assets) are **loosely coupled**, ensuring each can evolve independently.

<div align="right">

[![Back to Top](https://img.shields.io/badge/-⫛_TO_TOP-0d1117?style=flat)](#readme-top)

</div>


## 📂 Repository Structure
````text
Texte-Messenger/
│
├── client.py           # Main GUI client
├── server.py           # Network server (UDP/TCP)
├── icons/              # Toolbar and interface icons
├── avatars/            # Profile and user avatars
├── themes/             # Optional theme/style overrides
├── assets/             # Logos, design resources
├── README.md
└── LICENSE
````

> [!TIP]
> Directory structure is designed for **educational clarity** — client and server can be executed independently for testing.

<div align="right">

[![Back to Top](https://img.shields.io/badge/-⫛_TO_TOP-0d1117?style=flat)](#readme-top)

</div>


## 💻 Development Environment

| Component | Tools & Versions | Purpose / Usage |
|:-----------|:----------------|:----------------|
| **Programming Language** | **Python 3.9+ (64-bit)** | Core environment for GUI, sockets, and event handling. |
| **Framework** | **PyQt6 (Qt6 bindings)** | Provides the graphical interface, layout control, and event loop. |
| **Networking** | **socket**, **asyncio**, **threading** | Manages UDP/TCP transport and concurrent messaging. |
| **IDE** | **VS Code / PyCharm** | Recommended for debugging and development. |
| **Asset Design** | **PowerPoint (SVG Export)**, **Photoshop / GIMP** | Used to design avatars, icons, and GUI components. |
| **Version Control** | **Git / GitHub** | Handles version tracking, issues, and collaborative contributions. |
| **Testing (Planned)** | **pytest**, **unittest** | Frameworks to be added for regression and performance testing. |

> [!NOTE]
> The application follows a **signal–slot architecture**, ensuring responsive UI behavior and decoupled logic between the interface, network backend, and message handling layers.

<div align="right">

[![Back to Top](https://img.shields.io/badge/-⫛_TO_TOP-0d1117?style=flat)](#readme-top)

</div>


## 🧰 Requirements
````text
Python >= 3.9
PyQt6 >= 6.2
````

> [!IMPORTANT]
> PyQt6 requires the **Qt runtime libraries**.  
> On Windows, install via `pip install PyQt6`; on Linux, system packages like `python3-pyqt6` may be needed.

<div align="right">

[![Back to Top](https://img.shields.io/badge/-⫛_TO_TOP-0d1117?style=flat)](#readme-top)

</div>


## 🚀 Installation
````bash
# Clone the repository
git clone https://github.com/sabneet95/Texte-Messenger.git
cd Texte-Messenger

# Install dependencies
pip install PyQt6
````

> [!TIP]
> Ensure that **icons/** and **avatars/** directories remain alongside `client.py` and `server.py`,  
> as these assets are dynamically loaded by the Qt resource handlers at runtime.

<div align="right">

[![Back to Top](https://img.shields.io/badge/-⫛_TO_TOP-0d1117?style=flat)](#readme-top)

</div>


## 💬 Usage

### **Running the Server**
````bash
# Default UDP mode
python server.py

# TCP mode
python server.py tcp
````

### **Running the Client**
````bash
python client.py
````

Once the client starts:
- Select **protocol (UDP/TCP)** from the Server Settings panel.  
- Match host and port with the server configuration (`127.0.0.1:33002` by default).  
- Sign in, choose an avatar, and start messaging instantly.  
- The interface supports **file attachments**, **chat logs**, and **custom themes**.

> [!NOTE]
> The server can be hosted **locally or remotely**, making *Texte* ideal for  
> **LAN experiments**, **distributed systems coursework**, and **network performance demonstrations**.

<div align="right">

[![Back to Top](https://img.shields.io/badge/-⫛_TO_TOP-0d1117?style=flat)](#readme-top)

</div>


## 🤝 Contributing
**Contributions are welcome!**

1. **Open an issue** before implementing major changes.  
2. **Follow best practices** (PEP-8 compliance, PyQt signal-slot conventions).  
3. **Include supporting visuals or logs** for UI/network-related updates.  
4. **Submit a pull request** detailing your implementation and testing notes.

> [!TIP]
> Promising extensions: **encryption**, **async networking**, **group messaging**, or **REST/WebSocket hybrid models**.

<div align="right">

[![Back to Top](https://img.shields.io/badge/-⫛_TO_TOP-0d1117?style=flat)](#readme-top)

</div>


## 🔮 Future Work

| Area | Enhancement |
|:------|:-------------|
| **Networking** | Add persistent server-side state and broadcast support. |
| **Security** | Integrate **TLS** or **Fernet**-based encryption layers. |
| **Database** | Introduce **SQLite/MySQL** user profiles and chat history. |
| **Packaging** | Bundle cross-platform executables with **PyInstaller**. |
| **Testing & CI/CD** | Add **pytest**, **flake8**, and GitHub Actions pipelines. |
| **UI Customization** | Expand theme controls, font scaling, and accessibility options. |

> [!TIP]
> The long-term goal is to evolve *Texte* into a **distributed systems demonstrator** —  
> capable of simulating real-world communication protocols for educational and research purposes.

<div align="right">

[![Back to Top](https://img.shields.io/badge/-⫛_TO_TOP-0d1117?style=flat)](#readme-top)

</div>


<div align="center">

##
### 👤 Author  
**Sabneet Bains**  
*Quantum × AI × Scientific Computing*  
[LinkedIn](https://www.linkedin.com/in/sabneet-bains/) • [GitHub](https://github.com/sabneet-bains)

##
### 📄 License  
Licensed under the [MIT License](https://choosealicense.com/licenses/mit/)

<sub>“Communication systems remind us — signal and noise are only opposites when meaning gets lost in transmission.”</sub>

</div>
