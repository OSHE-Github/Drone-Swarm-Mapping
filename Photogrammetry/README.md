# PyODM Video-to-Point Cloud Pipeline

An automated photogrammetry pipeline that extracts frame keyframes from an input drone/action video, processes them through an OpenDroneMap (**NodeODM**) Docker backend using **PyODM**, and visualizes the resulting 3D point cloud using **Open3D**.

---

## 📋 Prerequisites

### 1. System Requirements
* **CPU Virtualization**: Enabled in BIOS/UEFI (VT-x for Intel or AMD-V for AMD).
* **Python**: Version 3.8 or higher.

### 2. Windows Subsystem for Linux (WSL 2) & Docker Desktop (Windows Users)
If running on Windows, WSL 2 is required as the backend engine for Docker Desktop.

1. **Install/Update WSL 2**:
   Open PowerShell as Administrator and run:
   ```powershell
   wsl --install
   ```
   *(If WSL is already installed, update it using `wsl --update`)*.

2. **Install Docker Desktop**:
   * Download and install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/).
   * Ensure **"Use the WSL 2 based engine"** is checked during setup.
   * Start Docker Desktop and wait until the whale icon in the system tray shows **Docker Desktop is running**.

---

## ⚙️ Installation & Environment Setup

### 1. Clone or Open the Repository
Open Git Bash or terminal and navigate to your workspace directory:
```bash
git clone https://github.com/OSHE-Github/Drone-Swarm-Mapping.git
cd Drone-Swarm-Mapping
```

### 2. Create and Activate a Python Virtual Environment
**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
*(If PowerShell displays a script execution error, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` first).*

**On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python Dependencies
With your virtual environment active, install the required packages:
```bash
pip install -U pyodm opencv-python open3d "laspy[lazrs]"
```

---

## 🚀 How to Run the Pipeline

### Step 1: Start the NodeODM Docker Container
Open a terminal window and start the OpenDroneMap background server:
```bash
docker run -ti -p 3000:3000 opendronemap/nodeodm
```
*Leave this terminal window running in the background. It will listen for API calls on `localhost:3000`.*

### Step 2: Add Your Input Video
Place your target drone or survey video file (`.mp4`, `.mov`, `.avi`, or `.mkv`) inside the `./video_file/` folder:
```text
pyODM_testing/
├── video_file/
│   └── input_video.mp4   <-- Place video here
├── process.py
├── extract_frames.py
└── visualize_map.py
```

### Step 3: Run the Main Processing Script
In your active virtual environment, run:
```bash
python process.py
```

---

## 🔄 How the Pipeline Works

1. **`extract_frames.py`**: Scans `./video_file/`, extracts keyframe images at fixed intervals, and saves them into `./image_frames/`.
2. **`process.py`**: Sends the extracted frames to the running NodeODM engine on `localhost:3000`, configures processing settings (`"dsm": True`), and waits for processing to complete.
3. **Asset Download**: Downloads the processed photogrammetry assets into `./mapping_results/`.
4. **`visualize_map.py`**: Locates the generated point cloud file and renders it in an interactive 3D window.

---

## 🛠️ Troubleshooting

* **Docker Connection Error (`npipe:////./pipe/docker_engine`)**:
  * Docker Desktop is not running. Launch Docker Desktop from the Start menu and wait for it to initialize before running `process.py`.
* **PowerShell Execution Policy Error**:
  * Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` in PowerShell to enable running activation scripts.
