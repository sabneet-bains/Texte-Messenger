# 💬 Texte — A Python × Qt Instant Messenger  

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt-6.x-orange?logo=qt&logoColor=white)](https://riverbankcomputing.com/software/pyqt/intro)
[![Networking](https://img.shields.io/badge/Protocol-UDP%20%7C%20TCP-lightgrey?logo=wireshark&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

<br>

**Texte** is a Python-based instant messaging application built with **Qt (PyQt6)**.  

It features a modern GUI and supports peer-to-peer communication over both **UDP** and **TCP**.  
The interface includes panels for server settings, sign-in, chat configuration, and avatar selection, with a chat log, message input field, and file attachment support.

<img src="https://github.com/sabneet95/Texte-Messenger/blob/master/messaging.png" width="800">


## 🧭 Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture & Design](#architecture--design)
- [Directory Structure](#directory-structure)
- [Requirements](#requirements)
- [Installation & Getting Started](#installation--getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [Future Work](#future-work)
- [Author](#author)
- [License](#license)


## 🧩 Overview

Texte is an instant-messaging program written in Python using **PyQt6**.  
It enables peer-to-peer communication via **UDP** or **TCP**, selectable from the client interface.  
The project serves as an educational and demonstrative implementation of modern GUI-based networking.


## ⚙️ Key Features

- **Modern Qt GUI** — High-DPI interface with custom themes, animations, and modular panels.  
- **Flexible Networking** — Supports UDP / TCP, selectable via UI or command line.  
- **User Panels** — Separate panes for server settings, sign-in, and chat configuration.  
- **Real-Time Chat** — Integrated log, input field, and file attachment support.


## 🧱 Architecture & Design

**Client (`client.py`)** — Qt-based graphical application encapsulating UI logic, animations, and networking controls.  
**Server (`server.py`)** — Headless server handling UDP / TCP messaging, supporting commands such as `{CONNECT}`, `{REGISTER}`, and `{UNREGISTER}`.  

This modular separation improves maintainability and scalability.


## 📂 Directory Structure

```
Texte-Messenger/
├── client.py
├── server.py
├── icons/
├── avatars/
├── README.md
└── LICENSE
```


## 🧰 Requirements

- **Python 3.9.1 or later (64-bit)**  
  [Download Python](https://www.python.org/downloads/)  
- **PyQt6**  
  ```bash
  pip install PyQt6
  ```


## 🚀 Installation & Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/sabneet95/Texte-Messenger.git
   cd Texte-Messenger
   ```
2. **Verify assets** — ensure `icons/` and `avatars/` directories are present.  
3. **Install dependencies**
   ```bash
   pip install PyQt6
   ```
4. **Open the project** in VS Code or PyCharm for the best experience.


## 💬 Usage

### **Running the Server**
- **UDP Mode (default):**
  ```bash
  python server.py
  ```
- **TCP Mode:**
  ```bash
  python server.py tcp
  ```

### **Running the Client**
```bash
python client.py
```

Within the client:
- Choose protocol (UDP/TCP) from the Server Settings panel.  
- Ensure host/port match (server default 127.0.0.1:33002).  
- Toggle connection and sign in to begin messaging.  
- Customize avatars and chat themes as desired.


## 🤝 Contributing

1. **Open an Issue** before major changes.  
2. **Follow Coding Standards** — PEP-8, docstrings, and type hints.  
3. **Submit Pull Requests** with clear descriptions and tests.


## 🔮 Future Work

- Expanded multi-user chat functionality.  
- Standalone server support with connection management.  
- Enhanced security and encryption layers.  
- Additional themes and customization options.  
- Integration of automated testing and CI pipelines.


## 🧠 Author

**Sabneet Bains** — *Quantum × AI × Scientific Computing*  
[LinkedIn](https://www.linkedin.com/in/sabneet-bains/) • [GitHub](https://github.com/sabneet-bains)


## 📄 License

Licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

