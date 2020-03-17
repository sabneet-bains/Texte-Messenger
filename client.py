import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork

def Run_Client():
# Intialize the udp socket and the chat window:
    SOCKET = QtNetwork.QUdpSocket()
    app = QtWidgets.QApplication(sys.argv)

# Custom High DPI Scalling as the builtin Qt HDPi is not working well:
    Screen_Size = app.primaryScreen().availableGeometry()
    Scaled_App_Width = int(Screen_Size.width()/3)
    Scaled_App_Height = int(Screen_Size.height()/2)
    Scaled_Border_Radius = str(int(Screen_Size.height()/86.4))
    Scaled_Font_Size = str(int(Screen_Size.height()/100))
    Scaled_Underline_Size = str(int(Screen_Size.height()/720))

    Chat_Window = QtWidgets.QDialog()
    Chat_Window.setObjectName("Chat_Window")
    Chat_Window.setGeometry(int(Screen_Size.width()/2)-int(Scaled_App_Width/2),int(Screen_Size.height()/2)-int(Scaled_App_Height/2),Scaled_App_Width,Scaled_App_Height)
    Chat_Window.setWindowTitle("  texte") # Chosen Brand Name for the Client
    Chat_Window.setWindowIcon(QtGui.QIcon(f"{os.getcwd()}/icons/texte_icon.svg"))

# Creates the left menu bar:
    Chat_Settings_Menu = QtWidgets.QFrame(Chat_Window)
    Chat_Settings_Menu.setObjectName("Chat_Settings_Menu")
    Chat_Settings_Menu.setGeometry(-int(Scaled_App_Width/30), int(2*Scaled_App_Height/3), int(Scaled_App_Width/3.62), int(Scaled_App_Height/2.9))
    Chat_Settings_Menu.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(color=QtGui.QColor(0, 0, 0, 25), blurRadius=60, xOffset=int(Scaled_App_Width/128), yOffset=int(Scaled_App_Height/103.5)))

    Chat_Settings_Menu_Animation = QtCore.QPropertyAnimation(Chat_Settings_Menu, b'pos')
    Chat_Settings_Menu_Animation.setStartValue(Chat_Settings_Menu.pos())
    Chat_Settings_Menu_Animation.setEndValue(QtCore.QPoint(0, int(2*Scaled_App_Height/3)))
    Chat_Settings_Menu_Animation.setDuration(150)

    Sign_In_Menu = QtWidgets.QFrame(Chat_Window)
    Sign_In_Menu.setObjectName("Sign_In_Menu")
    Sign_In_Menu.setGeometry(-int(Scaled_App_Width/20), int(Scaled_App_Height/3), int(Scaled_App_Width/3.62), int(Scaled_App_Height/3))
    Sign_In_Menu.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(color=QtGui.QColor(0, 0, 0, 25), blurRadius=60, xOffset=int(Scaled_App_Width/128), yOffset=int(Scaled_App_Height/103.5)))

    Sign_In_Menu_Animation = QtCore.QPropertyAnimation(Sign_In_Menu, b'pos')
    Sign_In_Menu_Animation.setStartValue(Sign_In_Menu.pos())
    Sign_In_Menu_Animation.setEndValue(QtCore.QPoint(0, int(Scaled_App_Height/3)))
    Sign_In_Menu_Animation.setDuration(150)

    Server_Settings_Menu = QtWidgets.QFrame(Chat_Window)
    Server_Settings_Menu.setObjectName("Server_Settings_Menu")
    Server_Settings_Menu.setGeometry(-int(Scaled_App_Width/10), 0, int(Scaled_App_Width/3.62), int(Scaled_App_Height/3))
    Server_Settings_Menu.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(color=QtGui.QColor(0, 0, 0, 25), blurRadius=60, xOffset=int(Scaled_App_Width/128), yOffset=int(Scaled_App_Height/103.5)))
    
    Server_Settings_Menu_Animation = QtCore.QPropertyAnimation(Server_Settings_Menu, b'pos')
    Server_Settings_Menu_Animation.setStartValue(Server_Settings_Menu.pos())
    Server_Settings_Menu_Animation.setEndValue(QtCore.QPoint(0, 0))
    Server_Settings_Menu_Animation.setDuration(150)

