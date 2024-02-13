
# HOUDINI CRASHED FILES

This Python panel for Houdini manages crashed files. It allows users to view, open, delete, and undo delete operations on crashed Houdini files. The panel provides functionalities to change the temporary directory path, search for specific files, and display file details such as name, modified date, size, and type. It also ensures the consistency of the Houdini environment by updating the environment file when the temporary directory path is changed. The panel is designed using PySide2 for the user interface and integrates seamlessly with Houdini's scripting environment.

![image](https://github.com/Pahaadi7/Houdini-Crashed-Files-Panel/assets/132155993/be841602-37f0-4c4d-91be-0bca0ef491d0)

Step-by-step guide to installing and launching the crashed files management Python panel in Houdini:

1. **Open Houdini:**
   - Launch Houdini application on your system.

2. **Navigate to Python Panel:**
   - Once Houdini is open, navigate to the Python Panel.

   ![image](https://github.com/Pahaadi7/Houdini-Crashed-Files-Panel/assets/132155993/57124616-28f3-441b-aa0d-92dc53ffce03)

3. **Navigate to Gear Icon:**
   - After the Python Panel is opened, go to the right side of the panel.
   - Locate and click on the gear icon to access additional options.
    ![image](https://github.com/Pahaadi7/Houdini-Crashed-Files-Panel/assets/132155993/357abe2c-47cf-4b78-90b1-8394798d994f)


4. **Create a New Interface:**
   - In the options menu, click on `New Interface`.
   - This will create a new blank interface within the Python Panel.

   ![image](https://github.com/Pahaadi7/Houdini-Crashed-Files-Panel/assets/132155993/723db213-21e2-4bba-8815-4a36dc9f1da3)

5. **Paste Python Code:**
   - Copy the provided Python code for the crashed files management panel.
   - Return to the Houdini Python Panel.
   - Paste the copied Python code into the newly created interface.

   ![image](https://github.com/Pahaadi7/Houdini-Crashed-Files-Panel/assets/132155993/1920508e-74d0-428b-bf22-c07e4f2a31af)


6. **Navigating the Panel:**
   - The panel displays a list of crashed files along with their details such as name, modified date, size, and type.
   - The panel also provides options to search for specific files, open selected files, delete selected files, and undo delete operations.

7. **Changing the Temporary Directory Path:**
   - Click on the "Change" button next to the "Temp Directory Path" label.
   - Choose a new directory path using the file dialog that appears.
   - Click "OK" to confirm the selection.

8. **Searching for Files:**
   - Enter the desired search query in the search box provided.
   - The file list will be filtered in real-time to display only the files matching the search query.

9. **Managing Files:**
   - Select one or more files from the list by clicking on them.
   - Use the "Open" button to open the selected files in Houdini.
   - Use the "Delete" button to permanently delete the selected files. A confirmation dialog will appear before deletion.
   - Use the "Undo Delete" button to restore previously deleted files.

10. **Status Messages:**
   - Status messages will appear at the bottom of the panel to indicate the success or failure of operations such as file deletion and restoration.

11. **Adjusting Panel Size:**
   - The panel's size can be adjusted by resizing the Houdini window or dragging the panel's edges.

12. **Exiting the Panel:**
    - Close the panel by clicking the "X" button on the panel's title bar or using the standard window close functionality.

By following these steps, you can effectively use the crashed files management Python panel in Houdini to organize and manage your crashed files efficiently.
