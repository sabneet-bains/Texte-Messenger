# Texte - Instant Messenger

Texte is a Python-based, Qt graphical instant messaging program that leverages the QUdpSocket for semi-secure, peer-to-peer communications.

![](https://github.com/sabneet95/Texte-Messenger/blob/master/messaging.png)

## Key Features
* Implements the Qt and QUdpSocket libraries for GUI and networking, respectively
* Offers semi-secure, peer-to-peer communication
* Currently runs both server and clients on the same host network, with plans to extend to standalone server support in the future.

## Requirements

[Python 3.9.1 (64-bit) or above](https://www.python.org/downloads/)

[PyQt5](https://www.riverbankcomputing.com/software/pyqt/download)

## Tested Environment

Visual Studio Code
* Version: 1.52.1 (system setup)
* Commit: ea3859d4ba2f3e577a159bc91e3074c5d85c0523
* Electron: 9.3.5
* Chrome: 83.0.4103.122
* Node.js: 12.14.1
* V8: 8.3.110.13-electron.0
* OS: Windows_NT x64 10.0.19042
* Memory: 1981M
* Cores: 8

## Getting Started

1)	Open the project in **Visual Studio Code** > _run_ the server.py

```python
import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork

def Run_Server():
    app = QtCore.QCoreApplication(sys.argv)
    SOCKET = QtNetwork.QUdpSocket()

    def Bind_Server(HOST = "127.0.0.1", PORT = 33002):
        SOCKET.bind(QtNetwork.QHostAddress(HOST), PORT)

    ..
    ...
    ....

if __name__ == "__main__":
    Run_Server()
```

2)	Using an additional terminal tab, _run_ the client.py

```
    >>  client.py █
```

3)	Make sure the client hostname and port match with the server specifications:

```python
    HOST = "127.0.0.1", PORT = 33002
```

4)	Open another client session through the terminal and start messaging!

```
    >>  client.py █
```

## Contributing

The project welcomes pull requests. For major changes, please open an issue first to discuss the proposed changes. Please make sure to update tests as appropriate.


## License
This repository is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License.
