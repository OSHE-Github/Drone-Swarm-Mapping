# PyODM Video-to-Map Pipeline (Point Cloud & Orthomosaic)

An automated photogrammetry pipeline that extracts frame keyframes from input drone or action camera videos, processes them through an OpenDroneMap (**NodeODM**) Docker backend using **PyODM**, and visualizes the resulting 3D point clouds and 2D orthomosaics.

---

## Prerequisites

### 1. System Requirements
- **CPU Virtualization**: Enabled in BIOS/UEFI (VT-x for Intel or AMD-V for AMD).
- **Python**: Version 3.8 or higher.

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
   * Start Docker Desktop and wait until the tray icon shows **Docker Desktop is running**.

---

## Installation & Environment Setup

### 1. Clone or Open the Repository
Open terminal/PowerShell and navigate to your workspace directory:
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
pip install -U pyodm opencv-python open3d "laspy[lazrs]" matplotlib rasterio
```

---

## Repository Structure

```text
Photogammetry/
├── video_file/               <-- Place input video files here
│   └── input_video.mp4
├── extract_frames.py         <-- Shared frame extraction module
├── process.py                <-- 3D Point cloud processing pipeline
├── visualize_map.py          <-- 3D Point cloud visualization module
├── open_created_map.py       <-- Script to open existing 3D point cloud
└── orthomap/
    ├── process_orthomap.py        <-- 2D Orthomosaic processing pipeline
    ├── visualize_orthomap.py      <-- 2D Orthomosaic visualization module
    └── open_created_orthomap.py   <-- Script to open existing 2D orthomosaic
```

---

## How to Run the Pipeline

### Step 1: Start the NodeODM Docker Container
Open a terminal window and start the OpenDroneMap background server:
```bash
docker run -ti -p 3000:3000 opendronemap/nodeodm
```
*Leave this terminal window running in the background. It listens for API calls on `localhost:3000`.*

### Step 2: Add Your Input Video
Place your drone or survey video file (`.mp4`, `.mov`, `.avi`, or `.mkv`) inside `./video_file/`.

### Step 3: Run a Processing Pipeline

* **Option A: Generate & Visualize a 3D Point Cloud**
  ```bash
  python process.py
  ```

* **Option B: Generate & Visualize a 2D Orthomosaic Map**
  ```bash
  python orthomap/process_orthomap.py
  ```

### Opening Previously Processed Maps
If a dataset has already been processed and downloaded, you can render the output directly without re-running NodeODM:

* **View 3D Point Cloud:**
  ```bash
  python open_created_map.py
  ```
* **View 2D Orthomosaic:**
  ```bash
  python orthomap/open_created_orthomap.py
  ```

---

## How the Pipeline Works

1. **`extract_frames.py`**: Scans `./video_file/`, extracts keyframe images at fixed intervals, and saves them into `./image_frames/`.
2. **Task Creation (`process.py` or `process_orthomap.py`)**: Uploads extracted frames to NodeODM (`localhost:3000`) with selected task parameters (`dsm` for point clouds, `orthophoto-resolution` for orthomosaics).
3. **Asset Download**: Downloads output assets into `./mapping_results/` (for point clouds) or `./mapping_results_ortho/` (for orthomosaics).
4. **Visualization**:
   * Point clouds (`.laz`, `.las`, `.ply`) are rendered interactively in 3D using Open3D.
   * Orthomosaics (`.tif`) are displayed using Rasterio and Matplotlib.

---

## Troubleshooting

- **Docker Connection Error (`npipe:////./pipe/docker_engine`)**:
  * Docker Desktop is not running. Launch Docker Desktop from your system menu and wait for it to initialize before running processing scripts.
- **PowerShell Execution Policy Error**:
  * Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` in PowerShell to enable running activation scripts.
- **Rasterio Installation Issues**:
  * If installing `rasterio` fails on Windows, install `Pillow` as a fallback (`pip install Pillow`), as `visualize_orthomap.py` will automatically fall back to standard image rendering.