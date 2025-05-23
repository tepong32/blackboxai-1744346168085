
Built by https://www.blackbox.ai

---
# Django File Manager

## Project Overview

Django File Manager is a simple web application built using the Django framework. It provides an easy-to-use interface for managing files and directories on the server, making it ideal for developers and users who need a reliable file handling solution. The project comes with essential functionalities to upload, download, and organize files effectively.

## Installation

To set up Django File Manager on your local machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd django_file_manager
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**
   Make sure to have `pip` also updated:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the application:**
   Open your web browser and navigate to `http://127.0.0.1:8000/`.

## Usage

Once the server is running, you can use the web interface to:

- Upload files to the server.
- Download files from the server.
- Organize files into directories.
- Delete or rename files as needed.

Follow the on-screen instructions to navigate through the application.

## Features

- **File Upload/Download:** Seamlessly upload and download files with a user-friendly interface.
- **File Organization:** Create, delete, and rename directories to keep your files structured.
- **Django Admin Integration:** A built-in admin interface for advanced management of the file system.

## Dependencies

The project requires the following Python libraries which can be found in the `requirements.txt` file:

- Django (version information can be specified in `requirements.txt`)

Make sure to install these dependencies to ensure the project functions correctly.

## Project Structure

The project directory is organized as follows:

```
django_file_manager/
│
├── manage.py                # Django's command-line utility for administrative tasks.
├── django_file_manager/
│   ├── __init__.py
│   ├── settings.py          # Settings and configurations for the Django project.
│   ├── urls.py              # URL declarations for the Django application.
│   ├── wsgi.py              # WSGI configuration for the project.
│   └── ...                  # Other application files, such as models, views, etc.
└── requirements.txt         # List of required Python libraries.
```

This structure adheres to the conventions used in Django applications, ensuring maintainability and scalability.

## Contributing

Contributions are welcome! Please submit a pull request for any features, bug fixes, or improvements that you would like to propose.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
Make sure to replace `<repository-url>` with the actual URL of the project's repository before sharing.

_________________________
Django File Manager application:

    User Management:

    Custom user system with storage quotas (5GB by default per user)
    Username generation in format: lastname.firstname.middleinitial
    Storage usage tracking per user
    User profiles with first name, last name, and middle initial

    File Management:

    Upload files with validation:
        Size limit of 500MB per file
        Supports specific file types:
            PDF documents
            Word documents (DOC, DOCX)
            Excel spreadsheets (XLS, XLSX)
            Images (JPEG, PNG, GIF)
            Text files
            Archives (ZIP, RAR)
    Download files
    Delete files
    Track file metadata (size, mime type, upload date)

    Folder System:

    Create folders and subfolders
    Hierarchical folder structure
    Delete folders
    Navigate through folder structure
    Unique folder names per user/parent combination

    File Sharing:

    Share files with other users
    Configurable sharing permissions (can_edit option)
    Track shared file status and sharing date
    View files shared by others
    Shared files appear in user's dashboard

    Dashboard Features:

    View all owned files and folders
    View files shared by others
    Organize files in folders
    File/folder management interface

    Security Features:

    Login required for all operations
    Permission checks for file access
    Storage quota enforcement
    File type validation
    Owner-only deletion rights
    Secure file sharing system

    Additional Features:

    Automatic file organization (files stored by date: year/month/day)
    File size tracking
    Last modified tracking
    MIME type detection and validation
    Storage quota management
    User storage usage tracking

This is a comprehensive file management system with user management, file organization, sharing capabilities, and security features built in.
