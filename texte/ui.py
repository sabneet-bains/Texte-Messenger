"""Layout-based widget construction for the Texte client."""

from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets

from texte.widgets import InvisibleItemDelegate, SmoothListWidget, ThemeModeSwitch

ICON_BUTTON_SIZE = 22
SIDEBAR_MIN_WIDTH = 300
SIDEBAR_MAX_WIDTH = 380
FIELD_MIN_WIDTH = 136
AVATAR_COLUMNS = 4
AVATAR_PAGE_SIZE = 12
PINNED_COLUMNS = 3


def setup_ui(client) -> None:
    """Build the native-window Messages-style shell for ChatClient."""
    _build_window(client)
    _build_sidebar(client)
    _build_setup_sheet(client)
    _build_chat_area(client)
    _build_profile_popup(client)
    _init_hidden_chat_state(client)
    client.root_layout.addWidget(client.splitter)


def _build_window(client) -> None:
    client.setObjectName("Chat_Window")
    client.resize(1120, 700)
    client.setMinimumSize(760, 520)
    client.setWindowTitle("texte")
    client.setWindowIcon(QtGui.QIcon(client._asset_path("icons", "texte_icon.svg")))
    client.setWindowFlags(
        QtCore.Qt.WindowType.Window
        | QtCore.Qt.WindowType.WindowSystemMenuHint
        | QtCore.Qt.WindowType.WindowMinimizeButtonHint
        | QtCore.Qt.WindowType.WindowMaximizeButtonHint
        | QtCore.Qt.WindowType.WindowCloseButtonHint
    )

    client.root_layout = QtWidgets.QHBoxLayout(client)
    client.root_layout.setContentsMargins(0, 0, 0, 0)
    client.root_layout.setSpacing(0)

    client.splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal, client)
    client.splitter.setObjectName("Main_Splitter")
    client.splitter.setChildrenCollapsible(False)


def _build_sidebar(client) -> None:
    client.sidebar = QtWidgets.QWidget(client.splitter)
    client.sidebar.setObjectName("Sidebar")
    client.sidebar.setMinimumWidth(SIDEBAR_MIN_WIDTH)
    client.sidebar.setMaximumWidth(SIDEBAR_MAX_WIDTH)

    client.sidebar_layout = QtWidgets.QVBoxLayout(client.sidebar)
    client.sidebar_layout.setContentsMargins(14, 14, 14, 14)
    client.sidebar_layout.setSpacing(10)

    toolbar_row = QtWidgets.QHBoxLayout()
    toolbar_row.setContentsMargins(0, 0, 0, 0)
    toolbar_row.setSpacing(8)

    title_stack = QtWidgets.QVBoxLayout()
    title_stack.setContentsMargins(0, 0, 0, 0)
    title_stack.setSpacing(0)
    client.app_title = QtWidgets.QLabel("Messages")
    client.app_title.setObjectName("App_Title")
    client.app_subtitle = QtWidgets.QLabel("Local conversations")
    client.app_subtitle.setObjectName("App_Subtitle")
    title_stack.addWidget(client.app_title)
    title_stack.addWidget(client.app_subtitle)

    action_row = QtWidgets.QHBoxLayout()
    action_row.setContentsMargins(0, 0, 0, 0)
    action_row.setSpacing(8)

    client.setup_button = _icon_round_button(
        client.sidebar,
        client._asset_path("icons", "filter_icon.svg"),
        "Setup_Button",
    )
    client.setup_button.setCheckable(True)
    client.setup_button.setToolTip("Advanced settings")
    client.new_message_button = _icon_round_button(
        client.sidebar,
        client._asset_path("icons", "compose_icon.svg"),
        "New_Message_Button",
    )
    client.new_message_button.setToolTip("Focus the current chat")
    action_row.addWidget(client.setup_button)
    action_row.addWidget(client.new_message_button)

    toolbar_row.addLayout(title_stack, 1)
    toolbar_row.addLayout(action_row)
    client.sidebar_layout.addLayout(toolbar_row)

    client.search_field = QtWidgets.QLineEdit()
    client.search_field.setObjectName("Search_Field")
    client.search_field.setPlaceholderText("Search")
    client.search_field.addAction(
        QtGui.QIcon(client._asset_path("icons", "search_icon.svg")),
        QtWidgets.QLineEdit.ActionPosition.LeadingPosition,
    )
    client.sidebar_layout.addWidget(client.search_field)

    client.pinned_title = QtWidgets.QLabel("Pinned")
    client.pinned_title.setObjectName("Sidebar_Section_Label")
    client.sidebar_layout.addWidget(client.pinned_title)

    client.pinned_widget = QtWidgets.QWidget(client.sidebar)
    client.pinned_widget.setObjectName("Pinned_Widget")
    client.pinned_layout = QtWidgets.QGridLayout(client.pinned_widget)
    client.pinned_layout.setContentsMargins(0, 0, 0, 0)
    client.pinned_layout.setHorizontalSpacing(8)
    client.pinned_layout.setVerticalSpacing(8)
    client.sidebar_layout.addWidget(client.pinned_widget)

    client.recent_title = QtWidgets.QLabel("Messages")
    client.recent_title.setObjectName("Sidebar_Section_Label")
    client.sidebar_layout.addWidget(client.recent_title)

    client.conversation_list = QtWidgets.QListWidget()
    client.conversation_list.setObjectName("Conversation_List")
    client.conversation_list.setSelectionMode(
        QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
    )
    client.conversation_list.setItemDelegate(InvisibleItemDelegate(client.conversation_list))
    client.conversation_list.setSpacing(2)
    client.conversation_list.addItem("ALL")
    client.conversation_list.setCurrentRow(0)
    client.sidebar_layout.addWidget(client.conversation_list, 1)
    client.splitter.addWidget(client.sidebar)


