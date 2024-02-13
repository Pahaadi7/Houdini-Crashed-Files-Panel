from PySide2 import QtWidgets, QtCore, QtGui
import os
import stat

class crashedFiles(QtWidgets.QWidget):
    def __init__(self):
        super(crashedFiles, self).__init__()

        self.deleted_files = []
        # Assuming the user's home directory is dynamic
        user_home = os.path.expanduser("~")
        version = hou.applicationVersion()
        version_string = f"{version[0]}.{version[1]}"
        
        # The relative path from the home directory to the config directory
        relative_path = "Documents/houdini"+version_string+"/CrashedFiles"
        
        # Construct the full path
        self.config_directory = os.path.join(user_home, relative_path)
        self.config_file_path = os.path.join(self.config_directory, 'config.txt')
        self.check_config_directory()
        self.directory_path = self.load_directory_path()
        
        
        relative_envPath = "Documents/houdini"+version_string+"/houdini.env"
        self.env_file_path = os.path.join(user_home, relative_envPath)

        # Set up the UI elements
        layout = QtWidgets.QVBoxLayout(self)

        header_label = QtWidgets.QLabel("Crashed Files", self)
        header_label.setObjectName("headerLabel")
        header_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-bottom: 10px;")
        layout.addWidget(header_label)

        self.path_layout = QtWidgets.QHBoxLayout()
        self.path_label = QtWidgets.QLabel("Temp Directory Path: ", self)
        self.path_edit = QtWidgets.QLineEdit(self.directory_path, self)
        self.path_edit.setReadOnly(True)
        self.path_button = QtWidgets.QPushButton("Change", self)
        self.path_button.clicked.connect(self.change_directory_path)
        self.path_layout.addWidget(self.path_label)
        self.path_layout.addWidget(self.path_edit)
        self.path_layout.addWidget(self.path_button)
        layout.addLayout(self.path_layout)

        self.search_box = QtWidgets.QLineEdit(self)
        self.search_box.setPlaceholderText("Search...")
        self.search_box.setStyleSheet("background-color: #333; color: white; border: 1px solid #555; padding: 5px; border-radius: 5px;")
        self.search_box.textChanged.connect(self.filter_file_list)  # Connect textChanged signal to filter_file_list method
        layout.addWidget(self.search_box)

        self.file_table = QtWidgets.QTableWidget(self)
        self.file_table.setColumnCount(5)  # Number of columns for details
        self.file_table.setHorizontalHeaderLabels(["#", "File Name", "Modified", "Size", "Type"])  # Set column headers
        self.file_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # Disable editing
        self.file_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.file_table.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)  # Allow multiple selection
        self.file_table.setStyleSheet("background-color: #1e1e1e; color: white; border: 1px solid #333;")
        self.file_table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #333; color: white; }")
        self.file_table.verticalHeader().setVisible(False)
        layout.addWidget(self.file_table)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()

        open_button = QtWidgets.QPushButton("Open", self)
        open_button.setObjectName("houdiniButton")
        open_button.clicked.connect(self.open_selected_files)
        button_layout.addWidget(open_button)

        delete_button = QtWidgets.QPushButton("Delete", self)
        delete_button.setObjectName("houdiniButton")
        delete_button.clicked.connect(self.confirm_delete_selected_files)
        button_layout.addWidget(delete_button)

        undo_button = QtWidgets.QPushButton("Undo Delete", self)
        undo_button.setObjectName("houdiniButton")
        undo_button.clicked.connect(self.undo_delete)
        button_layout.addWidget(undo_button)

        refresh_button = QtWidgets.QPushButton("Refresh", self)
        refresh_button.setObjectName("houdiniButton")
        refresh_button.clicked.connect(self.populate_file_table)
        button_layout.addWidget(refresh_button)

        layout.addLayout(button_layout)

        # Status bar
        self.status_bar = QtWidgets.QStatusBar(self)
        layout.addWidget(self.status_bar)

        self.populate_file_table()
        self.adjust_table_size()
          

    def check_config_directory(self):
        if not os.path.exists(self.config_directory):
            os.makedirs(self.config_directory)

    def load_directory_path(self):
        # Load the directory path from a file
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r') as f:
                saved_path = f.read().strip()
                if saved_path:
                    return saved_path
        # If config file doesn't exist or it's empty, use the default directory path
        default_path = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Temp", "houdini_temp")
        self.save_directory_path(default_path)  # Save default path to config file
        return default_path



    def save_directory_path(self, path):
        # Save the directory path to a file
        with open(self.config_file_path, 'w') as f:
            f.write(path)
            
    def change_directory_path(self):
        def modify_houdini_env(env_file_path, new_temp_path):
            try:
                with open(env_file_path, 'r') as f:
                    lines = f.readlines()
            except FileNotFoundError:
                print("Houdini environment file not found.")
                return
        
            # Check if the path already exists in the environment file
            for i, line in enumerate(lines):
                if "HOUDINI_TEMP_DIR" in line:
                    print("HOUDINI_TEMP_DIR already defined in the environment file. Modifying path.")
                    # Update the existing line with the new path
                    lines[i] = f'HOUDINI_TEMP_DIR={new_temp_path}\n'
                    break
            else:
                # If "HOUDINI_TEMP_DIR" is not found, add it to the end of the file
                lines.append(f'HOUDINI_TEMP_DIR={new_temp_path}\n')
        
            # Write the modified lines back to the environment file
            with open(env_file_path, 'w') as f:
                f.writelines(lines)
        
            print(f"Updated HOUDINI_TEMP_DIR to {new_temp_path} in Houdini environment file.")

        new_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", self.directory_path)
        if new_path:
            self.directory_path = new_path
            self.path_edit.setText(new_path)
            self.save_directory_path(new_path)
            self.populate_file_table()
            modify_houdini_env(self.env_file_path, self.directory_path)
            

    def populate_file_table(self):
        self.file_table.clearContents()
        self.file_table.setRowCount(0)

        hip_files = [file for file in os.listdir(self.directory_path) if file.endswith('.hip')]

        # Sort files by modified date in descending order (latest first)
        hip_files.sort(key=lambda x: os.path.getmtime(os.path.join(self.directory_path, x)), reverse=True)

        self.file_table.setRowCount(len(hip_files))
        self.file_names = []  # Clear previous file names

        for row, file in enumerate(hip_files):
            file_path = os.path.join(self.directory_path, file)
            file_date = QtCore.QDateTime.fromSecsSinceEpoch(os.path.getmtime(file_path))

            # Get additional file information
            file_stats = os.stat(file_path)
            file_size = file_stats.st_size
            file_type = self.get_file_type(stat.S_IFMT(file_stats.st_mode))

            # Set data in table cells
            self.file_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row + 1)))  # Serial number
            self.file_table.setItem(row, 1, QtWidgets.QTableWidgetItem(file))
            self.file_table.setItem(row, 2, QtWidgets.QTableWidgetItem(file_date.toString(QtCore.Qt.ISODate).replace('T', '  ')))
            self.file_table.setItem(row, 3, QtWidgets.QTableWidgetItem(self.format_size(file_size)))
            self.file_table.setItem(row, 4, QtWidgets.QTableWidgetItem(file_type))

            self.file_names.append(file)  # Store file name

            # Set tooltip for file name cell
            self.file_table.item(row, 1).setToolTip(file_path)

    def adjust_table_size(self):
        self.file_table.resizeColumnsToContents()
        self.file_table.resizeRowsToContents()

    def format_size(self, size):
        # Helper function to format file size in a human-readable format
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
        index = 0
        while size >= 1024 and index < len(suffixes) - 1:
            size /= 1024
            index += 1
        return "{:.2f} {}".format(size, suffixes[index])

    def get_file_type(self, file_type):
        # Helper function to get the file type description based on the file mode
        if stat.S_ISDIR(file_type):
            return "Directory"
        elif stat.S_ISREG(file_type):
            return "Regular File"
        else:
            return "Unknown"

    def open_selected_files(self):
        selected_items = self.file_table.selectedItems()
        for item in selected_items:
            file_name = item.text()
            file_row = item.row()
            file_path = os.path.join(self.directory_path, file_name)
            if os.path.isfile(file_path):
                hou.hipFile.load(file_path)

    def confirm_delete_selected_files(self):
        selected_rows = set(item.row() for item in self.file_table.selectedItems())
        if selected_rows:
            reply = QtWidgets.QMessageBox.question(self, 'Confirmation', 'Are you sure you want to delete selected file(s)?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.delete_selected_files(selected_rows)

    def delete_selected_files(self, selected_rows):
        selected_files = [self.file_names[row] for row in selected_rows]
        for file_name in selected_files:
            try:
                file_path = os.path.join(self.directory_path, file_name)
                deleted_file_path = file_path + '.deleted'
                os.rename(file_path, deleted_file_path)
                self.deleted_files.append(deleted_file_path)
                self.file_names.remove(file_name)  # Remove deleted file from the list of file names
            except Exception as e:
                print(f"Error occurred while deleting file '{file_name}': {str(e)}")

        self.populate_file_table()  # Refresh the file list to reflect the changes
        self.adjust_table_size()  # Adjust table size after deleting files
        self.status_bar.showMessage("Files deleted successfully.", 3000)  # Show message for 3 seconds


    def undo_delete(self):
        if self.deleted_files:
            for deleted_file_path in self.deleted_files:
                try:
                    restored_file_path = deleted_file_path[:-8]  # Remove the '.deleted' extension from the file path
                    os.rename(deleted_file_path, restored_file_path)
                except Exception as e:
                    hou.ui.displayMessage(f"Error occurred while restoring file '{os.path.basename(deleted_file_path)}': {str(e)}", severity=hou.severityType.Error)
            self.deleted_files.clear()  # Clear the list of deleted files after restoration
            self.populate_file_table()  # Refresh the file list to reflect the changes
            self.status_bar.showMessage("Files restored successfully.", 3000)  # Show message for 3 seconds
        else:
            hou.ui.displayMessage("No files to undo.", severity=hou.severityType.Warning)

    def filter_file_list(self):
        search_text = self.search_box.text().lower()
        for index in range(self.file_table.rowCount()):
            item = self.file_table.item(index, 1)  # File Name column
            if item:
                file_name = item.text().lower()
                if search_text in file_name:
                    self.file_table.setRowHidden(index, False)
                else:
                    self.file_table.setRowHidden(index, True)                   
                   




def onCreateInterface():
    panel = crashedFiles()
    return panel
