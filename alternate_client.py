import sys, os, subprocess
from PyQt5 import QtCore, QtGui, QtWidgets
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def Window():
# Intializes the chat window and the client socket:
    client_socket = socket(AF_INET, SOCK_STREAM)
    app = QtWidgets.QApplication(sys.argv)

# Custom High DPI Scalling as the builtin Qt HDPi is not working well:
    screen_size = app.primaryScreen().availableGeometry()
    scaled_app_width = int(screen_size.width()/3)
    scaled_app_height = int(screen_size.height()/2)
    scaled_border_radius = str(int(screen_size.height()/86.4))
    scaled_font_size = str(int(screen_size.height()/100))
    scaled_underline_size = str(int(screen_size.height()/720))

    Chat_Window = QtWidgets.QDialog()
    Chat_Window.setObjectName("Chat_Window")
    Chat_Window.setGeometry(int(screen_size.width()/2)-int(scaled_app_width/2),int(screen_size.height()/2)-int(scaled_app_height/2),scaled_app_width,scaled_app_height)
    Chat_Window.setWindowTitle("  texte") # Chosen Brand Name for the Client
    Chat_Window.setWindowIcon(QtGui.QIcon(os.getcwd() + "/icons/texte_icon.svg"))

# Creates the left menu bar:
    Chat_Settings_Menu = QtWidgets.QFrame(Chat_Window)
    Chat_Settings_Menu.setObjectName("Chat_Settings_Menu")
    Chat_Settings_Menu.setGeometry(-int(scaled_app_width/30), int(2*scaled_app_height/3), int(scaled_app_width/3.62), int(scaled_app_height/2.9))
    Chat_Settings_Menu.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(color=QtGui.QColor(0, 0, 0, 25), blurRadius=60, xOffset=int(scaled_app_width/128), yOffset=int(scaled_app_height/103.5)))

    Chat_Settings_Menu_Animation = QtCore.QPropertyAnimation(Chat_Settings_Menu, b'pos')
    Chat_Settings_Menu_Animation.setStartValue(Chat_Settings_Menu.pos())
    Chat_Settings_Menu_Animation.setEndValue(QtCore.QPoint(0, int(2*scaled_app_height/3)))
    Chat_Settings_Menu_Animation.setDuration(150)

    Sign_In_Menu = QtWidgets.QFrame(Chat_Window)
    Sign_In_Menu.setObjectName("Sign_In_Menu")
    Sign_In_Menu.setGeometry(-int(scaled_app_width/20), int(scaled_app_height/3), int(scaled_app_width/3.62), int(scaled_app_height/3))
    Sign_In_Menu.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(color=QtGui.QColor(0, 0, 0, 25), blurRadius=60, xOffset=int(scaled_app_width/128), yOffset=int(scaled_app_height/103.5)))

    Sign_In_Menu_Animation = QtCore.QPropertyAnimation(Sign_In_Menu, b'pos')
    Sign_In_Menu_Animation.setStartValue(Sign_In_Menu.pos())
    Sign_In_Menu_Animation.setEndValue(QtCore.QPoint(0, int(scaled_app_height/3)))
    Sign_In_Menu_Animation.setDuration(150)

    Server_Settings_Menu = QtWidgets.QFrame(Chat_Window)
    Server_Settings_Menu.setObjectName("Server_Settings_Menu")
    Server_Settings_Menu.setGeometry(-int(scaled_app_width/10), 0, int(scaled_app_width/3.62), int(scaled_app_height/3))
    Server_Settings_Menu.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(color=QtGui.QColor(0, 0, 0, 25), blurRadius=60, xOffset=int(scaled_app_width/128), yOffset=int(scaled_app_height/103.5)))
    
    Server_Settings_Menu_Animation = QtCore.QPropertyAnimation(Server_Settings_Menu, b'pos')
    Server_Settings_Menu_Animation.setStartValue(Server_Settings_Menu.pos())
    Server_Settings_Menu_Animation.setEndValue(QtCore.QPoint(0, 0))
    Server_Settings_Menu_Animation.setDuration(150)