def _build_setup_sheet(client) -> None:
    client.setup_sheet = QtWidgets.QFrame(client.sidebar)
    client.setup_sheet.setObjectName("Setup_Sheet")
    client.setup_sheet.setVisible(False)
    client.setup_sheet.raise_()

    sheet_layout = QtWidgets.QVBoxLayout(client.setup_sheet)
    sheet_layout.setContentsMargins(14, 14, 14, 14)
    sheet_layout.setSpacing(10)

    sheet_header = QtWidgets.QHBoxLayout()
    sheet_header.setContentsMargins(0, 0, 0, 0)
    client.setup_title = QtWidgets.QLabel("Advanced")
    client.setup_title.setObjectName("Setup_Title")
    client.setup_close_button = _icon_button(
        client.setup_sheet,
        client._asset_path("icons", "cancel_icon.svg"),
    )
    client.setup_close_button.setObjectName("Setup_Close_Button")
    sheet_header.addWidget(client.setup_title, 1)
    sheet_header.addWidget(client.setup_close_button)
    sheet_layout.addLayout(sheet_header)

    client.setup_content = QtWidgets.QWidget()
    client.setup_content.setObjectName("Setup_Content")
    content_layout = QtWidgets.QVBoxLayout(client.setup_content)
    content_layout.setContentsMargins(0, 0, 0, 0)
    content_layout.setSpacing(14)

    _add_connection_section(client, content_layout)
    content_layout.addStretch(1)
    sheet_layout.addWidget(client.setup_content)