# Creates the 'server settings' submenu:
    Server_Settings_Icon = QtWidgets.QPushButton(Server_Settings_Menu)
    Server_Settings_Icon.setObjectName("Server_Settings_Icon")
    Server_Settings_Icon.setGeometry(int(Scaled_App_Width/60), int(Scaled_App_Height/45), int(Scaled_App_Width/28), int(Scaled_App_Height/22))
    Server_Settings_Icon.setStyleSheet("background: transparent; border: none;")
    Server_Settings_Icon.setIcon(QtGui.QIcon(f"{os.getcwd()}/icons/server_icon.svg"))
    Server_Settings_Icon.setIconSize(QtCore.QSize(int(Scaled_App_Width/28), int(Scaled_App_Height/24)))
    Server_Settings_Icon.setCheckable(True) # Turns the pushbutton into a toggle switch
    Server_Settings_Icon.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(color=QtGui.QColor(0, 0, 0, 100), blurRadius=30, xOffset=int(Scaled_App_Width/350), yOffset=int(Scaled_App_Height/350)))
    Server_Settings_Icon.raise_()

    Server_Settings_Title = QtWidgets.QLabel(Server_Settings_Menu)
    Server_Settings_Title.setObjectName("Server_Settings_Title")
    Server_Settings_Title.setGeometry(int(Scaled_App_Width/13.2), int(Scaled_App_Height/33), int(Scaled_App_Width/5), int(Scaled_App_Height/34))
    Server_Settings_Title.setText("Server Settings")

    Host_Title = QtWidgets.QLabel(Server_Settings_Menu)
    Host_Title.setObjectName("Host_Title")
    Host_Title.setGeometry(int(Scaled_App_Width/12.8), int(Scaled_App_Height/11.2), int(Scaled_App_Width/5), int(Scaled_App_Height/34))
    Host_Title.setText("Hostname")

    Host_Address = QtWidgets.QLineEdit(Server_Settings_Menu)
    Host_Address.setObjectName("Host_Address")
    Host_Address.setGeometry(int(Scaled_App_Width/13.2), int(Scaled_App_Height/7.7), int(Scaled_App_Width/11.6), int(Scaled_App_Height/33))
    Host_Address.setText("127.0.0.1") # Prefilled default as also provided in server.py

    Port_Title = QtWidgets.QLabel(Server_Settings_Menu)
    Port_Title.setObjectName("Port_Title")
    Port_Title.setGeometry(int(Scaled_App_Width/12.8), int(Scaled_App_Height/5.6), int(Scaled_App_Width/5), int(Scaled_App_Height/34))
    Port_Title.setText("Port #")

    Port_Number = QtWidgets.QLineEdit(Server_Settings_Menu)
    Port_Number.setObjectName("Port_Number")
    Port_Number.setGeometry(int(Scaled_App_Width/13.2), int(Scaled_App_Height/4.56), int(Scaled_App_Width/11.6), int(Scaled_App_Height/33))
    Port_Number.setText("33002") # Prefilled default as also provided in server.py
    
    Server_Button = QtWidgets.QPushButton(Server_Settings_Menu)
    Server_Button.setObjectName("Server_Button")   
    Server_Button.setGeometry(int(Scaled_App_Width/4.7), int(Scaled_App_Height/5.1), int(Scaled_App_Width/25), int(Scaled_App_Height/20))
    Server_Button.setStyleSheet("background: transparent; border: none;")
    Server_Button.setIcon(QtGui.QIcon(f"{os.getcwd()}/icons/enter_icon.svg"))
    Server_Button.setIconSize(QtCore.QSize(int(Scaled_App_Width/20), int(Scaled_App_Height/17)))
    Server_Button.setCheckable(True) # Turns the pushbutton into a toggle switch
    Server_Button.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(color=QtGui.QColor(0, 0, 0, 100), blurRadius=30, xOffset=int(Scaled_App_Width/300), yOffset=int(Scaled_App_Height/350)))

    Server_Connection_Status = QtWidgets.QLabel(Server_Settings_Menu)
    Server_Connection_Status.setObjectName("Server_Connection_Status")
    Server_Connection_Status.setGeometry(0, int(Scaled_App_Height/3.5), int(Scaled_App_Width/3.62), int(Scaled_App_Height/20))
    Server_Connection_Status.setText("<html><head/><body><center>NOT CONNECTED</center></body></html>")