# Creates the 'server settings' submenu:
    Server_Settings_Icon = QtWidgets.QLabel(Server_Settings_Menu)
    Server_Settings_Icon.setObjectName("Server_Settings_Icon")
    Server_Settings_Icon.setGeometry(int(scaled_app_width/60), int(scaled_app_height/45), int(scaled_app_width/28), int(scaled_app_height/22))
    Server_Settings_Icon.setPixmap(QtGui.QPixmap(os.getcwd() + "/icons/server_icon.svg"))
    Server_Settings_Icon.setScaledContents(True)

    Server_Settings_Title = QtWidgets.QLabel(Server_Settings_Menu)
    Server_Settings_Title.setObjectName("Server_Settings_Title")
    Server_Settings_Title.setGeometry(int(scaled_app_width/13.2), int(scaled_app_height/33), int(scaled_app_width/5), int(scaled_app_height/34))
    Server_Settings_Title.setText("Server Settings")

    Host_Title = QtWidgets.QLabel(Server_Settings_Menu)
    Host_Title.setObjectName("Host_Title")
    Host_Title.setGeometry(int(scaled_app_width/12.8), int(scaled_app_height/11.2), int(scaled_app_width/5), int(scaled_app_height/34))
    Host_Title.setText("Hostname")

    Host_Address = QtWidgets.QLineEdit(Server_Settings_Menu)
    Host_Address.setObjectName("Host_Address")
    Host_Address.setGeometry(int(scaled_app_width/13.2), int(scaled_app_height/7.7), int(scaled_app_width/11.6), int(scaled_app_height/33))
    Host_Address.setText("127.0.0.1") # Prefilled default as also provided in server.py

    Port_Title = QtWidgets.QLabel(Server_Settings_Menu)
    Port_Title.setObjectName("Port_Title")
    Port_Title.setGeometry(int(scaled_app_width/12.8), int(scaled_app_height/5.6), int(scaled_app_width/5), int(scaled_app_height/34))
    Port_Title.setText("Port #")

    Port_Number = QtWidgets.QLineEdit(Server_Settings_Menu)
    Port_Number.setObjectName("Port_Number")
    Port_Number.setGeometry(int(scaled_app_width/13.2), int(scaled_app_height/4.56), int(scaled_app_width/11.6), int(scaled_app_height/33))
    Port_Number.setText("33002") # Prefilled default as also provided in server.py
    
    Server_Button = QtWidgets.QPushButton(Server_Settings_Menu)
    Server_Button.setObjectName("Server_Button")   
    Server_Button.setGeometry(int(scaled_app_width/4.7), int(scaled_app_height/5.1), int(scaled_app_width/25), int(scaled_app_height/20))
    Server_Button.setStyleSheet("background: transparent; border: none;")
    Server_Button.setIcon(QtGui.QIcon(os.getcwd() + "/icons/enter_icon.svg"))
    Server_Button.setIconSize(QtCore.QSize(int(scaled_app_width/20), int(scaled_app_height/17)))
    Server_Button.setCheckable(True) # Turns the pushbutton into a toggle switch

    Server_Connection_Status = QtWidgets.QLabel(Server_Settings_Menu)
    Server_Connection_Status.setObjectName("Server_Connection_Status")
    Server_Connection_Status.setGeometry(0, int(scaled_app_height/3.5), int(scaled_app_width/3.62), int(scaled_app_height/20))
    Server_Connection_Status.setText("<html><head/><body><center>NOT CONNECTED</center></body></html>")

# Creates the 'sign-in' submenu with FAKE password (NO AUTH):
    User_Avatar = QtWidgets.QPushButton(Sign_In_Menu)
    User_Avatar.setObjectName("user1") 
    User_Avatar.setGeometry(int(scaled_app_width/65), int(scaled_app_height/48), int(scaled_app_width/20), int(scaled_app_height/15))
    User_Avatar.setStyleSheet("background: transparent; border: none;")
    User_Avatar.setIcon(QtGui.QIcon("avatars/user1.svg"))
    User_Avatar.setIconSize(QtCore.QSize(int(scaled_app_width/20), int(scaled_app_height/17)))
    User_Avatar.setCheckable(True) # Turns the pushbutton into a toggle switch

    Temporary_Avatar = QtWidgets.QPushButton(Sign_In_Menu)
    Temporary_Avatar.setObjectName("Temporary_Avatar")
    Temporary_Avatar.setGeometry(int(scaled_app_width/65), int(scaled_app_height/48), int(scaled_app_width/20), int(scaled_app_height/15))
    Temporary_Avatar.setStyleSheet("background: transparent; border: none;")
    Temporary_Avatar.setIcon(QtGui.QIcon("avatars/user1.svg"))
    Temporary_Avatar.setIconSize(QtCore.QSize(int(scaled_app_width/20), int(scaled_app_height/17)))

    Sign_In_Title = QtWidgets.QLabel(Sign_In_Menu)
    Sign_In_Title.setObjectName("Sign_In_Title")
    Sign_In_Title.setGeometry(int(scaled_app_width/13.2), int(scaled_app_height/33), int(scaled_app_width/5), int(scaled_app_height/34))
    Sign_In_Title.setText("Sign-in")
    
    Username_Title = QtWidgets.QLabel(Sign_In_Menu)
    Username_Title.setObjectName("Username_Title")
    Username_Title.setGeometry(int(scaled_app_width/12.8), int(scaled_app_height/11.2), int(scaled_app_width/5), int(scaled_app_height/34))
    Username_Title.setText("Username")

    Username = QtWidgets.QLineEdit(Sign_In_Menu)
    Username.setObjectName("Username")
    Username.setGeometry(int(scaled_app_width/13.2), int(scaled_app_height/7.7), int(scaled_app_width/11.6), int(scaled_app_height/33))
    Username.setText("Hugo") # Prefilled for convenience
    Username.setEnabled(False)

    Password_Title = QtWidgets.QLabel(Sign_In_Menu)
    Password_Title.setObjectName("Password_Title")
    Password_Title.setGeometry(int(scaled_app_width/12.8), int(scaled_app_height/5.6), int(scaled_app_width/5), int(scaled_app_height/34))
    Password_Title.setText("Password")

    Password = QtWidgets.QLineEdit(Sign_In_Menu)
    Password.setObjectName("Password")
    Password.setGeometry(int(scaled_app_width/13.2), int(scaled_app_height/4.56), int(scaled_app_width/11.6), int(scaled_app_height/33))
    Password.setText("********") # FAKE: Does nothing, just for UI/UX conformity!
    Password.setEnabled(False)

    Sign_In_Button = QtWidgets.QPushButton(Sign_In_Menu)
    Sign_In_Button.setObjectName("Sign_In_Button")   
    Sign_In_Button.setGeometry(int(scaled_app_width/4.7), int(scaled_app_height/5.1), int(scaled_app_width/25), int(scaled_app_height/20))
    Sign_In_Button.setStyleSheet("background: transparent; border: none;")
    Sign_In_Button.setIcon(QtGui.QIcon(os.getcwd() + "/icons/enter_icon.svg"))
    Sign_In_Button.setIconSize(QtCore.QSize(int(scaled_app_width/20), int(scaled_app_height/17)))
    Sign_In_Button.setEnabled(False)
    Sign_In_Button.setCheckable(True)

    User_Connection_Status = QtWidgets.QLabel(Sign_In_Menu)
    User_Connection_Status.setObjectName("User_Connection_Status")
    User_Connection_Status.setGeometry(0, int(scaled_app_height/3.5), int(scaled_app_width/3.62), int(scaled_app_height/20))
    User_Connection_Status.setText("<html><head/><body><center>SIGNED-OUT       </center></body></html>")

