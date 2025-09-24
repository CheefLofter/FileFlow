# Local File Sharing Server

A lightweight file sharing server built with Python and Flask. This application allows you to easily upload, download, and manage files over your local network.

## Features

- **File Upload:** Drag & drop files to instantly upload them.
- **File Download:** Access and download shared files from any device on your network.
- **File Deletion:** Remove files with a simple click.
- **Automatic Cleanup:** The shared folder is automatically cleared when the server exits.
- **Real-Time Updates:** The page auto-refreshes every 30 seconds when idle.

## Technologies Used

- **Python:** The core programming language.
- **Flask:** A micro web framework that powers the server.
- **Werkzeug:** For secure file handling with the `secure_filename` function.
- **Tailwind CSS:** Provides sleek and responsive UI styles in the frontend.
- **Humanize:** Transforms file sizes and timestamps into human-readable formats.
- **JavaScript (Vanilla):** Handles file uploads with progress indication and drag & drop support.

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