# Creates the 'sign-in' submenu with FAKE password (NO AUTH):
    User_Avatar = QtWidgets.QPushButton(Sign_In_Menu)
    User_Avatar.setObjectName("user1") 
    User_Avatar.setGeometry(int(Scaled_App_Width/65), int(Scaled_App_Height/48), int(Scaled_App_Width/20), int(Scaled_App_Height/15))
    User_Avatar.setStyleSheet("background: transparent; border: none;")
    User_Avatar.setIcon(QtGui.QIcon(f"{os.getcwd()}/avatars/user1.svg"))
    User_Avatar.setIconSize(QtCore.QSize(int(Scaled_App_Width/20), int(Scaled_App_Height/17)))
    User_Avatar.setCheckable(True) # Turns the pushbutton into a toggle switch
    User_Avatar.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(color=QtGui.QColor(0, 0, 0, 100), blurRadius=30, xOffset=int(Scaled_App_Width/350), yOffset=int(Scaled_App_Height/350)))
    User_Avatar.setVisible(False)
    User_Avatar.raise_()
    
    Temporary_Avatar = QtWidgets.QPushButton(Sign_In_Menu)
    Temporary_Avatar.setObjectName("Temporary_Avatar")
    Temporary_Avatar.setGeometry(int(Scaled_App_Width/65), int(Scaled_App_Height/48), int(Scaled_App_Width/20), int(Scaled_App_Height/15))
    Temporary_Avatar.setStyleSheet("background: transparent; border: none;")
    Temporary_Avatar.setIcon(QtGui.QIcon(f"{os.getcwd()}/avatars/user1.svg"))
    Temporary_Avatar.setIconSize(QtCore.QSize(int(Scaled_App_Width/20), int(Scaled_App_Height/17)))
    Temporary_Avatar.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(color=QtGui.QColor(0, 0, 0, 100), blurRadius=30, xOffset=int(Scaled_App_Width/350), yOffset=int(Scaled_App_Height/350)))

    Sign_In_Title = QtWidgets.QLabel(Sign_In_Menu)
    Sign_In_Title.setObjectName("Sign_In_Title")
    Sign_In_Title.setGeometry(int(Scaled_App_Width/13.2), int(Scaled_App_Height/33), int(Scaled_App_Width/5), int(Scaled_App_Height/34))
    Sign_In_Title.setText("Sign-in")
    
    Username_Title = QtWidgets.QLabel(Sign_In_Menu)
    Username_Title.setObjectName("Username_Title")
    Username_Title.setGeometry(int(Scaled_App_Width/12.8), int(Scaled_App_Height/11.2), int(Scaled_App_Width/5), int(Scaled_App_Height/34))
    Username_Title.setText("Username")

    Username = QtWidgets.QLineEdit(Sign_In_Menu)
    Username.setObjectName("Username")
    Username.setGeometry(int(Scaled_App_Width/13.2), int(Scaled_App_Height/7.7), int(Scaled_App_Width/11.6), int(Scaled_App_Height/33))
    Username.setText("Hugo") # Prefilled for convenience
    Username.setEnabled(False)

    Password_Title = QtWidgets.QLabel(Sign_In_Menu)
    Password_Title.setObjectName("Password_Title")
    Password_Title.setGeometry(int(Scaled_App_Width/12.8), int(Scaled_App_Height/5.6), int(Scaled_App_Width/5), int(Scaled_App_Height/34))
    Password_Title.setText("Password")

    Password = QtWidgets.QLineEdit(Sign_In_Menu)
    Password.setObjectName("Password")
    Password.setGeometry(int(Scaled_App_Width/13.2), int(Scaled_App_Height/4.56), int(Scaled_App_Width/11.6), int(Scaled_App_Height/33))
    Password.setText("********") # FAKE: Does nothing, just for UI/UX conformity!
    Password.setEnabled(False)

    Sign_In_Button = QtWidgets.QPushButton(Sign_In_Menu)
    Sign_In_Button.setObjectName("Sign_In_Button")   
    Sign_In_Button.setGeometry(int(Scaled_App_Width/4.7), int(Scaled_App_Height/5.1), int(Scaled_App_Width/25), int(Scaled_App_Height/20))
    Sign_In_Button.setStyleSheet("background: transparent; border: none;")
    Sign_In_Button.setIcon(QtGui.QIcon(f"{os.getcwd()}/icons/enter_icon.svg"))
    Sign_In_Button.setIconSize(QtCore.QSize(int(Scaled_App_Width/20), int(Scaled_App_Height/17)))
    Sign_In_Button.setEnabled(False)
    Sign_In_Button.setCheckable(True)
    Sign_In_Button.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(color=QtGui.QColor(0, 0, 0, 100), blurRadius=30, xOffset=int(Scaled_App_Width/300), yOffset=int(Scaled_App_Height/350)))

    User_Connection_Status = QtWidgets.QLabel(Sign_In_Menu)
    User_Connection_Status.setObjectName("User_Connection_Status")
    User_Connection_Status.setGeometry(0, int(Scaled_App_Height/3.5), int(Scaled_App_Width/3.62), int(Scaled_App_Height/20))
    User_Connection_Status.setText("<html><head/><body><center>SIGNED-OUT       </center></body></html>")