# Extended Avatar Selection GUI
    Avatar_Selector_Widget = QtWidgets.QStackedWidget(Chat_Window)
    Avatar_Selector_Widget.setGeometry(int(scaled_app_width/16), int(scaled_app_height/2.8), int(scaled_app_width/5.12), int(scaled_app_height/3.3))
    Avatar_Selector_Widget.setObjectName("Avatar_Selector_Widget")
    Avatar_Selector_Widget.setVisible(False)

    Avatar_Selector_Page_1 = QtWidgets.QWidget()
    Avatar_Selector_Page_1.setObjectName("Avatar_Selector_Page_1")

    Avatar_Selector_Page_2 = QtWidgets.QWidget()
    Avatar_Selector_Page_2.setObjectName("Avatar_Selector_Page_2")

    Avatar_Selector_Page_3 = QtWidgets.QWidget()
    Avatar_Selector_Page_3.setObjectName("Avatar_Selector_Page_3")

    Avatar_Selector_Widget.addWidget(Avatar_Selector_Page_1)
    Avatar_Selector_Widget.addWidget(Avatar_Selector_Page_2)
    Avatar_Selector_Widget.addWidget(Avatar_Selector_Page_3)
    Avatar_Selector_Widget.setCurrentIndex(0)

    def Select_Avatar():
        """Allows selection of an avatar thorugh the avatar selection window."""
        selected_avatar = user.sender()
        User_Avatar.setIcon(QtGui.QIcon("avatars/" + selected_avatar.objectName() + ".svg"))
        Temporary_Avatar.setIcon(QtGui.QIcon("avatars/" + selected_avatar.objectName() + ".svg"))
        User_Avatar.setObjectName(selected_avatar.objectName())
        User_Avatar.toggle()
        Avatar_Selector_Widget.setVisible(False)
        
    def Open_Avatar_Selector():
        """Opens the avatar selection window."""
        if User_Avatar.isChecked():
            Avatar_Selector_Widget.setVisible(True)
        else:
            Avatar_Selector_Widget.setVisible(False)

    def Scroll_Avatar_Selector():
        """Allows flipping of pages in the avatar selection window."""
        current_index = Avatar_Selector_Widget.currentIndex()
        Avatar_Selector_Widget.setCurrentIndex(current_index + 1)

        if current_index == 2:
            Avatar_Selector_Widget.setCurrentIndex(0)

    for i in range(36): # Dynamic Avatar Creation
        j = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]

        if i < 4:
            page = Avatar_Selector_Page_1
            x = int(Avatar_Selector_Widget.width()/25) + (j[i]*int(Avatar_Selector_Widget.width()/4.166))
            y = int(Avatar_Selector_Widget.height()/14.5)

        if i >= 4:
            page = Avatar_Selector_Page_1
            x = int(Avatar_Selector_Widget.width()/25) + (j[i]*int(Avatar_Selector_Widget.width()/4.166))
            y = int(Avatar_Selector_Widget.height()/2.9)
        
        if i >= 8:
            page = Avatar_Selector_Page_1
            x = int(Avatar_Selector_Widget.width()/25) + (j[i]*int(Avatar_Selector_Widget.width()/4.166))
            y = int(Avatar_Selector_Widget.height()/1.611)

        if i >= 12:
            page = Avatar_Selector_Page_2
            x = int(Avatar_Selector_Widget.width()/25) + (j[i]*int(Avatar_Selector_Widget.width()/4.166))
            y = int(Avatar_Selector_Widget.height()/14.5)
        
        if i >= 16:
            page = Avatar_Selector_Page_2
            x = int(Avatar_Selector_Widget.width()/25) + (j[i]*int(Avatar_Selector_Widget.width()/4.166))
            y = int(Avatar_Selector_Widget.height()/2.9)

        if i >= 20:
            page = Avatar_Selector_Page_2
            x = int(Avatar_Selector_Widget.width()/25) + (j[i]*int(Avatar_Selector_Widget.width()/4.166))
            y = int(Avatar_Selector_Widget.height()/1.611)

        if i >= 24:
            page = Avatar_Selector_Page_3
            x = int(Avatar_Selector_Widget.width()/25) + (j[i]*int(Avatar_Selector_Widget.width()/4.166))
            y = int(Avatar_Selector_Widget.height()/14.5)

        if i >= 28:
            page = Avatar_Selector_Page_3
            x = int(Avatar_Selector_Widget.width()/25) + (j[i]*int(Avatar_Selector_Widget.width()/4.166))
            y = int(Avatar_Selector_Widget.height()/2.9)

        if i >= 32:
            page = Avatar_Selector_Page_3
            x = int(Avatar_Selector_Widget.width()/25) + (j[i]*int(Avatar_Selector_Widget.width()/4.166))
            y = int(Avatar_Selector_Widget.height()/1.611)

        user = QtWidgets.QPushButton(page)
        user.setObjectName("user" + str(i+1))
        user.setGeometry(x, y, int(Avatar_Selector_Widget.width()/5), int(Avatar_Selector_Widget.height()/5.9))
        user.setIcon(QtGui.QIcon("avatars/user" + str(i+1) +".svg"))
        user.setIconSize(QtCore.QSize(int(Avatar_Selector_Widget.width()/5), int(Avatar_Selector_Widget.height()/5.9)))
        user.setStyleSheet("background: transparent; border: none;")
        user.clicked.connect(Select_Avatar)
        
        if i == 8 or i == 20 or i == 32:
            Avatar_Selector_Next_Button = QtWidgets.QPushButton(page)
            Avatar_Selector_Next_Button.setObjectName("Avatar_Selector_Next_Button")
            Avatar_Selector_Next_Button.setGeometry(int(Avatar_Selector_Widget.width()/1.29), int(Avatar_Selector_Widget.height()/1.23), int(Avatar_Selector_Widget.width()/5), int(Avatar_Selector_Widget.height()/5.9)) 
            Avatar_Selector_Next_Button.setIcon(QtGui.QIcon(os.getcwd() + "/icons/next_icon.svg"))
            Avatar_Selector_Next_Button.setIconSize(QtCore.QSize(int(Avatar_Selector_Widget.width()/6.25), int(Avatar_Selector_Widget.height()/14.75)))
            Avatar_Selector_Next_Button.setStyleSheet("background: transparent; border: none;")
            Avatar_Selector_Next_Button.clicked.connect(Scroll_Avatar_Selector)

