from .widget import HtmlElement


# -----------------------------------------------------------------------------
# File Browser Widget
# -----------------------------------------------------------------------------
class FileBrowser(HtmlElement):
    """
    The FileBrowser widget for trame can be used in "Save" mode (default) or "Open" mode.
    In Save mode, the widget requires a list of all applicable types for the file about to be saved.
        Each item in the file types list should be a dictionary containing the following keys:
        "value" (for the file extension string, beginning with ".")
        "text" (for the name of the file type, as should appear in the file type select box)
    The widget requires a list of possible directory paths for both local and remote locations.
    The user may select a current directory for both local and remote locations.
    When either current directory is changed, the values for the current directory contents should be re-evaluated.
    Directory contents should come as a list of files, folders, and groups.
        A file is an object with the following shape:
        { name: str, type: str, size: str, modified: str, owner: str}
        A folder is an an object of the following shape:
        { name: str, type: 'folder', size: str, modified: str, owner: str}
        A group is an object of the following shape:
        { name: str, type: 'group', size: str, modified: str, owner: str, files: list[file] }


    :param mode: String containing either "Save" or "Open"
    :type mode: str
    :param dark: true for dark UI mode, false otherwise
    :type dark: bool
    :param file_types: List containing file types applicable to the current file (in Save mode only).
    :param file_types: list[{value: string, text: string}]

    :param local_hierarchy: List of full paths of all parents of current_local_dir
    :type local_hierarchy: list[str]
    :param remote_hierarchy: List of full paths of all parents of current_remote_dir
    :type remote_hierarchy: list[str]

    :param current_local_dir: Current local directory path
    :type current_local_dir: str
    :param current_remote_dir: Current remote directory path
    :type current_remote_dir: str

    :param current_local_dir_contents: Contents of current local directory
    :type current_local_dir_contents: list[file, folder, group]
    :param current_remote_dir_contents: Contents of current remote directory
    :type current_remote_dir_contents: list[file, folder, group]

    :param set_local_dir: Event triggered when user changes the current local dir
    :type set_local_dir: Function or JS expression (event)
    :param set_remote_dir: Event triggered when user changes the current remote dir
    :type set_remote_dir: Function or JS expression (event)

    :param byte_formatter (optional): A function that converts raw bytes to a user-friendlier string for populating the size column of the file browser.
    :type byte_formatter: (name of) a JS function to format the size in bytes to a string.

    :param date_formatter (optional): A function that converts raw UNIX timestapss to a user-friendlier string for populating the date column of the file browser.
    :type date_formatter: (name of) a JS function to format the date to a string.

    Events:

    :param submit: Event triggered when user clicks the submit button, either to Save or to Open
    :type submit: Function or JS expression (event)
    """

    def __init__(self, **kwargs):
        super().__init__(
            "file-browser",
            **kwargs,
        )
        self._attr_names += [
            "mode",
            "title",
            "visible",
            "locations",
            ("goto_shortcuts", "shortcutGoTo"),
            ("enable_history", "enableHistory"),
            "dark",
            ("file_types", "fileTypes"),
            ("local_hierarchy", "localHierarchy"),
            ("remote_hierarchy", "remoteHierarchy"),
            ("current_local_dir", "currentLocalDir"),
            ("current_remote_dir", "currentRemoteDir"),
            ("current_local_dir_contents", "currentLocalDirContents"),
            ("current_remote_dir_contents", "currentRemoteDirContents"),
            ("byte_formatter", "byteFormatter"),
            ("date_formatter", "dateFormatter"),
        ]
        self._event_names += [
            ("set_local_dir", "setLocalDir"),
            ("set_remote_dir", "setRemoteDir"),
            "submit",
            "close",
            "goto",
        ]