# Extended Avatar Selection GUI
    Avatar_Selector_Widget = QtWidgets.QStackedWidget(Chat_Window)
    Avatar_Selector_Widget.setGeometry(int(Scaled_App_Width/25), int(Scaled_App_Height/2.78), int(Scaled_App_Width/5.12), int(Scaled_App_Height/3.4))
    Avatar_Selector_Widget.setObjectName("Avatar_Selector_Widget")
    Avatar_Selector_Widget.setVisible(False)
    Avatar_Selector_Widget.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(color=QtGui.QColor(0, 0, 0, 50), blurRadius=20, xOffset=int(Scaled_App_Width/300), yOffset=int(Scaled_App_Height/300)))

    Avatar_Selector_Widget_Opening_Animation = QtCore.QPropertyAnimation(Avatar_Selector_Widget, b'pos')
    Avatar_Selector_Widget_Opening_Animation.setStartValue(Avatar_Selector_Widget.pos())
    Avatar_Selector_Widget_Opening_Animation.setEndValue(QtCore.QPoint(int(Scaled_App_Width/14.7), int(Scaled_App_Height/2.78)))
    Avatar_Selector_Widget_Opening_Animation.setDuration(20)

    Avatar_Selector_Widget_Closing_Animation = QtCore.QPropertyAnimation(Avatar_Selector_Widget, b'pos')
    Avatar_Selector_Widget_Closing_Animation.setStartValue(Avatar_Selector_Widget.pos())
    Avatar_Selector_Widget_Closing_Animation.setEndValue(QtCore.QPoint(int(Scaled_App_Width/25), int(Scaled_App_Height/2.78)))
    Avatar_Selector_Widget_Closing_Animation.setDuration(25)

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
        Selected_Avatar = User.sender()
        User_Avatar.setIcon(QtGui.QIcon(f"{os.getcwd()}/avatars/{Selected_Avatar.objectName()}.svg"))
        Temporary_Avatar.setIcon(QtGui.QIcon(f"{os.getcwd()}/avatars/{Selected_Avatar.objectName()}.svg"))
        User_Avatar.setObjectName(Selected_Avatar.objectName())
        User_Avatar.toggle()
        Avatar_Selector_Widget_Closing_Animation.start()

        if Avatar_Selector_Widget.x() == int(Scaled_App_Width/25):
            Avatar_Selector_Widget.setVisible(False)
        
    def Open_Avatar_Selector():
        """Opens the avatar selection window."""
        if User_Avatar.isChecked():
            Avatar_Selector_Widget.setVisible(True)
            Avatar_Selector_Widget_Opening_Animation.start()

        else:
            Avatar_Selector_Widget_Closing_Animation.start()

            if Avatar_Selector_Widget.x() == int(Scaled_App_Width/25):
                Avatar_Selector_Widget.setVisible(False)
            
    def Scroll_Avatar_Selector():
        """Allows flipping of pages in the avatar selection window."""
        Current_Index = Avatar_Selector_Widget.currentIndex()
        Avatar_Selector_Widget.setCurrentIndex(Current_Index + 1)

        if Current_Index == 2:
            Avatar_Selector_Widget.setCurrentIndex(0)

    for i in range(36): # Dynamic Avatar Creation
        j = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]

        if i < 4:
            Page = Avatar_Selector_Page_1
            x = int(Avatar_Selector_Widget.width()/25) + (j[i]*int(Avatar_Selector_Widget.width()/4.166))
            y = int(Avatar_Selector_Widget.height()/14.5)

        if i >= 4:
            Page = Avatar_Selector_Page_1
            x = int(Avatar_Selector_Widget.width()/25) + (j[i]*int(Avatar_Selector_Widget.width()/4.166))
            y = int(Avatar_Selector_Widget.height()/2.9)
        
        if i >= 8:
            Page = Avatar_Selector_Page_1
            x = int(Avatar_Selector_Widget.width()/25) + (j[i]*int(Avatar_Selector_Widget.width()/4.166))
            y = int(Avatar_Selector_Widget.height()/1.611)

        if i >= 12:
            Page = Avatar_Selector_Page_2
            x = int(Avatar_Selector_Widget.width()/25) + (j[i]*int(Avatar_Selector_Widget.width()/4.166))
            y = int(Avatar_Selector_Widget.height()/14.5)
        
        if i >= 16:
            Page = Avatar_Selector_Page_2
            x = int(Avatar_Selector_Widget.width()/25) + (j[i]*int(Avatar_Selector_Widget.width()/4.166))
            y = int(Avatar_Selector_Widget.height()/2.9)

        if i >= 20:
            Page = Avatar_Selector_Page_2
            x = int(Avatar_Selector_Widget.width()/25) + (j[i]*int(Avatar_Selector_Widget.width()/4.166))
            y = int(Avatar_Selector_Widget.height()/1.611)

        if i >= 24:
            Page = Avatar_Selector_Page_3
            x = int(Avatar_Selector_Widget.width()/25) + (j[i]*int(Avatar_Selector_Widget.width()/4.166))
            y = int(Avatar_Selector_Widget.height()/14.5)

        if i >= 28:
            Page = Avatar_Selector_Page_3
            x = int(Avatar_Selector_Widget.width()/25) + (j[i]*int(Avatar_Selector_Widget.width()/4.166))
            y = int(Avatar_Selector_Widget.height()/2.9)

        if i >= 32:
            Page = Avatar_Selector_Page_3
            x = int(Avatar_Selector_Widget.width()/25) + (j[i]*int(Avatar_Selector_Widget.width()/4.166))
            y = int(Avatar_Selector_Widget.height()/1.611)

        User = QtWidgets.QPushButton(Page)
        User.setObjectName(f"User{str(i + 1)}")
        User.setGeometry(x, y, int(Avatar_Selector_Widget.width()/5), int(Avatar_Selector_Widget.height()/5.9))
        User.setStyleSheet("background: transparent; border: none;")
        User.setIcon(QtGui.QIcon(f"{os.getcwd()}/avatars/User{str(i + 1)}.svg"))
        User.setIconSize(QtCore.QSize(int(Avatar_Selector_Widget.width()/5), int(Avatar_Selector_Widget.height()/5.9)))
        User.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(color=QtGui.QColor(0, 0, 0, 100), blurRadius=30, xOffset=int(Scaled_App_Width/350), yOffset=int(Scaled_App_Height/350)))
        User.clicked.connect(Select_Avatar)
        
        if i == 8 or i == 20 or i == 32:
            Avatar_Selector_Next_Button = QtWidgets.QPushButton(Page)
            Avatar_Selector_Next_Button.setObjectName("Avatar_Selector_Next_Button")
            Avatar_Selector_Next_Button.setGeometry(int(Avatar_Selector_Widget.width()/1.29), int(Avatar_Selector_Widget.height()/1.23), int(Avatar_Selector_Widget.width()/5), int(Avatar_Selector_Widget.height()/5.9)) 
            Avatar_Selector_Next_Button.setStyleSheet("background: transparent; border: none;")
            Avatar_Selector_Next_Button.setIcon(QtGui.QIcon(f"{os.getcwd()}/icons/next_icon.svg"))
            Avatar_Selector_Next_Button.setIconSize(QtCore.QSize(int(Avatar_Selector_Widget.width()/6.25), int(Avatar_Selector_Widget.height()/14.75)))
            Avatar_Selector_Next_Button.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(color=QtGui.QColor(0, 0, 0, 100), blurRadius=10, xOffset=int(Scaled_App_Width/300), yOffset=int(Scaled_App_Height/350)))
            Avatar_Selector_Next_Button.clicked.connect(Scroll_Avatar_Selector)