def _add_connection_section(client, layout: QtWidgets.QVBoxLayout) -> None:
    layout.addWidget(_section_label("Local Server"))
    form = _form_layout()

    client.host_title = _form_label("Host", "Host_Title")
    client.host_address = QtWidgets.QLineEdit()
    client.host_address.setObjectName("Host_Address")
    client.host_address.setText("127.0.0.1")

    client.port_title = _form_label("Port", "Port_Title")
    client.port_number = QtWidgets.QLineEdit()
    client.port_number.setObjectName("Port_Number")
    client.port_number.setText("33002")
    client.port_number.setValidator(QtGui.QIntValidator(1, 65535))

    client.protocol_selector = QtWidgets.QComboBox(client.setup_content)
    client.protocol_selector.setObjectName("Protocol_Selector")
    client.protocol_selector.addItems(["TCP", "UDP"])
    client.protocol_selector.hide()

    client.protocol_switch = QtWidgets.QFrame(client.setup_content)
    client.protocol_switch.setObjectName("Protocol_Switch")
    protocol_layout = QtWidgets.QHBoxLayout(client.protocol_switch)
    protocol_layout.setContentsMargins(4, 4, 4, 4)
    protocol_layout.setSpacing(4)

    client.protocol_tcp_button = QtWidgets.QPushButton("TCP")
    client.protocol_tcp_button.setObjectName("Protocol_TCP_Button")
    client.protocol_tcp_button.setCheckable(True)
    client.protocol_udp_button = QtWidgets.QPushButton("UDP")
    client.protocol_udp_button.setObjectName("Protocol_UDP_Button")
    client.protocol_udp_button.setCheckable(True)
    protocol_layout.addWidget(client.protocol_tcp_button)
    protocol_layout.addWidget(client.protocol_udp_button)

    client.auto_server_checkbox = QtWidgets.QCheckBox("Start local server automatically")
    client.auto_server_checkbox.setObjectName("Auto_Server_Checkbox")
    client.auto_server_checkbox.setChecked(True)

    form.addRow(client.host_title, client.host_address)
    form.addRow(client.port_title, client.port_number)
    form.addRow(_form_label("Protocol", "Protocol_Title"), client.protocol_switch)
    layout.addLayout(form)
    layout.addWidget(client.auto_server_checkbox)

    client.server_connection_status = _chip("Offline", "Server_Connection_Status")
    client.server_button = _text_button("Connect", "Server_Button")
    client.server_button.setCheckable(True)
    layout.addWidget(client.server_button)


def _add_identity_section(
    client,
    layout: QtWidgets.QVBoxLayout,
    parent: QtWidgets.QWidget,
    *,
    show_section_label: bool = True,
) -> None:
    if show_section_label:
        layout.addWidget(_section_label("Profile"))
    row = QtWidgets.QHBoxLayout()
    row.setContentsMargins(0, 0, 0, 0)
    row.setSpacing(10)

    # Create a separate avatar button for the profile popup (not the header one)
    profile_avatar = _icon_button(
        parent,
        client._asset_path("avatars", "user1.svg"),
        checkable=True,
    )
    profile_avatar.setObjectName("user1")
    profile_avatar.setEnabled(True)
    profile_avatar.clicked.connect(client.open_avatar_selector)
    # Store reference so choose_avatar can update it
    client.temporary_avatar = profile_avatar

    client.username_title = _form_label("Name", "Username_Title")
    client.username = QtWidgets.QLineEdit()
    client.username.setObjectName("Username")
    client.username.setText("Hugo")
    client.username.setEnabled(False)
    client.username.setPlaceholderText("Display name")

    row.addWidget(profile_avatar)
    row.addWidget(client.username, 1)
    layout.addLayout(row)

    client.sign_in_button = _text_button("Sign in", "Sign_In_Button")
    client.sign_in_button.setCheckable(True)
    client.sign_in_button.setEnabled(False)
    layout.addWidget(client.sign_in_button)