# Creates the 'chat settings' submenu:
    Chat_Settings_Icon = QtWidgets.QLabel(Chat_Settings_Menu)
    Chat_Settings_Icon.setObjectName("Chat_Settings_Icon")
    Chat_Settings_Icon.setGeometry(int(scaled_app_width/65), int(scaled_app_height/60), int(scaled_app_width/23), int(scaled_app_height/17))
    Chat_Settings_Icon.setPixmap(QtGui.QPixmap(os.getcwd() + "/icons/chat_icon.svg"))
    Chat_Settings_Icon.setScaledContents(True)

    Chat_Settings_Title = QtWidgets.QLabel(Chat_Settings_Menu)
    Chat_Settings_Title.setObjectName("Chat_Settings_Title")
    Chat_Settings_Title.setGeometry(int(scaled_app_width/13.2), int(scaled_app_height/33), int(scaled_app_width/5), int(scaled_app_height/34))
    Chat_Settings_Title.setText("Chat Settings")

    Chat_Theme_Title = QtWidgets.QLabel(Chat_Settings_Menu)
    Chat_Theme_Title.setObjectName("Chat_Theme_Title")
    Chat_Theme_Title.setGeometry(int(scaled_app_width/12.8), int(scaled_app_height/11.2), int(scaled_app_width/5), int(scaled_app_height/34))
    Chat_Theme_Title.setText("Theme")

    Chat_Theme = QtWidgets.QComboBox(Chat_Settings_Menu)
    Chat_Theme.setObjectName("Chat_Theme")
    Chat_Theme.setGeometry(int(scaled_app_width/13.2), int(scaled_app_height/7.7), int(scaled_app_width/11.6), int(scaled_app_height/33))
    Chat_Theme.addItems(["Default", "Blue", "Dark", "Light"])
    Chat_Theme.setEnabled(False)
    Chat_Theme.currentIndexChanged.connect(lambda: Theme(Chat_Theme.currentText()))

    Chat_Selector_Title = QtWidgets.QLabel(Chat_Settings_Menu)
    Chat_Selector_Title.setObjectName("Chat_Selector_Title")
    Chat_Selector_Title.setGeometry(int(scaled_app_width/12.8), int(scaled_app_height/5), int(scaled_app_width/5), int(scaled_app_height/34))
    Chat_Selector_Title.setText("Recipient")

    Chat_Selector = QtWidgets.QComboBox(Chat_Settings_Menu)
    Chat_Selector.setObjectName("Chat_Selector")
    Chat_Selector.setGeometry(int(scaled_app_width/13), int(scaled_app_height/4.15), int(scaled_app_width/11.6), int(scaled_app_height/33))
    Chat_Selector.addItem("ALL")
    Chat_Selector.setEnabled(False)

    Chat_Confirm_Button = QtWidgets.QPushButton(Chat_Settings_Menu)
    Chat_Confirm_Button.setObjectName("Chat_Confirm_Button") 
    Chat_Confirm_Button.setGeometry(int(scaled_app_width/4.7), int(scaled_app_height/4.4), int(scaled_app_width/25), int(scaled_app_height/20))
    Chat_Confirm_Button.setStyleSheet("background: transparent; border: none;")
    Chat_Confirm_Button.setIcon(QtGui.QIcon(os.getcwd() + "/icons/check_icon.svg"))
    Chat_Confirm_Button.setIconSize(QtCore.QSize(int(scaled_app_width/21), int(scaled_app_height/18)))
    Chat_Confirm_Button.setEnabled(False)
    Chat_Confirm_Button.setCheckable(True) # Turns the pushbutton into a toggle switch

