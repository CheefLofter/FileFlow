# FileFlow - Local Network File Sharing

![FileFlow Banner](resources/image.png)

FileFlow is a lightning-fast file sharing solution for local networks. It is similar to Google quick share or apple airdrop but works on any device with a web browser and any dvide on same network can access the shared files.

## FileFlow features

- 🚀  Running in seconds, no configuration needed
- 🔒  Your files never leave your network
- 💫  Clean, responsive design that just works
- 🎯  Simple Drag & drop, progress tracking, which does nothing more than needed

## Quick Start

```bash
git clone https://github.com/RavneetGrewal2911/FileFlow.git
cd FileFlow
pip install -r requirements.txt
python app.py
```

Then open `http://localhost:8080` in your browser. That's it!

## Features in Detail

### Smart File Management
- Drag & drop multiple files
- Real-time upload progress
- Automatic file cleanup on server shutdown
- File type filtering and size limits

### Network Accessibility
- Access from any device on your network
- No internet connection required
- Configurable port and host settings
- Auto-discovery of server IP (coming soon)

### Security First
- Local network isolation
- File sanitization
- Configurable access controls
- Session management

## Tech Stack

- Backend: Python + Flask
- Frontend: Vanilla JS + Tailwind CSS
- File Processing: Werkzeug
- Development: Poetry for dependency management

## Development Setup

1. Install Python 3.8 or newer
2. Clone the repository
3. Set up your environment:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. Start the development server:

```bash
python app.py
```


## Contributing

We welcome contributions! 

## License

Released under MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">
Made with ❤️ by Cheef
</div>