def _build_avatar_selector(
    client,
    layout: QtWidgets.QVBoxLayout,
    parent: QtWidgets.QWidget,
) -> None:
    client.avatar_selector_panel = QtWidgets.QDialog(parent)
    client.avatar_selector_panel.setObjectName("Avatar_Selector_Panel")
    client.avatar_selector_panel.setWindowFlags(
        QtCore.Qt.WindowType.Popup | QtCore.Qt.WindowType.FramelessWindowHint
    )
    client.avatar_selector_panel.setVisible(False)

    panel_layout = QtWidgets.QVBoxLayout(client.avatar_selector_panel)
    panel_layout.setContentsMargins(10, 10, 10, 10)
    panel_layout.setSpacing(8)

    navigation = QtWidgets.QHBoxLayout()
    navigation.setContentsMargins(0, 0, 0, 0)
    navigation.setSpacing(8)

    client.avatar_previous_button = _text_button("Previous", "Avatar_Previous_Button")
    client.avatar_next_button = _text_button("Next", "Avatar_Next_Button")
    navigation.addWidget(client.avatar_previous_button)
    navigation.addWidget(client.avatar_next_button)
    panel_layout.addLayout(navigation)

    client.avatar_selector_widget = QtWidgets.QStackedWidget(client.avatar_selector_panel)
    client.avatar_selector_widget.setObjectName("Avatar_Selector_Widget")
    panel_layout.addWidget(client.avatar_selector_widget)

    avatar_paths = _avatar_paths(client)
    page_count = max(1, (len(avatar_paths) + AVATAR_PAGE_SIZE - 1) // AVATAR_PAGE_SIZE)

    for page_index in range(page_count):
        page = QtWidgets.QWidget()
        page_number = page_index + 1
        page.setObjectName(f"Avatar_Selector_Page_{page_number}")
        page_layout = QtWidgets.QGridLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(8)

        start = page_index * AVATAR_PAGE_SIZE
        for avatar_index, avatar_path in enumerate(avatar_paths[start : start + AVATAR_PAGE_SIZE]):
            avatar_name = avatar_path.stem
            button = _icon_button(page, str(avatar_path))
            button.setObjectName(avatar_name)
            button.setToolTip(avatar_name)
            button.clicked.connect(
                lambda _checked=False, name=avatar_name: client.choose_avatar(name)
            )
            row, column = divmod(avatar_index, AVATAR_COLUMNS)
            page_layout.addWidget(button, row, column)

        client.avatar_selector_widget.addWidget(page)
        setattr(client, f"avatar_selector_page{page_number}", page)

    client.update_avatar_navigation()


def _build_chat_area(client) -> None:
    chat_shell = QtWidgets.QWidget(client.splitter)
    chat_shell.setObjectName("Chat_Area")
    chat_layout = QtWidgets.QVBoxLayout(chat_shell)
    chat_layout.setContentsMargins(20, 8, 20, 14)
    chat_layout.setSpacing(8)

    client.chat_header = QtWidgets.QWidget(chat_shell)
    client.chat_header.setObjectName("Chat_Header")
    header = QtWidgets.QHBoxLayout(client.chat_header)
    header.setContentsMargins(0, 2, 0, 4)
    header.setSpacing(10)

    # Start empty; the client will set this based on the active conversation
    client.chat_header_avatar = QtWidgets.QLabel("")
    client.chat_header_avatar.setObjectName("Chat_Header_Avatar")
    client.chat_header_avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    client.chat_header_avatar.setFixedSize(34, 34)

    title_stack = QtWidgets.QVBoxLayout()
    title_stack.setContentsMargins(0, 0, 0, 0)
    title_stack.setSpacing(0)
    client.chat_title = QtWidgets.QLabel("ALL")
    client.chat_title.setObjectName("Chat_Title")
    client.chat_subtitle = QtWidgets.QLabel("Connect, sign in, then start chatting")
    client.chat_subtitle.setObjectName("Chat_Subtitle")
    title_stack.addWidget(client.chat_title)
    title_stack.addWidget(client.chat_subtitle)

    client.theme_light_button = _segmented_theme_button(
        client._asset_path("icons", "theme_sun.svg"),
        "Theme_Light_Button",
    )
    client.theme_dark_button = _segmented_theme_button(
        client._asset_path("icons", "theme_moon.svg"),
        "Theme_Dark_Button",
    )
    client.theme_switch = ThemeModeSwitch(
        client._asset_path("icons", "theme_sun.svg"),
        client._asset_path("icons", "theme_moon.svg"),
        chat_shell,
    )
    client.theme_switch.setToolTip("Switch light or dark theme")
    
    # Create centered profile section (avatar + username)
    profile_section = QtWidgets.QWidget(chat_shell)
    profile_layout = QtWidgets.QVBoxLayout(profile_section)
    profile_layout.setContentsMargins(0, 0, 0, 0)
    profile_layout.setSpacing(4)
    
    client.user_avatar = _icon_button(
        profile_section,
        client._asset_path("avatars", "user1.svg"),
        checkable=True,
    )
    client.user_avatar.setObjectName("user1")
    client.user_avatar.setEnabled(False)
    client.user_avatar.setToolTip("Profile")
    
    client.header_username = QtWidgets.QLabel("Profile")
    client.header_username.setObjectName("Header_Username")
    client.header_username.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    
    profile_layout.addWidget(client.user_avatar, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
    profile_layout.addWidget(client.header_username, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
    
    header.addWidget(client.chat_header_avatar, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
    header.addLayout(title_stack, 0)
    header.addStretch(1)
    header.addWidget(profile_section, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
    header.addStretch(1)
    header.addWidget(client.theme_switch, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
    chat_layout.addWidget(client.chat_header)

    client.chat_log = SmoothListWidget()
    client.chat_log.setObjectName("Chat_Log")
    client.chat_log.setEnabled(False)
    client.chat_log.setSizePolicy(
        QtWidgets.QSizePolicy.Policy.Expanding,
        QtWidgets.QSizePolicy.Policy.Expanding,
    )
    chat_layout.addWidget(client.chat_log, 1)

    client.composer_panel = QtWidgets.QFrame(chat_shell)
    client.composer_panel.setObjectName("Composer_Panel")
    composer = QtWidgets.QHBoxLayout(client.composer_panel)
    composer.setContentsMargins(0, 4, 0, 0)
    composer.setSpacing(10)

    client.attach_button = _icon_round_button(
        client.composer_panel,
        client._asset_path("icons", "attach_icon.svg"),
        "Attach_Button",
    )
    client.attach_button.setEnabled(False)

    client.composer_shell = QtWidgets.QFrame(client.composer_panel)
    client.composer_shell.setObjectName("Composer_Shell")
    composer_shell_layout = QtWidgets.QHBoxLayout(client.composer_shell)
    composer_shell_layout.setContentsMargins(18, 4, 8, 4)
    composer_shell_layout.setSpacing(8)

    client.message_field = QtWidgets.QLineEdit()
    client.message_field.setObjectName("Message_Field")
    client.message_field.setPlaceholderText("iMessage")
    client.message_field.setText("Waiting for connection...")
    client.message_field.setEnabled(False)
    client.message_field.setSizePolicy(
        QtWidgets.QSizePolicy.Policy.Expanding,
        QtWidgets.QSizePolicy.Policy.Fixed,
    )

    client.emoji_button = _icon_round_button(
        client.composer_shell,
        client._asset_path("icons", "emoji_icon.svg"),
        "Emoji_Button",
    )
    client.emoji_button.setEnabled(False)
    client.emoji_button.setToolTip("Emoji")

    composer.addWidget(client.attach_button)
    composer_shell_layout.addWidget(client.message_field, 1)
    composer_shell_layout.addWidget(client.emoji_button)
    composer.addWidget(client.composer_shell, 1)
    chat_layout.addWidget(client.composer_panel)
    client.splitter.addWidget(chat_shell)
    client.splitter.setSizes([324, 796])


def _build_profile_popup(client) -> None:
    client.profile_popup = QtWidgets.QFrame(client)
    client.profile_popup.setObjectName("Profile_Popup")
    client.profile_popup.setMinimumWidth(320)
    client.profile_popup.hide()

    popup_layout = QtWidgets.QVBoxLayout(client.profile_popup)
    popup_layout.setContentsMargins(16, 16, 16, 16)
    popup_layout.setSpacing(12)

    client.profile_title = QtWidgets.QLabel("Profile")
    client.profile_title.setObjectName("Setup_Title")
    popup_layout.addWidget(client.profile_title)

    _add_identity_section(client, popup_layout, client.profile_popup, show_section_label=False)
    _build_avatar_selector(client, popup_layout, client.profile_popup)


def _init_hidden_chat_state(client) -> None:
    client.chat_theme = QtWidgets.QComboBox(client)
    client.chat_theme.setObjectName("Chat_Theme")
    client.chat_theme.addItems(["Light", "Dark"])
    client.chat_theme.hide()

    client.chat_selector = QtWidgets.QComboBox(client)
    client.chat_selector.setObjectName("Chat_Selector")
    client.chat_selector.addItem("ALL")
    client.chat_selector.hide()

    client.chat_confirm_button = QtWidgets.QPushButton(client)
    client.chat_confirm_button.setObjectName("Chat_Confirm_Button")
    client.chat_confirm_button.hide()


def _avatar_paths(client) -> list[Path]:
    avatar_dir = Path(client._asset_path("avatars"))
    return sorted(avatar_dir.glob("user*.svg"), key=_avatar_number)


def _avatar_number(path: Path) -> int:
    stem = path.stem.removeprefix("user")
    return int(stem) if stem.isdecimal() else 0


def _form_layout() -> QtWidgets.QFormLayout:
    layout = QtWidgets.QFormLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setHorizontalSpacing(10)
    layout.setVerticalSpacing(9)
    layout.setLabelAlignment(
        QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
    )
    layout.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
    layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
    return layout


def _form_label(text: str, object_name: str) -> QtWidgets.QLabel:
    label = QtWidgets.QLabel(text)
    label.setObjectName(object_name)
    label.setMinimumWidth(56)
    label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
    return label


def _section_label(text: str) -> QtWidgets.QLabel:
    label = QtWidgets.QLabel(text)
    label.setObjectName("Setup_Section_Label")
    return label


def _chip(text: str, object_name: str) -> QtWidgets.QLabel:
    label = QtWidgets.QLabel(text)
    label.setObjectName(object_name)
    label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
    return label


def _prepare_combo(combo: QtWidgets.QComboBox) -> None:
    combo.setMinimumWidth(FIELD_MIN_WIDTH)
    popup_view = QtWidgets.QListView(combo)
    popup_view.setObjectName(f"{combo.objectName()}_Popup")
    combo.setView(popup_view)


def _icon_button(
    parent: QtWidgets.QWidget,
    icon_path: str,
    *,
    checkable: bool = False,
) -> QtWidgets.QPushButton:
    button = QtWidgets.QPushButton(parent)
    button.setIcon(QtGui.QIcon(icon_path))
    button.setIconSize(QtCore.QSize(ICON_BUTTON_SIZE, ICON_BUTTON_SIZE))
    button.setFixedSize(ICON_BUTTON_SIZE + 18, ICON_BUTTON_SIZE + 18)
    button.setCheckable(checkable)
    return button


def _text_button(text: str, object_name: str) -> QtWidgets.QPushButton:
    button = QtWidgets.QPushButton(text)
    button.setObjectName(object_name)
    button.setMinimumHeight(34)
    return button


def _round_button(text: str, object_name: str) -> QtWidgets.QPushButton:
    button = QtWidgets.QPushButton(text)
    button.setObjectName(object_name)
    button.setFixedSize(34, 34)
    return button


def _icon_round_button(
    parent: QtWidgets.QWidget,
    icon_path: str,
    object_name: str,
) -> QtWidgets.QPushButton:
    button = QtWidgets.QPushButton(parent)
    button.setObjectName(object_name)
    button.setIcon(QtGui.QIcon(icon_path))
    button.setIconSize(QtCore.QSize(18, 18))
    button.setFixedSize(34, 34)
    return button


def _segmented_theme_button(icon_path: str, object_name: str) -> QtWidgets.QPushButton:
    button = QtWidgets.QPushButton()
    button.setObjectName(object_name)
    button.setCheckable(True)
    button.setIcon(QtGui.QIcon(icon_path))
    button.setIconSize(QtCore.QSize(24, 24))
    button.setFixedSize(44, 44)
    button.hide()
    return button