# Overlays the OS provided drop down with a custom icon:
# NOTE: Please keep this code below the 'chat settings' code in order for it to be drawn above the OS drop down menu!
    Chat_Theme_Drop_Down_Background = QtWidgets.QLabel(Chat_Theme)
    Chat_Theme_Drop_Down_Background.setObjectName("Chat_Theme_Drop_Down_Background")
    Chat_Theme_Drop_Down_Background.setGeometry(int(Chat_Theme.x()/1.26), 0, int(Chat_Theme.width()/3), int(Chat_Theme.height()/1))

    Chat_Theme_Drop_Down = QtWidgets.QPushButton(Chat_Theme)
    Chat_Theme_Drop_Down.setObjectName("Chat_Theme_Drop_Down")
    Chat_Theme_Drop_Down.setGeometry(int(Chat_Theme.x()/1.26), 0, int(Chat_Theme.width()/3), int(Chat_Theme.height()/1.1))
    Chat_Theme_Drop_Down.setStyleSheet("background: transparent; border: none;")
    Chat_Theme_Drop_Down.setIcon(QtGui.QIcon(os.getcwd() + "/icons/drop_down_icon.svg"))
    Chat_Theme_Drop_Down.setIconSize(QtCore.QSize(int(scaled_app_width/25.6), int(scaled_app_height/20.7)))
    Chat_Theme_Drop_Down.setVisible(False)

    Chat_Selector_Drop_Down_Background = QtWidgets.QLabel(Chat_Selector)
    Chat_Selector_Drop_Down_Background.setObjectName("Chat_Selector_Drop_Down_Background")
    Chat_Selector_Drop_Down_Background.setGeometry(int(Chat_Selector.x()/1.3), 0, int(Chat_Selector.width()/3), int(Chat_Selector.height()/1))

    Chat_Selector_Drop_Down = QtWidgets.QPushButton(Chat_Selector)
    Chat_Selector_Drop_Down.setObjectName("Chat_Selector_Drop_Down")
    Chat_Selector_Drop_Down.setGeometry(int(Chat_Selector.x()/1.3), 0, int(Chat_Selector.width()/3), int(Chat_Selector.height()/1.1))
    Chat_Selector_Drop_Down.setStyleSheet("background: transparent; border: none;")
    Chat_Selector_Drop_Down.setIcon(QtGui.QIcon(os.getcwd() + "/icons/drop_down_icon.svg"))
    Chat_Selector_Drop_Down.setIconSize(QtCore.QSize(int(scaled_app_width/25.6), int(scaled_app_height/20.7)))
    Chat_Selector_Drop_Down.setVisible(False)

# Creates the chat log area:
    Chat_Log = QtWidgets.QListWidget(Chat_Window)
    Chat_Log.setGeometry(int(scaled_app_width/3.2), int(scaled_app_height/25.8), int(scaled_app_width/1.52), int(scaled_app_height/1.2))
    Chat_Log.setObjectName("Chat_Log")
    Chat_Log.setEnabled(False) # Keeps the area disabled from interactions before sign-in