# Creates the 'chat settings' submenu:
    Chat_Settings_Icon = QtWidgets.QPushButton(Chat_Settings_Menu)
    Chat_Settings_Icon.setObjectName("Chat_Settings_Icon")
    Chat_Settings_Icon.setGeometry(int(Scaled_App_Width/65), int(Scaled_App_Height/60), int(Scaled_App_Width/23), int(Scaled_App_Height/17))
    Chat_Settings_Icon.setStyleSheet("background: transparent; border: none;")
    Chat_Settings_Icon.setIcon(QtGui.QIcon(f"{os.getcwd()}/icons/chat_icon.svg"))
    Chat_Settings_Icon.setIconSize(QtCore.QSize(int(Scaled_App_Width/23), int(Scaled_App_Height/19)))
    Chat_Settings_Icon.setCheckable(True) # Turns the pushbutton into a toggle switch
    Chat_Settings_Icon.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(color=QtGui.QColor(0, 0, 0, 100), blurRadius=30, xOffset=int(Scaled_App_Width/350), yOffset=int(Scaled_App_Height/350)))
    Chat_Settings_Icon.raise_()

    Chat_Settings_Title = QtWidgets.QLabel(Chat_Settings_Menu)
    Chat_Settings_Title.setObjectName("Chat_Settings_Title")
    Chat_Settings_Title.setGeometry(int(Scaled_App_Width/13.2), int(Scaled_App_Height/33), int(Scaled_App_Width/5), int(Scaled_App_Height/34))
    Chat_Settings_Title.setText("Chat Settings")

    Chat_Theme_Title = QtWidgets.QLabel(Chat_Settings_Menu)
    Chat_Theme_Title.setObjectName("Chat_Theme_Title")
    Chat_Theme_Title.setGeometry(int(Scaled_App_Width/12.8), int(Scaled_App_Height/11.2), int(Scaled_App_Width/5), int(Scaled_App_Height/34))
    Chat_Theme_Title.setText("Theme")

    Chat_Theme = QtWidgets.QComboBox(Chat_Settings_Menu)
    Chat_Theme.setObjectName("Chat_Theme")
    Chat_Theme.setGeometry(int(Scaled_App_Width/13.2), int(Scaled_App_Height/7.7), int(Scaled_App_Width/11.6), int(Scaled_App_Height/33))
    Chat_Theme.addItems(["Default", "Blue", "Dark", "Light"])
    Chat_Theme.setEnabled(False)
    Chat_Theme.currentIndexChanged.connect(lambda: Theme(Chat_Theme.currentText()))

    Chat_Selector_Title = QtWidgets.QLabel(Chat_Settings_Menu)
    Chat_Selector_Title.setObjectName("Chat_Selector_Title")
    Chat_Selector_Title.setGeometry(int(Scaled_App_Width/12.8), int(Scaled_App_Height/5), int(Scaled_App_Width/5), int(Scaled_App_Height/34))
    Chat_Selector_Title.setText("Recipient")

    Chat_Selector = QtWidgets.QComboBox(Chat_Settings_Menu)
    Chat_Selector.setObjectName("Chat_Selector")
    Chat_Selector.setGeometry(int(Scaled_App_Width/13), int(Scaled_App_Height/4.15), int(Scaled_App_Width/11.6), int(Scaled_App_Height/33))
    Chat_Selector.addItem("ALL")
    Chat_Selector.setEnabled(False)

    Chat_Confirm_Button = QtWidgets.QPushButton(Chat_Settings_Menu)
    Chat_Confirm_Button.setObjectName("Chat_Confirm_Button") 
    Chat_Confirm_Button.setGeometry(int(Scaled_App_Width/4.7), int(Scaled_App_Height/4.4), int(Scaled_App_Width/25), int(Scaled_App_Height/20))
    Chat_Confirm_Button.setStyleSheet("background: transparent; border: none;")
    Chat_Confirm_Button.setIcon(QtGui.QIcon(f"{os.getcwd()}/icons/check_icon.svg"))
    Chat_Confirm_Button.setIconSize(QtCore.QSize(int(Scaled_App_Width/21), int(Scaled_App_Height/18)))
    Chat_Confirm_Button.setEnabled(False)
    Chat_Confirm_Button.setCheckable(True) # Turns the pushbutton into a toggle switch
    Chat_Confirm_Button.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(color=QtGui.QColor(0, 0, 0, 100), blurRadius=30, xOffset=int(Scaled_App_Width/300), yOffset=int(Scaled_App_Height/350)))

