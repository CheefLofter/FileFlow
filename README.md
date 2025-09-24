# Local File Sharing Server

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-brightgreen.svg)](https://flask.palletsprojects.com/)

![Application Screenshot](files/image.png)

A lightweight and professional file sharing server built with Python and Flask. Easily upload, download, and manage files over your local network with an intuitive interface and real-time updates.

## Features

- **Modern UI:** Sleek design using Tailwind CSS with a professional color scheme.
- **File Upload:** Drag & drop support and progress indication for a seamless experience.
- **File Download:** Easy one-click downloads from any device on your network.
- **File Deletion:** Remove unwanted files quickly.
- **Automatic Cleanup:** Shared folder is cleared automatically when the server exits.
- **Real-Time Updates:** The page auto-refreshes every 30 seconds when idle.

## Technologies Used

- **Python:** Core programming language powering the server.
- **Flask:** A micro web framework that powers the backend.
- **Werkzeug:** Ensures secure file handling using [`secure_filename`](https://werkzeug.palletsprojects.com/en/2.0.x/utils/#werkzeug.utils.secure_filename).
- **Tailwind CSS:** Delivers a modern, responsive, and customizable UI.
- **Humanize:** Converts byte sizes and timestamps into human-readable strings.
- **JavaScript (Vanilla):** Manages dynamic file uploads complete with progress tracking.

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/local-file-sharing-server.git
   ```
2. **Navigate into the project directory:**
   ```sh
   cd local-file-sharing-server
   ```
3. **Install the required packages:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Run the server:**
   ```sh
   python app.py
   ```
5. **Access the application:**
   Open your web browser and go to `http://localhost:5000` to start using the file sharing server.

## Usage

- **Uploading Files:** Simply drag and drop files into the designated area on the web page, or click to browse and select files.
- **Downloading Files:** Click on the file name or download button next to the file you wish to download.
- **Deleting Files:** Click the delete button next to the file you want to remove from the server.

## Contributing

Contributions are welcome! If you have suggestions or improvements, please submit a pull request or open an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Inspired by the need for a simple and efficient local file sharing solution.
- Thanks to the contributors and open-source community for their valuable tools and libraries.
