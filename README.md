# Venom Console

<img width="854" height="100" alt="ascii-art-text" src="https://github.com/user-attachments/assets/887af14f-9f1e-4baf-a6d6-f728a94304f4" />

(windows only)

A powerful Windows console tool with system management, networking, file operations, utilities, and AI chatbot capabilities.

## Features

- **System Management**: System info, uptime, processes, storage, battery status
- **Networking**: Ping, traceroute, network info, WiFi, speedtest, DNS management
- **File Operations**: Copy, move, delete, search, compress, extract files
- **Utilities**: Timer, clock, calculator, text-to-speech, hex dump
- **AI Chatbot**: Interactive chat with MiniMax AI via Hugging Face

## Requirements

- Python 3.13 or higher
- Windows OS (primary target, may work on Linux/Mac with limitations)

## Installation

1. Download the latest release from the [GitHub Releases](https://github.com/yourusername/venom/releases) page
2. Extract the zip file to a folder of your choice
3. Ensure Python 3.13+ is installed
4. Run the console - no additional setup required!

**Note:** You don't need to download `.gitignore` or any other Git-related files - they're included in the release but aren't required to run the application.

## Configuration

### AI Chatbot

The AI chatbot feature uses a shared API key that's included with the project. **No setup required!** Just run the `chatbot` command and start chatting.

## Usage

Run the console:

```bash
python "venom_console .py"
```

Or on Windows, you can double-click the file.

### Available Commands

Type `help` in the console to see all available commands, or use `explain <command>` for detailed information about a specific command.

#### Command Categories:

- **Core**: `help`, `cls`, `exit`, `version`, `about`
- **System**: `sysinfo`, `uptime`, `whoami`, `processes`, `kill`, `storage`, `battery`
- **Network**: `ping`, `tracert`, `netinfo`, `myip`, `wifi`, `speedtest`, `dnsflush`
- **Files**: `ls`, `cd`, `cat`, `copy`, `del`, `rename`, `find`, `search`, `compress`, `extract`
- **Utilities**: `calc`, `time`, `date`, `timer`, `clock`, `say`, `typewriter`
- **AI**: `chatbot` - Start interactive AI chat session

### Example Usage

```bash
# Check system info
sysinfo

# Ping a host
ping google.com

# List files
ls

# Start AI chatbot
chatbot

# In chatbot mode, you can run console commands with:
venom.console ls
```

## Project Structure

```
venom/
├── venom_console .py      # Main console application
├── extra/                  # Additional utilities
│   ├── apikeytest.py      # API key testing script
│   └── ...                # Other utility scripts
├── README.md              # This file
└── .env.example           # Example environment file
```

## Contributing

This is an open source project. Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Security Notes

- The project includes a shared API key for the AI chatbot feature
- The key is encoded in the source code for basic obfuscation
- All users share the same API key for convenience

## License

[Add your license here - e.g., MIT, GPL, etc.]

## Troubleshooting

### AI Chatbot not working

- Check that you have internet connectivity
- Verify the API key in the code is valid
- Make sure your Hugging Face token has the necessary permissions

### Commands not working

- Some commands require administrator privileges on Windows
- Network commands require active internet connection
- File operations require appropriate file system permissions

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