# Overlays the OS provided drop down with a custom icon:
# NOTE: Please keep this code below the 'chat settings' code in order for it to be drawn above the OS drop down menu!
    Chat_Theme_Drop_Down_Background = QtWidgets.QLabel(Chat_Theme)
    Chat_Theme_Drop_Down_Background.setObjectName("Chat_Theme_Drop_Down_Background")
    Chat_Theme_Drop_Down_Background.setGeometry(int(Chat_Theme.x()/1.26), 0, int(Chat_Theme.width()/3), int(Chat_Theme.height()/1))

    Chat_Theme_Drop_Down = QtWidgets.QPushButton(Chat_Theme)
    Chat_Theme_Drop_Down.setObjectName("Chat_Theme_Drop_Down")
    Chat_Theme_Drop_Down.setGeometry(int(Chat_Theme.x()/1.26), 0, int(Chat_Theme.width()/3), int(Chat_Theme.height()/1.1))
    Chat_Theme_Drop_Down.setStyleSheet("background: transparent; border: none;")
    Chat_Theme_Drop_Down.setIcon(QtGui.QIcon(f"{os.getcwd()}/icons/drop_down_icon.svg"))
    Chat_Theme_Drop_Down.setIconSize(QtCore.QSize(int(Scaled_App_Width/25.6), int(Scaled_App_Height/20.7)))
    Chat_Theme_Drop_Down.setVisible(False)

    Chat_Selector_Drop_Down_Background = QtWidgets.QLabel(Chat_Selector)
    Chat_Selector_Drop_Down_Background.setObjectName("Chat_Selector_Drop_Down_Background")
    Chat_Selector_Drop_Down_Background.setGeometry(int(Chat_Selector.x()/1.3), 0, int(Chat_Selector.width()/3), int(Chat_Selector.height()/1))

    Chat_Selector_Drop_Down = QtWidgets.QPushButton(Chat_Selector)
    Chat_Selector_Drop_Down.setObjectName("Chat_Selector_Drop_Down")
    Chat_Selector_Drop_Down.setGeometry(int(Chat_Selector.x()/1.3), 0, int(Chat_Selector.width()/3), int(Chat_Selector.height()/1.1))
    Chat_Selector_Drop_Down.setStyleSheet("background: transparent; border: none;")
    Chat_Selector_Drop_Down.setIcon(QtGui.QIcon(f"{os.getcwd()}/icons/drop_down_icon.svg"))
    Chat_Selector_Drop_Down.setIconSize(QtCore.QSize(int(Scaled_App_Width/25.6), int(Scaled_App_Height/20.7)))
    Chat_Selector_Drop_Down.setVisible(False)

# Creates the chat log area:
    Chat_Log = QtWidgets.QListWidget(Chat_Window)
    Chat_Log.setGeometry(int(Scaled_App_Width/3.2), int(Scaled_App_Height/25.8), int(Scaled_App_Width/1.52), int(Scaled_App_Height/1.2))
    Chat_Log.setObjectName("Chat_Log")
    Chat_Log.setEnabled(False) # Keeps the area disabled from interactions before sign-in

