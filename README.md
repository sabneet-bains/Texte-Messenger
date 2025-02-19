# Texte - Instant Messenger

Texte is a Python‑based instant messaging application built with Qt (PyQt6). It provides a full‑featured graphical interface for peer‑to‑peer communication, supporting both UDP and TCP protocols. The application offers separate panels for server settings, user sign‑in, chat configuration, and avatar selection, along with a chat log, message input field, and file attachment support.

![Texte Screenshot](https://github.com/sabneet95/Texte-Messenger/blob/master/messaging.png)

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture & Design](#architecture--design)
- [Directory Structure](#directory-structure)
- [Requirements](#requirements)
- [Installation & Getting Started](#installation--getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Future Work](#future-work)

---

## Overview

Texte is an instant messaging program written in Python using the PyQt6 library. It enables peer‑to‑peer communications via either UDP or TCP (selectable within the client interface). The project is designed as an educational tool with a rich, customizable user interface.

---

## Key Features

- **Modern Qt GUI:**  
  A clean, high‑DPI interface with custom themes, animated transitions, and modular panels.
  
- **Flexible Networking:**  
  Supports both UDP and TCP protocols (selectable from the UI or via command-line for the server).
  
- **User Panels:**  
  Separate panels for server settings, sign‑in, and chat configuration with dynamic avatar selection.
  
- **Real-Time Chat:**  
  A chat log area, message input field, and attachment support for instant messaging.

---

## Architecture & Design

Texte is divided into two main components:

- **Client:**  
  A Qt‑based graphical application (implemented in `client.py`) that encapsulates UI, animations, and networking logic (UDP/TCP selectable via a protocol selector).

- **Server:**  
  A headless server application (implemented in `server.py`) that listens for connections (default UDP, or TCP if specified) and responds to commands such as `{CONNECT}`, `{REGISTER}`, and `{UNREGISTER}`.

This modular design facilitates maintainability, testability, and future extension.

---

## Directory Structure

- **client.py**  
  Chat client application (PyQt6)

- **server.py**  
  Chat server supporting UDP and TCP (PyQt6)

- **icons/**  
  UI icons (e.g., `texte_icon.svg`, `enter_icon.svg`, etc.)

- **avatars/**  
  Avatar SVG files for user selection

- **README.md**  
  This documentation

---

## Requirements

- **Python 3.9.1 or later (64‑bit)**  
  [Download Python](https://www.python.org/downloads/)

- **PyQt6**  
  Install via pip:
  ```bash  
  pip install PyQt6
  ```
---

## Installation & Getting Started

1. **Clone the Repository:**
   ```bash   
   git clone https://github.com/sabneet95/Texte-Messenger.git
   cd Texte-Messenger
   ```
2. **Ensure Required Assets Are Present:**  
   Verify that the `icons` and `avatars` directories contain the expected images and SVG files.

3. **Install Dependencies:**
   ```bash   
   pip install PyQt6
   ```
4. **Open the Project:**  
   Use an IDE such as [Visual Studio Code](https://code.visualstudio.com/) or PyCharm with Python extensions.

---

## Usage

### Running the Server

The server supports both UDP and TCP protocols. By default, it runs in UDP mode. To run the server, open a terminal in the project directory and execute:

- **UDP Mode (default):**
  ```bash 
  python server.py
  ```
- **TCP Mode:**
  ```bash 
  python server.py tcp
  ```
### Running the Client

Open a separate terminal and run:

```bash 
python client.py
```

Within the client:

- **Protocol Selection:**  
  Use the protocol selector in the Server Settings panel to choose UDP or TCP.
  
- **Connection:**  
  Ensure the hostname and port match the server settings (default: 127.0.0.1 and port 33002), then toggle the server button to connect or disconnect.
  
- **Sign-In and Messaging:**  
  Toggle the sign‑in button to register your username and start messaging. You can run multiple client sessions to simulate messaging between different users.
  
- **Avatar & Chat Settings:**  
  Use the avatar selection and chat settings panels to customize your chat experience.

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Open an Issue:**  
   Discuss proposed changes before submitting pull requests.

2. **Follow Coding Standards:**  
   Ensure your contributions follow modern Python practices (PEP‑8, clear docstrings, and type hints).

3. **Submit Pull Requests:**  
   Provide clear descriptions and include tests/documentation as needed.

---

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

---

## Future Work

Planned enhancements include:

- Further security improvements.
- Expanded multi‑user chat functionality.
- Standalone server support with enhanced connection management.
- Additional theming and customization options.
- Integration of automated testing and continuous integration.

---

*For questions or further information, please consult the project’s issues or contact the maintainers.*