# Creates the message field with attach button:
    Message_Field = QtWidgets.QLineEdit(Chat_Window)
    Message_Field.setObjectName("Message_Field")
    Message_Field.setGeometry(int(scaled_app_width/3.2), int(scaled_app_height), int(scaled_app_width/1.68), int(scaled_app_height/20.7))
    Message_Field.setText("Waiting for connection...")
    Message_Field.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(color=QtGui.QColor(0, 0, 0, 25), blurRadius=60, xOffset=int(scaled_app_width/128), yOffset=int(scaled_app_height/103.5)))
    Message_Field.setEnabled(False) # Keeps the field disabled from interactions before sign-in

    Message_Field_Animation = QtCore.QPropertyAnimation(Message_Field, b'pos')
    Message_Field_Animation.setStartValue(Message_Field.pos())
    Message_Field_Animation.setEndValue(QtCore.QPoint(int(scaled_app_width/3.2), int(scaled_app_height/1.1)))
    Message_Field_Animation.setDuration(150)
    
    Attach_Button = QtWidgets.QPushButton(Chat_Window)
    Attach_Button.setObjectName("Attach_Button")
    Attach_Button.setGeometry(int(scaled_app_width/1.075), int(scaled_app_height), int(scaled_app_width/25.09), int(scaled_app_height/20.29))
    Attach_Button.setStyleSheet("background: transparent; border: none;")
    Attach_Button.setIcon(QtGui.QIcon(os.getcwd() + "/icons/attach_icon.svg"))
    Attach_Button.setIconSize(QtCore.QSize(int(scaled_app_width/25.6), int(scaled_app_height/20.7)))
    Attach_Button.setEnabled(False) # Keeps the button disabled from interactions before sign-in

    Attach_Button_Animation = QtCore.QPropertyAnimation(Attach_Button, b'pos')
    Attach_Button_Animation.setStartValue(Attach_Button.pos())
    Attach_Button_Animation.setEndValue(QtCore.QPoint(int(scaled_app_width/1.075), int(scaled_app_height/1.1)))
    Attach_Button_Animation.setDuration(150)

    def Theme(theme_name):
        """Assigns the theme based on user selection."""
    # Default Theme
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
    
    # Blue Theme
        if theme_name == "Blue":
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

    # Dark Theme
        if theme_name == "Dark":
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

    # Light Theme
        if theme_name == "Light":
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

        Server_Settings_Menu.setStyleSheet("background: " + Main_Background_Color) # Color Line
        Server_Settings_Title.setStyleSheet("color: " + Main_Title_Color + "; font: " + scaled_font_size + "px;") # Color Line
        Host_Title.setStyleSheet("color: " + Main_Title_Color + "; font: " + scaled_font_size + "px;") # Color Line
        Host_Address.setStyleSheet("background: transparent; border: transparent; border-bottom: " + scaled_underline_size + " solid " + Main_Underline_Color + "; padding: 0 5px; color: " + Main_Text_Color + "; font: " + scaled_font_size + "px;") # Color Line
        Port_Title.setStyleSheet("color: " + Main_Title_Color + "; font: " + scaled_font_size + "px;") # Color Line
        Port_Number.setStyleSheet("background: transparent; border: transparent; border-bottom: " + scaled_underline_size + " solid " + Main_Underline_Color + "; padding: 0 5px; color: " + Main_Text_Alternate_Color + "; font: " + scaled_font_size + "px;") # Color Line

        if Server_Connection_Status.text() == "<html><head/><body><center>NOT CONNECTED</center></body></html>":
            Server_Connection_Status.setStyleSheet("color: " + Main_Status_Banner_Disconnected_Color + "; background: transparent; border-bottom: 2px solid " + Main_Status_Banner_Shadow_Color + "; font: " + scaled_font_size + "px;") # Color Line
        else:
            Server_Connection_Status.setStyleSheet("color: " + Main_Status_Banner_Connected_Color + "; background: transparent; border-bottom: 2px solid " + Main_Status_Banner_Shadow_Color + "; font: " + scaled_font_size + "px;") # Color Line
        
        Sign_In_Menu.setStyleSheet("background: " + Main_Background_Color) # Color Line
        Sign_In_Title.setStyleSheet("color: " + Main_Title_Color + "; font: " + scaled_font_size + "px;") # Color Line
        Username_Title.setStyleSheet("color: " + Main_Title_Color + "; font: " + scaled_font_size + "px;") # Color Line
        Username.setStyleSheet("background: transparent; border: transparent; border-bottom: " + scaled_underline_size + " solid " + Main_Underline_Color + "; padding: 0 5px; color: " + Main_Text_Color + "; font: " + scaled_font_size + "px;")
        Password_Title.setStyleSheet("color: " + Main_Title_Color + "; font: " + scaled_font_size + "px;") # Color Line
        Password.setStyleSheet("background: transparent; border: transparent; border-bottom: " + scaled_underline_size + " solid " + Main_Underline_Color + "; padding: 0 5px; color: " + Main_Text_Alternate_Color + "; font: " + scaled_font_size + "px;") # Color Line
        
        if User_Connection_Status.text() == "<html><head/><body><center>SIGNED-OUT       </center></body></html>":
            User_Connection_Status.setStyleSheet("color: " + Main_Status_Banner_Disconnected_Color + "; background: transparent; border-bottom: 2px solid " + Main_Status_Banner_Shadow_Color + "; font: " + scaled_font_size + "px;") # Color Line
        else:
            User_Connection_Status.setStyleSheet("color: " + Main_Status_Banner_Connected_Color + "; background: transparent; border-bottom: 2px solid " + Main_Status_Banner_Shadow_Color + "; font: " + scaled_font_size + "px;") # Color Line

        Avatar_Selector_Page_1.setStyleSheet("background: " + Main_Background_Color) # Color Line
        Avatar_Selector_Page_2.setStyleSheet("background: " + Main_Background_Color) # Color Line
        Avatar_Selector_Page_3.setStyleSheet("background: " + Main_Background_Color) # Color Line
        
        Chat_Settings_Menu.setStyleSheet("background: " + Main_Background_Color) # Color Line
        Chat_Settings_Title.setStyleSheet("color: " + Main_Title_Color + "; font: " + scaled_font_size + "px;") # Color Line
        Chat_Theme_Title.setStyleSheet("color: " + Main_Title_Color + "; font: " + scaled_font_size + "px;") # Color Line
        Chat_Theme.setStyleSheet("background: " + Main_Background_Color + "; border: none; border-bottom: " + scaled_underline_size + " solid " + Main_Underline_Color + "; padding: 0 5px; color: " + Main_Text_Color + "; font: " + scaled_font_size + "px;") # Color Line
        Chat_Selector_Title.setStyleSheet("color: " + Main_Title_Color + "; font: " + scaled_font_size + "px;") # Color Line
        Chat_Selector.setStyleSheet("background: " + Main_Background_Color + "; border: none; border-bottom: " + scaled_underline_size + " solid " + Main_Underline_Color + "; padding: 0 5px; color: " + Main_Text_Alternate_Color + "; font: " + scaled_font_size + "px;") # Color Line
        Chat_Theme_Drop_Down_Background.setStyleSheet("background: " + Main_Background_Color) # Color Line
        Chat_Selector_Drop_Down_Background.setStyleSheet("background: " + Main_Background_Color) # Color Line
        
        Chat_Window.setStyleSheet("background-color: " + Main_Chat_Log_Background_Color)
        Chat_Log.setStyleSheet("border: none; color: " + Main_Chat_Log_Text_Color + "; background-color: " + Main_Chat_Log_Background_Color + "; padding: 10px 20px; font: " + scaled_font_size + "px;") # Color Line
        Message_Field.setStyleSheet("border: 0px solid #000000; color: " + Main_Message_Field_Text_Color + "; background-color: " + Main_Message_Field_Background_Color + "; border-radius: " + scaled_border_radius + "px; padding: 0 15px; font: " + scaled_font_size + "px;") # Color Line

    Theme("Default") # Starts the app in default theme

# Alignment grid for UI/UX purposes:
    # y = 0
    # for i in range(46):
    #     x_line = QtWidgets.QFrame(Chat_Window)
    #     x_line.setObjectName("x_line")
    #     x_line.setGeometry(0, y, scaled_app_width, 1)
    #     x_line.setFrameShape(QtWidgets.QFrame.HLine)
    #     x_line.setFrameShadow(QtWidgets.QFrame.Sunken)
    #     x_line.setStyleSheet("background-color:red")
    #     y = y + 23

    # x = 0
    # for i in range(41):
    #     y_line = QtWidgets.QFrame(Chat_Window)
    #     y_line.setObjectName("y_line")
    #     y_line.setGeometry(x, 0, 1, scaled_app_height)
    #     y_line.setFrameShape(QtWidgets.QFrame.HLine)
    #     y_line.setFrameShadow(QtWidgets.QFrame.Sunken)
    #     y_line.setStyleSheet("background-color:red")
    #     x = x + 32

