import sys
import os
import logging
from typing import Optional

from PyQt6 import QtCore, QtGui, QtWidgets, QtNetwork

# Configure logging for production readiness.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatClient(QtWidgets.QDialog):
    """
    Production-ready chat client with complete UI features and the option to use UDP or TCP.
    
    Features:
      - UDP/TCP socket initialization based on user selection.
      - High-DPI scaling calculations.
      - Main chat window with custom icon and centered geometry.
      - Left-side menus for Server Settings, Sign-In, and Chat Settings (with shadow effects and animations).
      - Extended avatar selection widget with dynamic avatar creation and page flipping.
      - Chat log area, message field, and attach button (with animations).
      - Custom drop-down overlays for Chat Theme and Chat Recipient combo boxes.
      - All functions for connecting/disconnecting, signing in/out, sending/receiving messages, attaching images, etc.
    """

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self.logger = logger

        # Default to UDP; a socket instance will be re-created later if TCP is chosen.
        self.socket = QtNetwork.QUdpSocket(self)

        # Calculate scaling values
        self._setup_scaling()

        # Build the complete UI (all widgets and layouts)
        self._setup_ui()

        # Setup animations for menus/buttons (already created during UI setup)
        self._setup_animations()

        # Setup custom drop-down overlays (widgets created in _setup_ui)
        self._setup_drop_down_overlays()

        # Connect signals to slots
        self._connect_signals()

        # Apply the default theme
        self.theme("Default")

    def _setup_scaling(self) -> None:
        """Calculate scaling parameters from the primary screen geometry."""
        app = QtWidgets.QApplication.instance()
        screen_geom = app.primaryScreen().availableGeometry()
        self.scaled_app_width = int(screen_geom.width() / 3)
        self.scaled_app_height = int(screen_geom.height() / 2)
        self.scaled_border_radius = str(int(screen_geom.height() / 86.4))
        self.scaled_font_size = str(int(screen_geom.height() / 100))
        self.scaled_underline_size = str(int(screen_geom.height() / 720))
        self.screen_geom = screen_geom

    def _setup_ui(self) -> None:
        """Set up the main window and all its child widgets."""
        # Main Chat Window
        self.setObjectName("Chat_Window")
        self.setGeometry(
            int(self.screen_geom.width() / 2) - int(self.scaled_app_width / 2),
            int(self.screen_geom.height() / 2) - int(self.scaled_app_height / 2),
            self.scaled_app_width,
            self.scaled_app_height,
        )
        self.setWindowTitle("  texte")
        icon_path = os.path.join(os.getcwd(), "icons", "texte_icon.svg")
        self.setWindowIcon(QtGui.QIcon(icon_path))

        # --- Left Menu Bars ---
        # Server Settings Menu (top left)
        self.server_settings_menu = QtWidgets.QFrame(self)
        self.server_settings_menu.setObjectName("Server_Settings_Menu")
        self.server_settings_menu.setGeometry(
            -int(self.scaled_app_width / 10),
            0,
            int(self.scaled_app_width / 3.62),
            int(self.scaled_app_height / 3),
        )
        self.server_settings_menu.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(
                color=QtGui.QColor(0, 0, 0, 25),
                blurRadius=60,
                xOffset=int(self.scaled_app_width / 128),
                yOffset=int(self.scaled_app_height / 103.5),
            )
        )
        self.server_settings_menu_anim = QtCore.QPropertyAnimation(
            self.server_settings_menu, b"pos"
        )
        self.server_settings_menu_anim.setStartValue(self.server_settings_menu.pos())
        self.server_settings_menu_anim.setEndValue(QtCore.QPoint(0, 0))
        self.server_settings_menu_anim.setDuration(150)

        # Sign-In Menu (middle left)
        self.sign_in_menu = QtWidgets.QFrame(self)
        self.sign_in_menu.setObjectName("Sign_In_Menu")
        self.sign_in_menu.setGeometry(
            -int(self.scaled_app_width / 20),
            int(self.scaled_app_height / 3),
            int(self.scaled_app_width / 3.62),
            int(self.scaled_app_height / 3),
        )
        self.sign_in_menu.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(
                color=QtGui.QColor(0, 0, 0, 25),
                blurRadius=60,
                xOffset=int(self.scaled_app_width / 128),
                yOffset=int(self.scaled_app_height / 103.5),
            )
        )
        self.sign_in_menu_anim = QtCore.QPropertyAnimation(
            self.sign_in_menu, b"pos"
        )
        self.sign_in_menu_anim.setStartValue(self.sign_in_menu.pos())
        self.sign_in_menu_anim.setEndValue(QtCore.QPoint(0, int(self.scaled_app_height / 3)))
        self.sign_in_menu_anim.setDuration(150)

        # Chat Settings Menu (bottom left)
        self.chat_settings_menu = QtWidgets.QFrame(self)
        self.chat_settings_menu.setObjectName("Chat_Settings_Menu")
        self.chat_settings_menu.setGeometry(
            -int(self.scaled_app_width / 30),
            int(2 * self.scaled_app_height / 3),
            int(self.scaled_app_width / 3.62),
            int(self.scaled_app_height / 2.9),
        )
        self.chat_settings_menu.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(
                color=QtGui.QColor(0, 0, 0, 25),
                blurRadius=60,
                xOffset=int(self.scaled_app_width / 128),
                yOffset=int(self.scaled_app_height / 103.5),
            )
        )
        self.chat_settings_menu_anim = QtCore.QPropertyAnimation(
            self.chat_settings_menu, b"pos"
        )
        self.chat_settings_menu_anim.setStartValue(self.chat_settings_menu.pos())
        self.chat_settings_menu_anim.setEndValue(
            QtCore.QPoint(0, int(2 * self.scaled_app_height / 3))
        )
        self.chat_settings_menu_anim.setDuration(150)

        # --- Server Settings Submenu Widgets ---
        self.server_settings_icon = QtWidgets.QPushButton(self.server_settings_menu)
        self.server_settings_icon.setObjectName("Server_Settings_Icon")
        self.server_settings_icon.setGeometry(
            int(self.scaled_app_width / 60),
            int(self.scaled_app_height / 45),
            int(self.scaled_app_width / 28),
            int(self.scaled_app_height / 22),
        )
        self.server_settings_icon.setStyleSheet("background: transparent; border: none;")
        self.server_settings_icon.setIcon(
            QtGui.QIcon(os.path.join(os.getcwd(), "icons", "server_icon.svg"))
        )
        self.server_settings_icon.setIconSize(
            QtCore.QSize(
                int(self.scaled_app_width / 28), int(self.scaled_app_height / 24)
            )
        )
        self.server_settings_icon.setCheckable(True)
        self.server_settings_icon.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(
                color=QtGui.QColor(0, 0, 0, 100),
                blurRadius=30,
                xOffset=int(self.scaled_app_width / 350),
                yOffset=int(self.scaled_app_height / 350),
            )
        )
        self.server_settings_icon.raise_()

        self.server_settings_title = QtWidgets.QLabel(self.server_settings_menu)
        self.server_settings_title.setObjectName("Server_Settings_Title")
        self.server_settings_title.setGeometry(
            int(self.scaled_app_width / 13.2),
            int(self.scaled_app_height / 33),
            int(self.scaled_app_width / 5),
            int(self.scaled_app_height / 34),
        )
        self.server_settings_title.setText("Server Settings")

        self.host_title = QtWidgets.QLabel(self.server_settings_menu)
        self.host_title.setObjectName("Host_Title")
        self.host_title.setGeometry(
            int(self.scaled_app_width / 12.8),
            int(self.scaled_app_height / 11.2),
            int(self.scaled_app_width / 5),
            int(self.scaled_app_height / 34),
        )
        self.host_title.setText("Hostname")

        self.host_address = QtWidgets.QLineEdit(self.server_settings_menu)
        self.host_address.setObjectName("Host_Address")
        self.host_address.setGeometry(
            int(self.scaled_app_width / 13.2),
            int(self.scaled_app_height / 7.7),
            int(self.scaled_app_width / 11.6),
            int(self.scaled_app_height / 33),
        )
        self.host_address.setText("127.0.0.1")

        self.port_title = QtWidgets.QLabel(self.server_settings_menu)
        self.port_title.setObjectName("Port_Title")
        self.port_title.setGeometry(
            int(self.scaled_app_width / 12.8),
            int(self.scaled_app_height / 5.6),
            int(self.scaled_app_width / 5),
            int(self.scaled_app_height / 34),
        )
        self.port_title.setText("Port #")

        self.port_number = QtWidgets.QLineEdit(self.server_settings_menu)
        self.port_number.setObjectName("Port_Number")
        self.port_number.setGeometry(
            int(self.scaled_app_width / 13.2),
            int(self.scaled_app_height / 4.56),
            int(self.scaled_app_width / 11.6),
            int(self.scaled_app_height / 33),
        )
        self.port_number.setText("33002")

        # --- New: Protocol Selector (UDP/TCP) ---
        self.protocol_selector = QtWidgets.QComboBox(self.server_settings_menu)
        self.protocol_selector.setObjectName("Protocol_Selector")
        # Position it below the port number (adjust as needed)
        self.protocol_selector.setGeometry(
            int(self.scaled_app_width / 13.2),
            int(self.scaled_app_height / 3.0),
            int(self.scaled_app_width / 11.6),
            int(self.scaled_app_height / 33),
        )
        self.protocol_selector.addItems(["UDP", "TCP"])

        self.server_button = QtWidgets.QPushButton(self.server_settings_menu)
        self.server_button.setObjectName("Server_Button")
        self.server_button.setGeometry(
            int(self.scaled_app_width / 4.7),
            int(self.scaled_app_height / 5.1),
            int(self.scaled_app_width / 25),
            int(self.scaled_app_height / 20),
        )
        self.server_button.setStyleSheet("background: transparent; border: none;")
        self.server_button.setIcon(
            QtGui.QIcon(os.path.join(os.getcwd(), "icons", "enter_icon.svg"))
        )
        self.server_button.setIconSize(
            QtCore.QSize(
                int(self.scaled_app_width / 20), int(self.scaled_app_height / 17)
            )
        )
        self.server_button.setCheckable(True)
        self.server_button.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(
                color=QtGui.QColor(0, 0, 0, 100),
                blurRadius=30,
                xOffset=int(self.scaled_app_width / 300),
                yOffset=int(self.scaled_app_height / 350),
            )
        )

        self.server_connection_status = QtWidgets.QLabel(self.server_settings_menu)
        self.server_connection_status.setObjectName("Server_Connection_Status")
        self.server_connection_status.setGeometry(
            0,
            int(self.scaled_app_height / 3.5),
            int(self.scaled_app_width / 3.62),
            int(self.scaled_app_height / 20),
        )
        self.server_connection_status.setText(
            "<html><head/><body><center>NOT CONNECTED</center></body></html>"
        )

        # --- Sign-In Menu Widgets ---
        self.user_avatar = QtWidgets.QPushButton(self.sign_in_menu)
        self.user_avatar.setObjectName("user1")
        self.user_avatar.setGeometry(
            int(self.scaled_app_width / 65),
            int(self.scaled_app_height / 48),
            int(self.scaled_app_width / 20),
            int(self.scaled_app_height / 15),
        )
        self.user_avatar.setStyleSheet("background: transparent; border: none;")
        self.user_avatar.setIcon(
            QtGui.QIcon(os.path.join(os.getcwd(), "avatars", "user1.svg"))
        )
        self.user_avatar.setIconSize(
            QtCore.QSize(
                int(self.scaled_app_width / 20), int(self.scaled_app_height / 17)
            )
        )
        self.user_avatar.setCheckable(True)
        self.user_avatar.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(
                color=QtGui.QColor(0, 0, 0, 100),
                blurRadius=30,
                xOffset=int(self.scaled_app_width / 350),
                yOffset=int(self.scaled_app_height / 350),
            )
        )
        self.user_avatar.setVisible(False)
        self.user_avatar.raise_()

        self.temporary_avatar = QtWidgets.QPushButton(self.sign_in_menu)
        self.temporary_avatar.setObjectName("Temporary_Avatar")
        self.temporary_avatar.setGeometry(
            int(self.scaled_app_width / 65),
            int(self.scaled_app_height / 48),
            int(self.scaled_app_width / 20),
            int(self.scaled_app_height / 15),
        )
        self.temporary_avatar.setStyleSheet("background: transparent; border: none;")
        self.temporary_avatar.setIcon(
            QtGui.QIcon(os.path.join(os.getcwd(), "avatars", "user1.svg"))
        )
        self.temporary_avatar.setIconSize(
            QtCore.QSize(
                int(self.scaled_app_width / 20), int(self.scaled_app_height / 17)
            )
        )
        self.temporary_avatar.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(
                color=QtGui.QColor(0, 0, 0, 100),
                blurRadius=30,
                xOffset=int(self.scaled_app_width / 350),
                yOffset=int(self.scaled_app_height / 350),
            )
        )

        self.sign_in_title = QtWidgets.QLabel(self.sign_in_menu)
        self.sign_in_title.setObjectName("Sign_In_Title")
        self.sign_in_title.setGeometry(
            int(self.scaled_app_width / 13.2),
            int(self.scaled_app_height / 33),
            int(self.scaled_app_width / 5),
            int(self.scaled_app_height / 34),
        )
        self.sign_in_title.setText("Sign-in")

        self.username_title = QtWidgets.QLabel(self.sign_in_menu)
        self.username_title.setObjectName("Username_Title")
        self.username_title.setGeometry(
            int(self.scaled_app_width / 12.8),
            int(self.scaled_app_height / 11.2),
            int(self.scaled_app_width / 5),
            int(self.scaled_app_height / 34),
        )
        self.username_title.setText("Username")

        self.username = QtWidgets.QLineEdit(self.sign_in_menu)
        self.username.setObjectName("Username")
        self.username.setGeometry(
            int(self.scaled_app_width / 13.2),
            int(self.scaled_app_height / 7.7),
            int(self.scaled_app_width / 11.6),
            int(self.scaled_app_height / 33),
        )
        self.username.setText("Hugo")
        self.username.setEnabled(False)

        self.password_title = QtWidgets.QLabel(self.sign_in_menu)
        self.password_title.setObjectName("Password_Title")
        self.password_title.setGeometry(
            int(self.scaled_app_width / 12.8),
            int(self.scaled_app_height / 5.6),
            int(self.scaled_app_width / 5),
            int(self.scaled_app_height / 34),
        )
        self.password_title.setText("Password")

        self.password = QtWidgets.QLineEdit(self.sign_in_menu)
        self.password.setObjectName("Password")
        self.password.setGeometry(
            int(self.scaled_app_width / 13.2),
            int(self.scaled_app_height / 4.56),
            int(self.scaled_app_width / 11.6),
            int(self.scaled_app_height / 33),
        )
        self.password.setText("********")
        self.password.setEnabled(False)

        self.sign_in_button = QtWidgets.QPushButton(self.sign_in_menu)
        self.sign_in_button.setObjectName("Sign_In_Button")
        self.sign_in_button.setGeometry(
            int(self.scaled_app_width / 4.7),
            int(self.scaled_app_height / 5.1),
            int(self.scaled_app_width / 25),
            int(self.scaled_app_height / 20),
        )
        self.sign_in_button.setStyleSheet("background: transparent; border: none;")
        self.sign_in_button.setIcon(
            QtGui.QIcon(os.path.join(os.getcwd(), "icons", "enter_icon.svg"))
        )
        self.sign_in_button.setIconSize(
            QtCore.QSize(
                int(self.scaled_app_width / 20), int(self.scaled_app_height / 17)
            )
        )
        self.sign_in_button.setEnabled(False)
        self.sign_in_button.setCheckable(True)
        self.sign_in_button.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(
                color=QtGui.QColor(0, 0, 0, 100),
                blurRadius=30,
                xOffset=int(self.scaled_app_width / 300),
                yOffset=int(self.scaled_app_height / 350),
            )
        )

        self.user_connection_status = QtWidgets.QLabel(self.sign_in_menu)
        self.user_connection_status.setObjectName("User_Connection_Status")
        self.user_connection_status.setGeometry(
            0,
            int(self.scaled_app_height / 3.5),
            int(self.scaled_app_width / 3.62),
            int(self.scaled_app_height / 20),
        )
        self.user_connection_status.setText(
            "<html><head/><body><center>SIGNED-OUT       </center></body></html>"
        )

        # --- Extended Avatar Selection GUI ---
        self.avatar_selector_widget = QtWidgets.QStackedWidget(self)
        self.avatar_selector_widget.setGeometry(
            int(self.scaled_app_width / 25),
            int(self.scaled_app_height / 2.78),
            int(self.scaled_app_width / 5.12),
            int(self.scaled_app_height / 3.4),
        )
        self.avatar_selector_widget.setObjectName("Avatar_Selector_Widget")
        self.avatar_selector_widget.setVisible(False)
        self.avatar_selector_widget.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(
                color=QtGui.QColor(0, 0, 0, 50),
                blurRadius=20,
                xOffset=int(self.scaled_app_width / 300),
                yOffset=int(self.scaled_app_height / 300),
            )
        )
        self.avatar_selector_open_anim = QtCore.QPropertyAnimation(
            self.avatar_selector_widget, b"pos"
        )
        self.avatar_selector_open_anim.setStartValue(self.avatar_selector_widget.pos())
        self.avatar_selector_open_anim.setEndValue(
            QtCore.QPoint(int(self.scaled_app_width / 14.7), int(self.scaled_app_height / 2.78))
        )
        self.avatar_selector_open_anim.setDuration(20)

        self.avatar_selector_close_anim = QtCore.QPropertyAnimation(
            self.avatar_selector_widget, b"pos"
        )
        self.avatar_selector_close_anim.setStartValue(self.avatar_selector_widget.pos())
        self.avatar_selector_close_anim.setEndValue(
            QtCore.QPoint(int(self.scaled_app_width / 25), int(self.scaled_app_height / 2.78))
        )
        self.avatar_selector_close_anim.setDuration(25)

        self.avatar_selector_page1 = QtWidgets.QWidget()
        self.avatar_selector_page1.setObjectName("Avatar_Selector_Page_1")
        self.avatar_selector_page2 = QtWidgets.QWidget()
        self.avatar_selector_page2.setObjectName("Avatar_Selector_Page_2")
        self.avatar_selector_page3 = QtWidgets.QWidget()
        self.avatar_selector_page3.setObjectName("Avatar_Selector_Page_3")
        self.avatar_selector_widget.addWidget(self.avatar_selector_page1)
        self.avatar_selector_widget.addWidget(self.avatar_selector_page2)
        self.avatar_selector_widget.addWidget(self.avatar_selector_page3)
        self.avatar_selector_widget.setCurrentIndex(0)

        # --- Functions for Avatar Selection ---
        def select_avatar() -> None:
            """Allows selection of an avatar through the avatar selection window."""
            selected_avatar = self.sender()
            self.user_avatar.setIcon(
                QtGui.QIcon(os.path.join(os.getcwd(), "avatars", f"{selected_avatar.objectName()}.svg"))
            )
            self.temporary_avatar.setIcon(
                QtGui.QIcon(os.path.join(os.getcwd(), "avatars", f"{selected_avatar.objectName()}.svg"))
            )
            self.user_avatar.setObjectName(selected_avatar.objectName())
            self.user_avatar.toggle()
            self.avatar_selector_close_anim.start()
            if self.avatar_selector_widget.x() == int(self.scaled_app_width / 25):
                self.avatar_selector_widget.setVisible(False)

        def open_avatar_selector() -> None:
            """Opens or closes the avatar selection window."""
            if self.user_avatar.isChecked():
                self.avatar_selector_widget.setVisible(True)
                self.avatar_selector_open_anim.start()
            else:
                self.avatar_selector_close_anim.start()
                if self.avatar_selector_widget.x() == int(self.scaled_app_width / 25):
                    self.avatar_selector_widget.setVisible(False)

        def scroll_avatar_selector() -> None:
            """Allows flipping of pages in the avatar selection window."""
            current_index = self.avatar_selector_widget.currentIndex()
            next_index = current_index + 1 if current_index < 2 else 0
            self.avatar_selector_widget.setCurrentIndex(next_index)

        j_vals = [0, 1, 2, 3] * 9
        for i in range(36):
            if i < 4:
                page = self.avatar_selector_page1
                x = int(self.avatar_selector_widget.width() / 25) + (j_vals[i] * int(self.avatar_selector_widget.width() / 4.166))
                y = int(self.avatar_selector_widget.height() / 14.5)
            elif i < 8:
                page = self.avatar_selector_page1
                x = int(self.avatar_selector_widget.width() / 25) + (j_vals[i] * int(self.avatar_selector_widget.width() / 4.166))
                y = int(self.avatar_selector_widget.height() / 2.9)
            elif i < 12:
                page = self.avatar_selector_page1
                x = int(self.avatar_selector_widget.width() / 25) + (j_vals[i] * int(self.avatar_selector_widget.width() / 4.166))
                y = int(self.avatar_selector_widget.height() / 1.611)
            elif i < 16:
                page = self.avatar_selector_page2
                x = int(self.avatar_selector_widget.width() / 25) + (j_vals[i] * int(self.avatar_selector_widget.width() / 4.166))
                y = int(self.avatar_selector_widget.height() / 14.5)
            elif i < 20:
                page = self.avatar_selector_page2
                x = int(self.avatar_selector_widget.width() / 25) + (j_vals[i] * int(self.avatar_selector_widget.width() / 4.166))
                y = int(self.avatar_selector_widget.height() / 2.9)
            elif i < 24:
                page = self.avatar_selector_page2
                x = int(self.avatar_selector_widget.width() / 25) + (j_vals[i] * int(self.avatar_selector_widget.width() / 4.166))
                y = int(self.avatar_selector_widget.height() / 1.611)
            elif i < 28:
                page = self.avatar_selector_page3
                x = int(self.avatar_selector_widget.width() / 25) + (j_vals[i] * int(self.avatar_selector_widget.width() / 4.166))
                y = int(self.avatar_selector_widget.height() / 14.5)
            elif i < 32:
                page = self.avatar_selector_page3
                x = int(self.avatar_selector_widget.width() / 25) + (j_vals[i] * int(self.avatar_selector_widget.width() / 4.166))
                y = int(self.avatar_selector_widget.height() / 2.9)
            else:
                page = self.avatar_selector_page3
                x = int(self.avatar_selector_widget.width() / 25) + (j_vals[i] * int(self.avatar_selector_widget.width() / 4.166))
                y = int(self.avatar_selector_widget.height() / 1.611)
            user_btn = QtWidgets.QPushButton(page)
            user_btn.setObjectName(f"User{str(i + 1)}")
            user_btn.setGeometry(x, y,
                                 int(self.avatar_selector_widget.width() / 5),
                                 int(self.avatar_selector_widget.height() / 5.9))
            user_btn.setStyleSheet("background: transparent; border: none;")
            user_icon_path = os.path.join(os.getcwd(), "avatars", f"User{str(i + 1)}.svg")
            user_btn.setIcon(QtGui.QIcon(user_icon_path))
            user_btn.setIconSize(QtCore.QSize(
                int(self.avatar_selector_widget.width() / 5),
                int(self.avatar_selector_widget.height() / 5.9)
            ))
            user_btn.setGraphicsEffect(
                QtWidgets.QGraphicsDropShadowEffect(
                    color=QtGui.QColor(0, 0, 0, 100),
                    blurRadius=30,
                    xOffset=int(self.scaled_app_width / 350),
                    yOffset=int(self.scaled_app_height / 350)
                )
            )
            user_btn.clicked.connect(select_avatar)
            if i in [8, 20, 32]:
                next_btn = QtWidgets.QPushButton(page)
                next_btn.setObjectName("Avatar_Selector_Next_Button")
                next_btn.setGeometry(
                    int(self.avatar_selector_widget.width() / 1.29),
                    int(self.avatar_selector_widget.height() / 1.23),
                    int(self.avatar_selector_widget.width() / 5),
                    int(self.avatar_selector_widget.height() / 5.9)
                )
                next_btn.setStyleSheet("background: transparent; border: none;")
                next_icon = os.path.join(os.getcwd(), "icons", "next_icon.svg")
                next_btn.setIcon(QtGui.QIcon(next_icon))
                next_btn.setIconSize(QtCore.QSize(
                    int(self.avatar_selector_widget.width() / 6.25),
                    int(self.avatar_selector_widget.height() / 14.75)
                ))
                next_btn.setGraphicsEffect(
                    QtWidgets.QGraphicsDropShadowEffect(
                        color=QtGui.QColor(0, 0, 0, 100),
                        blurRadius=10,
                        xOffset=int(self.scaled_app_width / 300),
                        yOffset=int(self.scaled_app_height / 350)
                    )
                )
                next_btn.clicked.connect(scroll_avatar_selector)

        # --- Chat Settings Menu Widgets ---
        self.chat_settings_icon = QtWidgets.QPushButton(self.chat_settings_menu)
        self.chat_settings_icon.setObjectName("Chat_Settings_Icon")
        self.chat_settings_icon.setGeometry(
            int(self.scaled_app_width / 65),
            int(self.scaled_app_height / 60),
            int(self.scaled_app_width / 23),
            int(self.scaled_app_height / 17)
        )
        self.chat_settings_icon.setStyleSheet("background: transparent; border: none;")
        self.chat_settings_icon.setIcon(
            QtGui.QIcon(os.path.join(os.getcwd(), "icons", "chat_icon.svg"))
        )
        self.chat_settings_icon.setIconSize(
            QtCore.QSize(
                int(self.scaled_app_width / 23),
                int(self.scaled_app_height / 19)
            )
        )
        self.chat_settings_icon.setCheckable(True)
        self.chat_settings_icon.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(
                color=QtGui.QColor(0, 0, 0, 100),
                blurRadius=30,
                xOffset=int(self.scaled_app_width / 350),
                yOffset=int(self.scaled_app_height / 350)
            )
        )
        self.chat_settings_icon.raise_()

        self.chat_settings_title = QtWidgets.QLabel(self.chat_settings_menu)
        self.chat_settings_title.setObjectName("Chat_Settings_Title")
        self.chat_settings_title.setGeometry(
            int(self.scaled_app_width / 13.2),
            int(self.scaled_app_height / 33),
            int(self.scaled_app_width / 5),
            int(self.scaled_app_height / 34)
        )
        self.chat_settings_title.setText("Chat Settings")

        self.chat_theme_title = QtWidgets.QLabel(self.chat_settings_menu)
        self.chat_theme_title.setObjectName("Chat_Theme_Title")
        self.chat_theme_title.setGeometry(
            int(self.scaled_app_width / 12.8),
            int(self.scaled_app_height / 11.2),
            int(self.scaled_app_width / 5),
            int(self.scaled_app_height / 34)
        )
        self.chat_theme_title.setText("Theme")

        self.chat_theme = QtWidgets.QComboBox(self.chat_settings_menu)
        self.chat_theme.setObjectName("Chat_Theme")
        self.chat_theme.setGeometry(
            int(self.scaled_app_width / 13.2),
            int(self.scaled_app_height / 7.7),
            int(self.scaled_app_width / 11.6),
            int(self.scaled_app_height / 33)
        )
        self.chat_theme.addItems(["Default", "Blue", "Dark", "Light"])
        self.chat_theme.setEnabled(False)
        self.chat_theme.currentIndexChanged.connect(
            lambda: self.theme(self.chat_theme.currentText())
        )

        self.chat_selector_title = QtWidgets.QLabel(self.chat_settings_menu)
        self.chat_selector_title.setObjectName("Chat_Selector_Title")
        self.chat_selector_title.setGeometry(
            int(self.scaled_app_width / 12.8),
            int(self.scaled_app_height / 5),
            int(self.scaled_app_width / 5),
            int(self.scaled_app_height / 34)
        )
        self.chat_selector_title.setText("Recipient")

        self.chat_selector = QtWidgets.QComboBox(self.chat_settings_menu)
        self.chat_selector.setObjectName("Chat_Selector")
        self.chat_selector.setGeometry(
            int(self.scaled_app_width / 13),
            int(self.scaled_app_height / 4.15),
            int(self.scaled_app_width / 11.6),
            int(self.scaled_app_height / 33)
        )
        self.chat_selector.addItem("ALL")
        self.chat_selector.setEnabled(False)

        self.chat_confirm_button = QtWidgets.QPushButton(self.chat_settings_menu)
        self.chat_confirm_button.setObjectName("Chat_Confirm_Button")
        self.chat_confirm_button.setGeometry(
            int(self.scaled_app_width / 4.7),
            int(self.scaled_app_height / 4.4),
            int(self.scaled_app_width / 25),
            int(self.scaled_app_height / 20)
        )
        self.chat_confirm_button.setStyleSheet("background: transparent; border: none;")
        self.chat_confirm_button.setIcon(
            QtGui.QIcon(os.path.join(os.getcwd(), "icons", "check_icon.svg"))
        )
        self.chat_confirm_button.setIconSize(
            QtCore.QSize(
                int(self.scaled_app_width / 21),
                int(self.scaled_app_height / 18)
            )
        )
        self.chat_confirm_button.setEnabled(False)
        self.chat_confirm_button.setCheckable(True)
        self.chat_confirm_button.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(
                color=QtGui.QColor(0, 0, 0, 100),
                blurRadius=30,
                xOffset=int(self.scaled_app_width / 300),
                yOffset=int(self.scaled_app_height / 350)
            )
        )

        # --- Overlays for OS Drop-down Customization ---
        # Chat Theme Drop-down Overlay
        self.chat_theme_dropdown_bg = QtWidgets.QLabel(self.chat_theme)
        self.chat_theme_dropdown_bg.setObjectName("Chat_Theme_Drop_Down_Background")
        self.chat_theme_dropdown_bg.setGeometry(
            int(self.chat_theme.x() / 1.26), 0,
            int(self.chat_theme.width() / 3),
            int(self.chat_theme.height())
        )
        self.chat_theme_dropdown_btn = QtWidgets.QPushButton(self.chat_theme)
        self.chat_theme_dropdown_btn.setObjectName("Chat_Theme_Drop_Down")
        self.chat_theme_dropdown_btn.setGeometry(
            int(self.chat_theme.x() / 1.26), 0,
            int(self.chat_theme.width() / 3),
            int(self.chat_theme.height() * 0.9)
        )
        self.chat_theme_dropdown_btn.setStyleSheet("background: transparent; border: none;")
        self.chat_theme_dropdown_btn.setIcon(
            QtGui.QIcon(os.path.join(os.getcwd(), "icons", "drop_down_icon.svg"))
        )
        self.chat_theme_dropdown_btn.setIconSize(
            QtCore.QSize(
                int(self.scaled_app_width / 25.6),
                int(self.scaled_app_height / 20.7)
            )
        )
        self.chat_theme_dropdown_btn.setVisible(False)

        # Chat Selector Drop-down Overlay
        self.chat_selector_dropdown_bg = QtWidgets.QLabel(self.chat_selector)
        self.chat_selector_dropdown_bg.setObjectName("Chat_Selector_Drop_Down_Background")
        self.chat_selector_dropdown_bg.setGeometry(
            int(self.chat_selector.x() / 1.3), 0,
            int(self.chat_selector.width() / 3),
            int(self.chat_selector.height())
        )
        self.chat_selector_dropdown_btn = QtWidgets.QPushButton(self.chat_selector)
        self.chat_selector_dropdown_btn.setObjectName("Chat_Selector_Drop_Down")
        self.chat_selector_dropdown_btn.setGeometry(
            int(self.chat_selector.x() / 1.3), 0,
            int(self.chat_selector.width() / 3),
            int(self.chat_selector.height() * 0.9)
        )
        self.chat_selector_dropdown_btn.setStyleSheet("background: transparent; border: none;")
        self.chat_selector_dropdown_btn.setIcon(
            QtGui.QIcon(os.path.join(os.getcwd(), "icons", "drop_down_icon.svg"))
        )
        self.chat_selector_dropdown_btn.setIconSize(
            QtCore.QSize(
                int(self.scaled_app_width / 25.6),
                int(self.scaled_app_height / 20.7)
            )
        )
        self.chat_selector_dropdown_btn.setVisible(False)

        # --- Chat Log Area ---
        self.chat_log = QtWidgets.QListWidget(self)
        self.chat_log.setGeometry(
            int(self.scaled_app_width / 3.2),
            int(self.scaled_app_height / 25.8),
            int(self.scaled_app_width / 1.52),
            int(self.scaled_app_height / 1.2)
        )
        self.chat_log.setObjectName("Chat_Log")
        self.chat_log.setEnabled(False)

        # --- Message Field and Attach Button ---
        self.message_field = QtWidgets.QLineEdit(self)
        self.message_field.setObjectName("Message_Field")
        self.message_field.setGeometry(
            int(self.scaled_app_width / 3.2),
            int(self.scaled_app_height),
            int(self.scaled_app_width / 1.68),
            int(self.scaled_app_height / 20.7)
        )
        self.message_field.setText("Waiting for connection...")
        self.message_field.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(
                color=QtGui.QColor(0, 0, 0, 25),
                blurRadius=60,
                xOffset=int(self.scaled_app_width / 128),
                yOffset=int(self.scaled_app_height / 103.5)
            )
        )
        self.message_field.setEnabled(False)

        self.message_field_anim = QtCore.QPropertyAnimation(self.message_field, b"pos")
        self.message_field_anim.setStartValue(self.message_field.pos())
        self.message_field_anim.setEndValue(
            QtCore.QPoint(int(self.scaled_app_width / 3.2), int(self.scaled_app_height / 1.1))
        )
        self.message_field_anim.setDuration(150)

        self.attach_button = QtWidgets.QPushButton(self)
        self.attach_button.setObjectName("Attach_Button")
        self.attach_button.setGeometry(
            int(self.scaled_app_width / 1.075),
            int(self.scaled_app_height),
            int(self.scaled_app_width / 25.09),
            int(self.scaled_app_height / 20.29)
        )
        self.attach_button.setStyleSheet("background: transparent; border: none;")
        self.attach_button.setIcon(
            QtGui.QIcon(os.path.join(os.getcwd(), "icons", "attach_icon.svg"))
        )
        self.attach_button.setIconSize(
            QtCore.QSize(
                int(self.scaled_app_width / 25.6),
                int(self.scaled_app_height / 20.7)
            )
        )
        self.attach_button.setEnabled(False)

        self.attach_button_anim = QtCore.QPropertyAnimation(self.attach_button, b"pos")
        self.attach_button_anim.setStartValue(self.attach_button.pos())
        self.attach_button_anim.setEndValue(
            QtCore.QPoint(int(self.scaled_app_width / 1.075), int(self.scaled_app_height / 1.1))
        )
        self.attach_button_anim.setDuration(150)

    def _setup_animations(self) -> None:
        """Additional animations were set up during widget creation."""
        pass

    def _setup_drop_down_overlays(self) -> None:
        """
        (The custom overlays for the Chat Theme and Chat Selector drop-downs are created in _setup_ui.
         This method exists to indicate that these widgets must be created after their parent widgets.)
        """
        pass

    def _connect_signals(self) -> None:
        """Connect widget signals to their respective slot functions."""
        self.socket.readyRead.connect(self.receive_message)
        self.server_button.clicked.connect(self.connect_client)
        self.user_avatar.clicked.connect(lambda: self.open_avatar_selector())
        self.sign_in_button.clicked.connect(self.sign_in)
        self.chat_theme_dropdown_btn.clicked.connect(lambda: self.better_drop_down(0))
        self.chat_selector_dropdown_btn.clicked.connect(lambda: self.better_drop_down(1))
        self.chat_confirm_button.clicked.connect(self.chat_target)
        self.message_field.returnPressed.connect(
            lambda: self.send_message(
                f"{{FIELD}}{{{self.chat_selector.currentText()}}}" + self.message_field.text()
            )
        )
        self.attach_button.clicked.connect(self.attach_picture)

    def theme(self, theme_name: str) -> None:
        """Apply a theme based on the user selection."""
        if theme_name == "Default":
            Main_Background_Color = "#28284E"
            Main_Title_Color = "#A599E9"
            Main_Text_Color = "#FFFFFF"
            Main_Text_Alternate_Color = "#FAD000"
            Main_Underline_Color = "#544F83"
            Main_Status_Banner_Disconnected_Color = "#DE486F"
            Main_Status_Banner_Connected_Color = "#8FE47F"
            Main_Status_Banner_Shadow_Color = "#202044"
            Main_Chat_Log_Background_Color = "#F0F0F0"
            Main_Chat_Log_Text_Color = "#000000"
            Main_Message_Field_Background_Color = "#FFFFFF"
            Main_Message_Field_Text_Color = "#000000"
        elif theme_name == "Blue":
            Main_Background_Color = "#073642"
            Main_Title_Color = "#94A1A1"
            Main_Text_Color = "#EEE8D5"
            Main_Text_Alternate_Color = "#268BD2"
            Main_Underline_Color = "#576A71"
            Main_Status_Banner_Disconnected_Color = "#CD3080"
            Main_Status_Banner_Connected_Color = "#8FE47F"
            Main_Status_Banner_Shadow_Color = "#002B36"
            Main_Chat_Log_Background_Color = "#00212B"
            Main_Chat_Log_Text_Color = "#EEE8D5"
            Main_Message_Field_Background_Color = "#125252"
            Main_Message_Field_Text_Color = "#EEE8D5"
        elif theme_name == "Dark":
            Main_Background_Color = "#272822"
            Main_Title_Color = "#FCFAF2"
            Main_Text_Color = "#E1E676"
            Main_Text_Alternate_Color = "#D33682"
            Main_Underline_Color = "#544F83"
            Main_Status_Banner_Disconnected_Color = "#FD275A"
            Main_Status_Banner_Connected_Color = "#8FE47F"
            Main_Status_Banner_Shadow_Color = "#1E1F1C"
            Main_Chat_Log_Background_Color = "#1E1F1C"
            Main_Chat_Log_Text_Color = "#65D9EF"
            Main_Message_Field_Background_Color = "#414339"
            Main_Message_Field_Text_Color = "#65D9EF"
        elif theme_name == "Light":
            Main_Background_Color = "#E3E3E9"
            Main_Title_Color = "#073642"
            Main_Text_Color = "#657B83"
            Main_Text_Alternate_Color = "#2A8FDA"
            Main_Underline_Color = "#93A1A1"
            Main_Status_Banner_Disconnected_Color = "#CD3080"
            Main_Status_Banner_Connected_Color = "#5AE150"
            Main_Status_Banner_Shadow_Color = "#E6E6E6"
            Main_Chat_Log_Background_Color = "#F0F0F0"
            Main_Chat_Log_Text_Color = "#073642"
            Main_Message_Field_Background_Color = "#C0C0D8"
            Main_Message_Field_Text_Color = "#6A5878"
        else:
            self.logger.error(f"Unknown theme: {theme_name}")
            return

        self.server_settings_menu.setStyleSheet(f"background: {Main_Background_Color}")
        self.server_settings_title.setStyleSheet(f"color: {Main_Title_Color}; font: {self.scaled_font_size}px;")
        self.host_title.setStyleSheet(f"color: {Main_Title_Color}; font: {self.scaled_font_size}px;")
        self.host_address.setStyleSheet(
            f"background: transparent; border: transparent; border-bottom: {self.scaled_underline_size} solid {Main_Underline_Color}; padding: 0 5px; color: {Main_Text_Color}; font: {self.scaled_font_size}px;"
        )
        self.port_title.setStyleSheet(f"color: {Main_Title_Color}; font: {self.scaled_font_size}px;")
        self.port_number.setStyleSheet(
            f"background: transparent; border: transparent; border-bottom: {self.scaled_underline_size} solid {Main_Underline_Color}; padding: 0 5px; color: {Main_Text_Alternate_Color}; font: {self.scaled_font_size}px;"
        )
        if self.server_connection_status.text() == "<html><head/><body><center>NOT CONNECTED</center></body></html>":
            self.server_connection_status.setStyleSheet(
                f"color: {Main_Status_Banner_Disconnected_Color}; background: transparent; border-bottom: 2px solid {Main_Status_Banner_Shadow_Color}; font: {self.scaled_font_size}px;"
            )
        else:
            self.server_connection_status.setStyleSheet(
                f"color: {Main_Status_Banner_Connected_Color}; background: transparent; border-bottom: 2px solid {Main_Status_Banner_Shadow_Color}; font: {self.scaled_font_size}px;"
            )
        self.sign_in_menu.setStyleSheet(f"background: {Main_Background_Color}")
        self.sign_in_title.setStyleSheet(f"color: {Main_Title_Color}; font: {self.scaled_font_size}px;")
        self.username_title.setStyleSheet(f"color: {Main_Title_Color}; font: {self.scaled_font_size}px;")
        self.username.setStyleSheet(
            f"background: transparent; border: transparent; border-bottom: {self.scaled_underline_size} solid {Main_Underline_Color}; padding: 0 5px; color: {Main_Text_Color}; font: {self.scaled_font_size}px;"
        )
        self.password_title.setStyleSheet(f"color: {Main_Title_Color}; font: {self.scaled_font_size}px;")
        self.password.setStyleSheet(
            f"background: transparent; border: transparent; border-bottom: {self.scaled_underline_size} solid {Main_Underline_Color}; padding: 0 5px; color: {Main_Text_Alternate_Color}; font: {self.scaled_font_size}px;"
        )
        if self.user_connection_status.text() == "<html><head/><body><center>SIGNED-OUT       </center></body></html>":
            self.user_connection_status.setStyleSheet(
                f"color: {Main_Status_Banner_Disconnected_Color}; background: transparent; border-bottom: 2px solid {Main_Status_Banner_Shadow_Color}; font: {self.scaled_font_size}px;"
            )
        else:
            self.user_connection_status.setStyleSheet(
                f"color: {Main_Status_Banner_Connected_Color}; background: transparent; border-bottom: 2px solid {Main_Status_Banner_Shadow_Color}; font: {self.scaled_font_size}px;"
            )
        self.chat_settings_menu.setStyleSheet(f"background: {Main_Background_Color}")
        self.chat_settings_title.setStyleSheet(f"color: {Main_Title_Color}; font: {self.scaled_font_size}px;")
        self.chat_theme_title.setStyleSheet(f"color: {Main_Title_Color}; font: {self.scaled_font_size}px;")
        self.chat_theme.setStyleSheet(
            f"background: {Main_Background_Color}; border: none; border-bottom: {self.scaled_underline_size} solid {Main_Underline_Color}; padding: 0 5px; color: {Main_Text_Color}; font: {self.scaled_font_size}px;"
        )
        self.chat_selector_title.setStyleSheet(f"color: {Main_Title_Color}; font: {self.scaled_font_size}px;")
        self.chat_selector.setStyleSheet(
            f"background: {Main_Background_Color}; border: none; border-bottom: {self.scaled_underline_size} solid {Main_Underline_Color}; padding: 0 5px; color: {Main_Text_Alternate_Color}; font: {self.scaled_font_size}px;"
        )
        self.chat_theme_dropdown_bg.setStyleSheet(f"background: {Main_Background_Color}")
        self.chat_selector_dropdown_bg.setStyleSheet(f"background: {Main_Background_Color}")
        self.setStyleSheet(f"background-color: {Main_Chat_Log_Background_Color}")
        self.chat_log.setStyleSheet(
            f"border: none; color: {Main_Chat_Log_Text_Color}; background-color: {Main_Chat_Log_Background_Color}; padding: 10px 20px; font: {self.scaled_font_size}px;"
        )
        self.message_field.setStyleSheet(
            f"border: none; color: {Main_Message_Field_Text_Color}; background-color: {Main_Message_Field_Background_Color}; border-radius: {self.scaled_border_radius}px; padding: 0 15px; font: {self.scaled_font_size}px;"
        )

    def connect_client(self) -> None:
        """
        Connects to the server using the provided hostname and port.
        Also checks the Protocol selector to use UDP or TCP.
        """
        # Adjust socket type if needed based on protocol selection.
        protocol = self.protocol_selector.currentText()
        if protocol == "TCP":
            if not isinstance(self.socket, QtNetwork.QTcpSocket):
                self.socket.deleteLater()
                self.socket = QtNetwork.QTcpSocket(self)
        else:  # UDP
            if not isinstance(self.socket, QtNetwork.QUdpSocket):
                self.socket.deleteLater()
                self.socket = QtNetwork.QUdpSocket(self)

        if self.server_button.isChecked():
            host = self.host_address.text()
            try:
                port = int(self.port_number.text())
            except ValueError:
                self.logger.error("Invalid port number")
                return
            self.socket.connectToHost(QtNetwork.QHostAddress(host), port)
            self.send_message("{CONNECT}")
            self.server_button.setIcon(
                QtGui.QIcon(os.path.join(os.getcwd(), "icons", "exit_icon.svg"))
            )
            self.server_connection_status.setText(
                "<html><head/><body><center>CONNECTED     </center></body></html>"
            )
            self.theme(self.chat_theme.currentText())
            self.host_address.setEnabled(False)
            self.port_number.setEnabled(False)
            self.temporary_avatar.setVisible(False)
            self.user_avatar.setVisible(True)
            self.username.setEnabled(True)
            self.sign_in_button.setEnabled(True)
            self.message_field.setText("Waiting for sign-in...")
        else:
            self.send_message("{DISCONNECT}")
            self.server_button.setIcon(
                QtGui.QIcon(os.path.join(os.getcwd(), "icons", "enter_icon.svg"))
            )
            self.server_connection_status.setText(
                "<html><head/><body><center>NOT CONNECTED</center></body></html>"
            )
            self.theme(self.chat_theme.currentText())
            self.host_address.setEnabled(True)
            self.port_number.setEnabled(True)
            self.temporary_avatar.setVisible(True)
            self.user_avatar.setVisible(False)
            self.username.setEnabled(False)
            self.sign_in_button.setEnabled(False)
            self.message_field.setText("Dissconnected! Good Bye...")

    def sign_in(self) -> None:
        """Registers or unregisters the username with the server."""
        if self.sign_in_button.isChecked():
            self.send_message("{REGISTER}")
            self.server_button.setEnabled(False)
            self.sign_in_button.setIcon(
                QtGui.QIcon(os.path.join(os.getcwd(), "icons", "exit_icon.svg"))
            )
            self.user_connection_status.setText(
                "<html><head/><body><center>SIGNED-IN        </center></body></html>"
            )
            self.theme(self.chat_theme.currentText())
            self.username.setEnabled(False)
            self.temporary_avatar.setVisible(True)
            self.user_avatar.setVisible(False)
            self.chat_theme.setEnabled(True)
            self.chat_theme_dropdown_btn.setVisible(True)
            self.chat_selector.setEnabled(True)
            self.chat_selector.setItemText(0, "ALL")
            self.chat_selector_dropdown_btn.setVisible(True)
            self.chat_confirm_button.setEnabled(True)
            self.message_field.setText("Select a user to start chatting...")
            self.chat_log.setEnabled(True)
        else:
            self.send_message("{UNREGISTER}")
            self.server_button.setEnabled(True)
            self.sign_in_button.setIcon(
                QtGui.QIcon(os.path.join(os.getcwd(), "icons", "enter_icon.svg"))
            )
            self.user_connection_status.setText(
                "<html><head/><body><center>SIGNED-OUT       </center></body></html>"
            )
            self.theme(self.chat_theme.currentText())
            self.username.setEnabled(True)
            self.temporary_avatar.setVisible(False)
            self.user_avatar.setVisible(True)
            self.chat_theme.setEnabled(False)
            self.chat_theme_dropdown_btn.setVisible(False)
            self.chat_selector.setEnabled(False)
            self.chat_selector_dropdown_btn.setVisible(False)
            self.chat_confirm_button.setEnabled(False)
            self.message_field.setText("Signed Out!...") 
            self.chat_log.setEnabled(False)

    def send_message(self, message: str, host: str = "127.0.0.1", port: int = 33002) -> None:
        """
        Sends a message using the chosen protocol.
        For UDP, uses writeDatagram; for TCP, uses write.
        """
        protocol = self.protocol_selector.currentText()
        if protocol == "UDP":
            if message.startswith("{FIELD}"):
                message = message.replace("{FIELD}", "")
                self.socket.writeDatagram(message.encode(), QtNetwork.QHostAddress(host), port)
                self.message_field.setText("")
                self.message_field.setFocus()
            else:
                self.socket.writeDatagram(message.encode(), QtNetwork.QHostAddress(host), port)
        else:  # TCP
            if message.startswith("{FIELD}"):
                message = message.replace("{FIELD}", "")
                self.socket.write(message.encode())
                self.message_field.setText("")
                self.message_field.setFocus()
            else:
                self.socket.write(message.encode())

    def receive_message(self) -> None:
        """
        Receives messages using the chosen protocol.
        For UDP, reads datagrams; for TCP, reads available bytes.
        """
        protocol = self.protocol_selector.currentText()
        if protocol == "UDP":
            while self.socket.hasPendingDatagrams():
                datagram, _, _ = self.socket.readDatagram(self.socket.pendingDatagramSize())
                received_message = datagram.decode()
                if received_message.startswith("{MSG}"):
                    received_message = received_message.replace("{MSG}", "")
                    self.chat_log.addItem(received_message)
        else:  # TCP
            if self.socket.bytesAvailable() > 0:
                data = self.socket.readAll().data().decode()
                if data.startswith("{MSG}"):
                    data = data.replace("{MSG}", "")
                    self.chat_log.addItem(data)

    def better_drop_down(self, whom: int) -> None:
        """
        Mimics a cleaner drop-down behavior.
        whom == 0 for Chat Theme; whom == 1 for Chat Selector.
        """
        if whom == 0:
            self.chat_theme_dropdown_btn.parent().showPopup()
        elif whom == 1:
            self.chat_selector_dropdown_btn.parent().showPopup()

    def chat_target(self) -> None:
        """
        Handles chat recipient confirmation.
        Enables message field and disables selection widgets if confirmed.
        """
        if self.chat_confirm_button.isChecked():
            self.chat_confirm_button.setIcon(
                QtGui.QIcon(QtGui.QPixmap(os.path.join(os.getcwd(), "icons", "cancel_icon.svg")))
            )
            self.chat_theme.setEnabled(False)
            self.chat_theme_dropdown_btn.setVisible(False)
            self.chat_selector.setEnabled(False)
            self.chat_selector_dropdown_btn.setVisible(False)
            self.sign_in_button.setEnabled(False)
            self.message_field.setEnabled(True)
            self.message_field.setText("")
            self.message_field.setFocus()
            self.chat_log.setEnabled(True)
            self.attach_button.setEnabled(True)
        else:
            self.chat_confirm_button.setIcon(
                QtGui.QIcon(QtGui.QPixmap(os.path.join(os.getcwd(), "icons", "check_icon.svg")))
            )
            self.chat_theme.setEnabled(True)
            self.chat_theme_dropdown_btn.setVisible(True)
            self.chat_selector.setEnabled(True)
            self.chat_selector_dropdown_btn.setVisible(True)
            self.sign_in_button.setEnabled(True)
            self.message_field.setEnabled(False)
            self.message_field.setText("Select a User to start chatting...")
            self.chat_log.setEnabled(False)
            self.attach_button.setEnabled(False)

    def attach_picture(self) -> None:
        """Opens a file dialog to attach an image to the chat log."""
        image_tuple = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Attach an Image', os.getcwd(), "Image files (*.jpg *.png *.gif *.svg)"
        )
        if image_tuple[0]:
            attached_item = QtWidgets.QListWidgetItem("\n\n\n\n")
            attached_item.setIcon(QtGui.QIcon(image_tuple[0]))
            self.chat_log.setIconSize(
                QtCore.QSize(int(self.scaled_app_width / 20), int(self.scaled_app_height / 17))
            )
            self.chat_log.addItem(attached_item)

    def _connect_signals(self) -> None:
        """Connect signals to their corresponding slot functions."""
        self.socket.readyRead.connect(self.receive_message)
        self.server_button.clicked.connect(self.connect_client)
        self.user_avatar.clicked.connect(lambda: self.open_avatar_selector())
        self.sign_in_button.clicked.connect(self.sign_in)
        self.chat_theme_dropdown_btn.clicked.connect(lambda: self.better_drop_down(0))
        self.chat_selector_dropdown_btn.clicked.connect(lambda: self.better_drop_down(1))
        self.chat_confirm_button.clicked.connect(self.chat_target)
        self.message_field.returnPressed.connect(
            lambda: self.send_message(
                f"{{FIELD}}{{{self.chat_selector.currentText()}}}" + self.message_field.text()
            )
        )
        self.attach_button.clicked.connect(self.attach_picture)

    def open_avatar_selector(self) -> None:
        """Opens or closes the avatar selection widget based on the toggle state."""
        if self.user_avatar.isChecked():
            self.avatar_selector_widget.setVisible(True)
            self.avatar_selector_open_anim.start()
        else:
            self.avatar_selector_close_anim.start()
            if self.avatar_selector_widget.x() == int(self.scaled_app_width / 25):
                self.avatar_selector_widget.setVisible(False)

def main() -> None:
    """Entry point for the chat client application."""
    app = QtWidgets.QApplication(sys.argv)
    client = ChatClient()
    client.show()
    # Start animations for menus/buttons
    client.server_settings_menu_anim.start()
    client.sign_in_menu_anim.start()
    client.chat_settings_menu_anim.start()
    client.message_field_anim.start()
    client.attach_button_anim.start()
    client._connect_signals()  # Connect all signals
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
