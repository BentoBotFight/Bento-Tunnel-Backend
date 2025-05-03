# Bento-Tunnel-Backend

A Python Flask service that acts as a gateway between a web client and PiTunnel (reverse SSH), enabling control of remote devices via HTTP endpoints and a web UI. The project also includes Go-based HTTP servers and a Dart example.

# Purpose

This project served as an attempt to build a low-latency remote control interface to translate user control to robot movements via reverse-ssh tunnel. The result was 0.8s latency end-to-end.
# Contact

I believe codebases are complex and hard to understand by nature, so if you would like some help with using this for your own projects, please feel free to reach out to me at tungvunguyennguyen@gmail.com.

If you wish to start your own Bentobot fight, talk to us in our Discord server: https://discord.gg/rQWPPPNMmZ

## Features

- HTTP endpoints to send commands to a remote host over SSH & tmux
- Web UI for controlling a remote RC car via directional buttons
- SSH client example using Paramiko under `ssh/main.py`
- Go server examples in `main.go`, `main2.go`, `main3.go`, `main4.go`
- Dart script example in `dart/run.dart`

## Prerequisites

- Python 3.8+
- Go 1.23+
- tmux, sshpass (or native SSH) installed
- pip dependencies listed in `requirements.txt`
- `autossh` configured for PiTunnel host

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ThomasVuNguyen/Bento-Tunnel-Backend.git
   cd Bento-Tunnel-Backend
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure `dc.py` exists in the working directory for device control scripts.
4. (Optional) Build Go servers:
   ```bash
   go build main.go
   go build main2.go
   go build main3.go
   go build main4.go
   ```

## Configuration

- Update `host`, `username`, `password`, and `port` in `main.py` or `ssh/main.py` to match your PiTunnel settings.
- Adjust tmux session name and SSH command in `main.py` to suit your environment.
- Place `cert.pem` and `key.pem` files in the project root if HTTPS is required.

## Usage

Start the Flask server:
```bash
python main.py
```

- Access the Web UI at `http://localhost:5000/` and use the buttons to control the device.
- Use curl to trigger commands directly, e.g.:
  ```bash
  curl http://localhost:5000/forward
  ```

## API Endpoints

| Route        | Method | Description                                      |
|--------------|--------|--------------------------------------------------|
| `/greet`     | POST   | Execute an arbitrary shell command (use with caution) |
| `/run`       | GET    | Start motors via tmux                            |
| `/stop`      | GET    | Stop motors                                      |
| `/left`      | GET    | Turn left                                        |
| `/right`     | GET    | Turn right                                       |
| `/forward`   | GET    | Move forward                                     |
| `/backward`  | GET    | Move backward                                    |
| `/`          | GET/POST | Render controller UI (`controller.html`)        |
| `/old`       | GET/POST | Legacy button UI                                |
| `/bet`       | GET/POST | Alternative UI (`ctrl_test.html`)               |
| `/test`      | GET    | Render test grid (`grid.html`)                   |

## Directory Structure

```
.
├── main.py            # Flask application
├── main.go            # Simple Go Hello server
├── main2.go           # Go server + tmux commands
├── main3.go           # Go server with HTML template
├── main4.go           # Go server with iframe result
├── ssh/
│   └── main.py        # Paramiko SSH example
├── dart/
│   └── run.dart       # Dart Process.run example
├── templates/         # HTML templates for Flask UI
├── requirements.txt   # Python dependencies
├── go.mod             # Go module file
├── cert.pem, key.pem  # TLS certificates
└── README.md          # Project documentation
```

## Contributing

Contributions are welcome! Please open issues or submit pull requests with clear descriptions and tests where applicable.

## License

This project is licensed under the MIT License. Feel free to add a `LICENSE` file to the root of the repository.