# Creates the message field with attach button:
    Message_Field = QtWidgets.QLineEdit(Chat_Window)
    Message_Field.setObjectName("Message_Field")
    Message_Field.setGeometry(int(Scaled_App_Width/3.2), int(Scaled_App_Height), int(Scaled_App_Width/1.68), int(Scaled_App_Height/20.7))
    Message_Field.setText("Waiting for connection...")
    Message_Field.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(color=QtGui.QColor(0, 0, 0, 25), blurRadius=60, xOffset=int(Scaled_App_Width/128), yOffset=int(Scaled_App_Height/103.5)))
    Message_Field.setEnabled(False) # Keeps the field disabled from interactions before sign-in

    Message_Field_Animation = QtCore.QPropertyAnimation(Message_Field, b'pos')
    Message_Field_Animation.setStartValue(Message_Field.pos())
    Message_Field_Animation.setEndValue(QtCore.QPoint(int(Scaled_App_Width/3.2), int(Scaled_App_Height/1.1)))
    Message_Field_Animation.setDuration(150)
    
    Attach_Button = QtWidgets.QPushButton(Chat_Window)
    Attach_Button.setObjectName("Attach_Button")
    Attach_Button.setGeometry(int(Scaled_App_Width/1.075), int(Scaled_App_Height), int(Scaled_App_Width/25.09), int(Scaled_App_Height/20.29))
    Attach_Button.setStyleSheet("background: transparent; border: none;")
    Attach_Button.setIcon(QtGui.QIcon(f"{os.getcwd()}/icons/attach_icon.svg"))
    Attach_Button.setIconSize(QtCore.QSize(int(Scaled_App_Width/25.6), int(Scaled_App_Height/20.7)))
    Attach_Button.setEnabled(False) # Keeps the button disabled from interactions before sign-in

    Attach_Button_Animation = QtCore.QPropertyAnimation(Attach_Button, b'pos')
    Attach_Button_Animation.setStartValue(Attach_Button.pos())
    Attach_Button_Animation.setEndValue(QtCore.QPoint(int(Scaled_App_Width/1.075), int(Scaled_App_Height/1.1)))
    Attach_Button_Animation.setDuration(150)

    def Theme(theme_name):
        """Assigns the theme based on User selection."""
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

        Server_Settings_Menu.setStyleSheet(f"background: {Main_Background_Color}")
        Server_Settings_Title.setStyleSheet(f"color: {Main_Title_Color}; font: {Scaled_Font_Size}px;")
        Host_Title.setStyleSheet(f"color: {Main_Title_Color}; font: {Scaled_Font_Size}px;")
        Host_Address.setStyleSheet(f"background: transparent; border: transparent; border-bottom: {Scaled_Underline_Size} solid {Main_Underline_Color}; padding: 0 5px; color: {Main_Text_Color}; font: {Scaled_Font_Size}px;")
        Port_Title.setStyleSheet(f"color: {Main_Title_Color}; font: {Scaled_Font_Size}px;")
        Port_Number.setStyleSheet(f"background: transparent; border: transparent; border-bottom: {Scaled_Underline_Size} solid {Main_Underline_Color}; padding: 0 5px; color: {Main_Text_Alternate_Color}; font: {Scaled_Font_Size}px;")

        if Server_Connection_Status.text() == "<html><head/><body><center>NOT CONNECTED</center></body></html>":
            Server_Connection_Status.setStyleSheet(f"color: {Main_Status_Banner_Disconnected_Color}; background: transparent; border-bottom: 2px solid {Main_Status_Banner_Shadow_Color}; font: {Scaled_Font_Size}px;")
        else:
            Server_Connection_Status.setStyleSheet(f"color: {Main_Status_Banner_Connected_Color}; background: transparent; border-bottom: 2px solid {Main_Status_Banner_Shadow_Color}; font: {Scaled_Font_Size}px;")
        
        Sign_In_Menu.setStyleSheet(f"background: {Main_Background_Color}")
        Sign_In_Title.setStyleSheet(f"color: {Main_Title_Color}; font: {Scaled_Font_Size}px;")
        Username_Title.setStyleSheet(f"color: {Main_Title_Color}; font: {Scaled_Font_Size}px;")
        Username.setStyleSheet(f"background: transparent; border: transparent; border-bottom: {Scaled_Underline_Size} solid {Main_Underline_Color}; padding: 0 5px; color: {Main_Text_Color}; font: {Scaled_Font_Size}px;")
        Password_Title.setStyleSheet(f"color: {Main_Title_Color}; font: {Scaled_Font_Size}px;")
        Password.setStyleSheet(f"background: transparent; border: transparent; border-bottom: {Scaled_Underline_Size} solid {Main_Underline_Color}; padding: 0 5px; color: {Main_Text_Alternate_Color}; font: {Scaled_Font_Size}px;")
        
        if User_Connection_Status.text() == "<html><head/><body><center>SIGNED-OUT       </center></body></html>":
            User_Connection_Status.setStyleSheet(f"color: {Main_Status_Banner_Disconnected_Color}; background: transparent; border-bottom: 2px solid {Main_Status_Banner_Shadow_Color}; font: {Scaled_Font_Size}px;")
        else:
            User_Connection_Status.setStyleSheet(f"color: {Main_Status_Banner_Connected_Color}; background: transparent; border-bottom: 2px solid {Main_Status_Banner_Shadow_Color}; font: {Scaled_Font_Size}px;")

        # Avatar_Selector_Widget.setStyleSheet(f"background: {Main_Background_Color}")
        Avatar_Selector_Widget.setStyleSheet(f"background: #31315B; border-radius: {Scaled_Border_Radius}px")
        
        Chat_Settings_Menu.setStyleSheet(f"background: {Main_Background_Color}")
        Chat_Settings_Title.setStyleSheet(f"color: {Main_Title_Color}; font: {Scaled_Font_Size}px;")
        Chat_Theme_Title.setStyleSheet(f"color: {Main_Title_Color}; font: {Scaled_Font_Size}px;")
        Chat_Theme.setStyleSheet(f"background: {Main_Background_Color}; border: none; border-bottom: {Scaled_Underline_Size} solid {Main_Underline_Color}; padding: 0 5px; color: {Main_Text_Color}; font: {Scaled_Font_Size}px;")
        Chat_Selector_Title.setStyleSheet(f"color: {Main_Title_Color}; font: {Scaled_Font_Size}px;")
        Chat_Selector.setStyleSheet(f"background: {Main_Background_Color}; border: none; border-bottom: {Scaled_Underline_Size} solid {Main_Underline_Color}; padding: 0 5px; color: {Main_Text_Alternate_Color}; font: {Scaled_Font_Size}px;")
        Chat_Theme_Drop_Down_Background.setStyleSheet(f"background: {Main_Background_Color}")
        Chat_Selector_Drop_Down_Background.setStyleSheet(f"background: {Main_Background_Color}")
        
        Chat_Window.setStyleSheet(f"background-color: {Main_Chat_Log_Background_Color}")
        Chat_Log.setStyleSheet(f"border: none; color: {Main_Chat_Log_Text_Color}; background-color: {Main_Chat_Log_Background_Color}; padding: 10px 20px; font: {Scaled_Font_Size}px;")
        Message_Field.setStyleSheet(f"border: 0px solid #000000; color: {Main_Message_Field_Text_Color}; background-color: {Main_Message_Field_Background_Color}; border-radius: {Scaled_Border_Radius}px; padding: 0 15px; font: {Scaled_Font_Size}px;")

    Theme("Default") # Starts the app in default theme

    def Connect_Client():
            """Connects to the server with provided hostname and port."""
            if Server_Button.isChecked():
                HOST = Host_Address.text()
                PORT = int(Port_Number.text())

                SOCKET.connectToHost(QtNetwork.QHostAddress(HOST), PORT)
                Send_Message("{CONNECT}")

                Server_Button.setIcon(QtGui.QIcon(f"{os.getcwd()}/icons/exit_icon.svg"))
                Server_Connection_Status.setText("<html><head/><body><center>CONNECTED     </center></body></html>")
                Theme(Chat_Theme.currentText())

                Host_Address.setEnabled(False)
                Port_Number.setEnabled(False)

                Temporary_Avatar.setVisible(False)
                User_Avatar.setVisible(True)
                Username.setEnabled(True)
                Sign_In_Button.setEnabled(True)

                Message_Field.setText("Waiting for sign-in...")

            else:
                Send_Message("{DISCONNECT}")

                Server_Button.setIcon(QtGui.QIcon(f"{os.getcwd()}/icons/enter_icon.svg"))
                Server_Connection_Status.setText("<html><head/><body><center>NOT CONNECTED</center></body></html>")
                Theme(Chat_Theme.currentText())

                Host_Address.setEnabled(True)
                Port_Number.setEnabled(True)

                Temporary_Avatar.setVisible(True)
                User_Avatar.setVisible(False)
                Username.setEnabled(False)
                Sign_In_Button.setEnabled(False)

                Message_Field.setText("Dissconnected! Good Bye...")

    def Sign_In():
        """Registers the provided username with the server."""
        if Sign_In_Button.isChecked():
            Send_Message("{REGISTER}")
            Server_Button.setEnabled(False)

            Sign_In_Button.setIcon(QtGui.QIcon(f"{os.getcwd()}/icons/exit_icon.svg"))
            User_Connection_Status.setText("<html><head/><body><center>SIGNED-IN        </center></body></html>")
            Theme(Chat_Theme.currentText())
            
            Username.setEnabled(False)
            Temporary_Avatar.setVisible(True)
            User_Avatar.setVisible(False)

            Chat_Theme.setEnabled(True)
            Chat_Theme_Drop_Down.setVisible(True)
            Chat_Selector.setEnabled(True)
            Chat_Selector.setItemText(0,"ALL")
            Chat_Selector_Drop_Down.setVisible(True)
            Chat_Confirm_Button.setEnabled(True)

            Message_Field.setText("Select a user to start chatting...")
            Chat_Log.setEnabled(True)

        else:
            Send_Message("{UNREGISTER}")
            Server_Button.setEnabled(True)

            Sign_In_Button.setIcon(QtGui.QIcon(f"{os.getcwd()}/icons/enter_icon.svg"))
            User_Connection_Status.setText("<html><head/><body><center>SIGNED-OUT       </center></body></html>")
            Theme(Chat_Theme.currentText())

            Username.setEnabled(True)
            Temporary_Avatar.setVisible(False)
            User_Avatar.setVisible(True)

            Chat_Theme.setEnabled(False)
            Chat_Theme_Drop_Down.setVisible(False)
            Chat_Selector.setEnabled(False)
            Chat_Selector_Drop_Down.setVisible(False)
            Chat_Confirm_Button.setEnabled(False)

            Message_Field.setText("Signed Out!...")
            Chat_Log.setEnabled(False)

    def Send_Message(message, HOST = "127.0.0.1", PORT = 33002):
        if message.startswith("{FIELD}"):
            message = message.replace("{FIELD}", "")
            SOCKET.writeDatagram(message.encode(), QtNetwork.QHostAddress(HOST), PORT)
            Message_Field.setText("")
            Message_Field.setFocus()
        else:
            SOCKET.writeDatagram(message.encode(), QtNetwork.QHostAddress(HOST), PORT)

    def Receive_Message():
        while SOCKET.hasPendingDatagrams():
            received_message, received_client, received_port = SOCKET.readDatagram(SOCKET.pendingDatagramSize())
            received_message = received_message.decode()

            if received_message.startswith("{MSG}"):
                received_message = received_message.replace("{MSG}", "")
                Chat_Log.addItem(received_message)
    
    # timer = QtCore.QTimer(interval=1000, timeout=Sign_In)
    # timer.start()

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
            Chat_Confirm_Button.setIcon(QtGui.QIcon(QtGui.QPixmap(f"{os.getcwd()}/icons/cancel_icon.svg")))
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
            Chat_Confirm_Button.setIcon(QtGui.QIcon(QtGui.QPixmap(f"{os.getcwd()}/icons/check_icon.svg")))
            Chat_Theme.setEnabled(True)
            Chat_Theme_Drop_Down.setVisible(True)
            Chat_Selector.setEnabled(True)
            Chat_Selector_Drop_Down.setVisible(True)

            Sign_In_Button.setEnabled(True)

            Message_Field.setEnabled(False)
            Message_Field.setText("Select a User to start chatting...")
            Chat_Log.setEnabled(False)

            Attach_Button.setEnabled(False)

    def Attach_Picture():
        Image = QtWidgets.QFileDialog.getOpenFileName(Chat_Window, 'Attach an Image', os.getcwd(), "Image files (*.jpg *.png *.gif *.svg)")

        Attached_Image = QtWidgets.QListWidgetItem("\n\n\n\n")
        Attached_Image.setIcon(QtGui.QIcon(Image[0]))
        Chat_Log.setIconSize(QtCore.QSize(int(Scaled_App_Width/20), int(Scaled_App_Height/17)))
        Chat_Log.addItem(Attached_Image) 

# Assigns each pushbutton their respective function:
    SOCKET.readyRead.connect(Receive_Message)
    Server_Button.clicked.connect(Connect_Client)
    User_Avatar.clicked.connect(Open_Avatar_Selector)
    Sign_In_Button.clicked.connect(Sign_In)
    Chat_Theme_Drop_Down.clicked.connect(lambda: Better_Drop_Down(0))
    Chat_Selector_Drop_Down.clicked.connect(lambda: Better_Drop_Down(1))
    Chat_Confirm_Button.clicked.connect(Chat_Target)
    Message_Field.returnPressed.connect(lambda: Send_Message(f"{{FIELD}}{{{Chat_Selector.currentText()}}}Message_Field.text()"))
    Attach_Button.clicked.connect(Attach_Picture)

# Draws the entire GUI:
    Chat_Window.show()
    Server_Settings_Menu_Animation.start()
    Sign_In_Menu_Animation.start()
    Chat_Settings_Menu_Animation.start()
    Message_Field_Animation.start()
    Attach_Button_Animation.start()
    sys.exit(app.exec_())

if __name__ == "__main__":
    Run_Client()