# Defines the logic for server connection and disconnection after 'Server_Button' press:
    def Server_Connection():
        """Connects to the server with provided hostname and port."""
        if Server_Button.isChecked():
            HOST = Host_Address.text()
            PORT = int(Port_Number.text())

            client_socket.connect((HOST, PORT))
            receive_thread = Thread(target=Receive) # Could have used QThread but treating server.py as an API, and since it uses Thread, here we got the same!
            receive_thread.start()

            Server_Button.setIcon(QtGui.QIcon(os.getcwd() + "/icons/exit_icon.svg"))
            Server_Connection_Status.setText("<html><head/><body><center>CONNECTED     </center></body></html>")
            Theme(Chat_Theme.currentText())

            Host_Address.setEnabled(False)
            Port_Number.setEnabled(False)

            Temporary_Avatar.setVisible(False)
            Username.setEnabled(True)
            Sign_In_Button.setEnabled(True)

            Message_Field.setText("Waiting for sign-in...")

        else:
            Server_Button.setIcon(QtGui.QIcon(os.getcwd() + "/icons/enter_icon.svg"))
            Server_Connection_Status.setText("<html><head/><body><center>NOT CONNECTED</center></body></html>")
            Theme(Chat_Theme.currentText())

            Host_Address.setEnabled(True)
            Port_Number.setEnabled(True)

            Temporary_Avatar.setVisible(True)
            Username.setEnabled(False)
            Sign_In_Button.setEnabled(False)

            Message_Field.setText("Dissconnected! Good Bye...")

            client_socket.sendall(bytes("{QUIT}", "utf8")) # Actual disconnect/quit logic
            
# Defines the logic for user client sign-in and disconnection after 'Sign_In_Button' press:
    def Sign_In():
        """Registers the provided username with the server."""
        if Sign_In_Button.isChecked():
            client_socket.sendall(bytes("{REGISTER}" + Username.text(), "utf8"))
            client_socket.sendall(bytes("{ALL}#_*_#" + User_Avatar.objectName(), "utf8"))
            Server_Button.setEnabled(False)

            Sign_In_Button.setIcon(QtGui.QIcon(os.getcwd() + "/icons/exit_icon.svg"))
            User_Connection_Status.setText("<html><head/><body><center>SIGNED-IN        </center></body></html>")
            Theme(Chat_Theme.currentText())
            
            Username.setEnabled(False)
            Temporary_Avatar.setVisible(True)

            Chat_Theme.setEnabled(True)
            Chat_Theme_Drop_Down.setVisible(True)
            Chat_Selector.setEnabled(True)
            Chat_Selector.setItemText(0,"ALL")
            Chat_Selector_Drop_Down.setVisible(True)
            Chat_Confirm_Button.setEnabled(True)

            Message_Field.setText("Select a user to start chatting...")
            Chat_Log.setEnabled(True)

        else:
            Server_Button.setEnabled(True)

            Sign_In_Button.setIcon(QtGui.QIcon(os.getcwd() + "/icons/enter_icon.svg"))
            User_Connection_Status.setText("<html><head/><body><center>SIGNED-OUT       </center></body></html>")
            Theme(Chat_Theme.currentText())

            Username.setEnabled(True)
            Temporary_Avatar.setVisible(False)

            Chat_Theme.setEnabled(False)
            Chat_Theme_Drop_Down.setVisible(False)
            Chat_Selector.setEnabled(False)
            Chat_Selector_Drop_Down.setVisible(False)
            Chat_Confirm_Button.setEnabled(False)

            Message_Field.setText("Signed Out!...")
            Chat_Log.setEnabled(False)

# Defines the logic for continous message receiving and adding to the chat log:
    def Receive():
        """Continously recieves the messages sent by different users."""
        while True:
            try:
                msg = client_socket.recv(2048).decode("utf8")
                #Chat_Log.addItem(msg) # Crazy makes the program quit properly!!!

                if not (msg.startswith("{MSG}") or "{CLIENTS}" in msg):
                    if "#_*_#" in msg:
                        full_message = msg.replace("#_*_#", "#")
                        text_part = full_message.split("#")[0]
                        avatar_name = full_message.split("#")[1]
                        
                        final_formatted_message = QtWidgets.QListWidgetItem(text_part + "\n")
                        final_formatted_message.setIcon(QtGui.QIcon("avatars/" + avatar_name + ".svg"))
                        Chat_Log.setIconSize(QtCore.QSize(int(scaled_app_width/20), int(scaled_app_height/17)))
                        Chat_Log.addItem(final_formatted_message)             

                if msg.startswith("{MSG}"):
                    if "#_*_#" in msg:
                        msg = msg.replace("{MSG}", "")
                        full_message = msg.replace("#_*_#", "#")
                        text_part = full_message.split("#")[0]
                        avatar_name = full_message.split("#")[1]
                        
                        final_formatted_message = QtWidgets.QListWidgetItem(text_part + "\n")
                        final_formatted_message.setIcon(QtGui.QIcon("avatars/" + avatar_name + ".svg"))
                        Chat_Log.setIconSize(QtCore.QSize(int(scaled_app_width/20), int(scaled_app_height/17)))
                        Chat_Log.addItem(final_formatted_message)

                    else:
                        msg = msg.replace("{MSG}", "")
                        Chat_Log.addItem(msg)

                # Side comments are provided for a logic walkthrough in a scenario where Hugo and Sabneet are chatting:
                if "{CLIENTS}" in msg: # {CLIENTS}Hugo|Sabneet{MSG}Sabneet: #_*_#user2
                    if "#_*_#" in msg:
                        client_detail_message = msg.replace("{CLIENTS}", "@") # Blah...Blah...@Hugo|Sabneet{MSG}Sabneet: #_*_#user2
                        client_detail_message = client_detail_message.split("@")[1] # [Hugo|Sabneet{MSG}Sabneet: #_*_#user2]

                        client_detail_message = client_detail_message.replace("{MSG}",">") # Hugo|Sabneet>Sabneet: #_*_#user2
                        client_list = client_detail_message.split(">")[0] # [(Hugo|Sabneet)]

                        if "|" in client_list:
                            client_list = client_list.split("|") # [(Hugo),(Sabneet)]
                        else:
                            client_list = [] # In case, only Hugo
                        
                        Chat_Selector.clear()
                        Chat_Selector.addItem("ALL")
                        Chat_Selector.setCurrentIndex(0)

                        for i in range(len(client_list)):
                            if not Username.text() in client_list[i]:

                                chat_avatar = client_detail_message.split(">")[1] # [Sabneet:#_*_#user2]
                                client_detail_message = client_detail_message.replace("#_*_#","#")
                                chat_avatar = client_detail_message.split("#")[1] # [user2]

                                Chat_Selector.addItem(client_list[i])

                    else: # {CLIENTS}Hugo|Sabneet
                        client_list = msg.replace("{CLIENTS}", "") # Hugo|Sabneet

                        if "|" in client_list:
                            client_list = client_list.split("|") # [(Hugo),(Sabneet)]
                        else:
                            client_list = [client_list] # In case, only Hugo

                        client_list.insert(0,"ALL")
                        for i in range(Chat_Selector.count()):
                            if not Chat_Selector.itemText(i) in client_list:
                                Chat_Selector.removeItem(i)
                        Chat_Selector.setCurrentIndex(0)

            except OSError:
                break

# Defines the logic to send messages based on the selected 'Chat_With' user while retaining compatibility with textual '{QUIT}' command:
    def Send():
        """Sends the message and user avatar to the server."""
        if "{QUIT}" in Message_Field.text():
            client_socket.sendall(bytes("{QUIT}", "utf8"))
            
        else:
            msg = "{" + Chat_Selector.currentText() + "}\n" + Message_Field.text() + "#_*_#" + User_Avatar.objectName() #+ "\n"
            Message_Field.setText("")
            Message_Field.setFocus()
            client_socket.sendall(bytes(msg, "utf8"))
            
# Allows the custom drop down menu to mimic the one provided by the OS:
    def Better_Drop_Down(whom):
        """Provides a cleaner drop down experience"""
        if whom == 0:
            Chat_Theme_Drop_Down.parent().showPopup()
        if whom == 1:
            Chat_Selector_Drop_Down.parent().showPopup()

# Defines the logic for chat recipient confirmation and revocation after 'Chat_Confirm_Button' press:
    def Chat_Target():
        """Provides the option to select the recipient of one's messages."""
        if Chat_Confirm_Button.isChecked():
            Chat_Confirm_Button.setIcon(QtGui.QIcon(QtGui.QPixmap(os.getcwd() + "/icons/cancel_icon.svg")))
            Chat_Theme.setEnabled(False)
            Chat_Theme_Drop_Down.setVisible(False)
            Chat_Selector.setEnabled(False)
            Chat_Selector_Drop_Down.setVisible(False)

            Sign_In_Button.setEnabled(False)

            Message_Field.setEnabled(True)
            Message_Field.setText("")
            Message_Field.setFocus()
            Chat_Log.setEnabled(True)

            Attach_Button.setEnabled(True)
            
        else:
            Chat_Confirm_Button.setIcon(QtGui.QIcon(QtGui.QPixmap(os.getcwd() + "/icons/check_icon.svg")))
            Chat_Theme.setEnabled(True)
            Chat_Theme_Drop_Down.setVisible(True)
            Chat_Selector.setEnabled(True)
            Chat_Selector_Drop_Down.setVisible(True)

            Sign_In_Button.setEnabled(True)

            Message_Field.setEnabled(False)
            Message_Field.setText("Select a user to start chatting...")
            Chat_Log.setEnabled(False)

            Attach_Button.setEnabled(False)

    def Attach_Picture():
        image = QtWidgets.QFileDialog.getOpenFileName(Chat_Window, 'Attach an image', os.getcwd(), "Image files (*.jpg *.png *.gif *.svg)")

        attached_image = QtWidgets.QListWidgetItem("\n\n\n\n")
        attached_image.setIcon(QtGui.QIcon(image[0]))
        Chat_Log.setIconSize(QtCore.QSize(int(scaled_app_width/20), int(scaled_app_height/17)))
        Chat_Log.addItem(attached_image) 

# Assigns each pushbutton their respective function:
    Server_Button.clicked.connect(Server_Connection)
    User_Avatar.clicked.connect(Open_Avatar_Selector)
    Sign_In_Button.clicked.connect(Sign_In)
    Chat_Theme_Drop_Down.clicked.connect(lambda: Better_Drop_Down(0))
    Chat_Selector_Drop_Down.clicked.connect(lambda: Better_Drop_Down(1))
    Chat_Confirm_Button.clicked.connect(Chat_Target)
    Message_Field.returnPressed.connect(Send)
    Attach_Button.clicked.connect(Attach_Picture)

# Draws the entire GUI:
    Chat_Window.show()
    Server_Settings_Menu_Animation.start()
    Sign_In_Menu_Animation.start()
    Chat_Settings_Menu_Animation.start()
    Message_Field_Animation.start()
    Attach_Button_Animation.start()
    sys.exit(app.exec_())

if __name__ == '__main__':
   Window()