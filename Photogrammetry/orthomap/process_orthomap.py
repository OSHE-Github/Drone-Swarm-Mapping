import os
import sys
import glob
from pyodm import Node
from pyodm.exceptions import TaskFailedError

# Add parent directory (Photogammetry/) to path so extract_frames can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from extract_frames import extract_frames
from visualize_orthomap import visualize_orthophoto


def find_orthophoto(results_dir: str):
    """Locate an orthophoto GeoTIFF in the downloaded assets."""
    for ext in ("tif", "tiff"):
        matches = glob.glob(os.path.join(results_dir, "**", f"*.{ext}"), recursive=True)
        if matches:
            matches.sort(key=lambda p: ("orthophoto" not in os.path.basename(p).lower(), len(p)))
            return matches[0]
    return None


def run_pipeline():
    # Adjust paths relative to Photogammetry folder
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    video_dir = os.path.join(base_dir, "video_file")
    frames_dir = os.path.join(base_dir, "image_frames")
    results_dir = os.path.join(base_dir, "mapping_results_ortho")

    print("=== STAGE 1: Extracting Video Frames ===")
    image_paths = extract_frames(video_directory=video_dir, output_directory=frames_dir, frame_stride=8)

    if not image_paths:
        print("Error: No images extracted. Pipeline aborted.")
        return

    print("\n=== STAGE 2: Submitting Task to PyODM / NodeODM ===")
    node = Node("localhost", 3000)

    options = {
        # "fast-orthophoto": True,        # Skips dense 3D meshing
        "orthophoto-resolution": 2.0,   # Resolution in cm/pixel
        "feature-quality": "medium",
        "min-num-features": 4000,
    }

    print("Uploading photos and creating ODM processing task...")
    task = node.create_task(image_paths, options)
    print(f"Task created successfully. Task UUID: {task.uuid}")

    print("\nProcessing in progress on NodeODM (waiting for completion)...")
    try:
        task.wait_for_completion(
            status_callback=lambda info: print(f"  status: {info.status.name} ({info.progress}%)")
        )
    except TaskFailedError as e:
        print(f"\nTask failed: {e}")
        print("--- Last lines of task output ---")
        print("\n".join(task.output()[-30:]))
        return

    info = task.info()
    if info.status.name != "COMPLETED":
        print(f"\nTask ended with status {info.status.name}. Last error: {info.last_error}")
        print("--- Last lines of task output ---")
        print("\n".join(task.output()[-30:]))
        return

    print("\n=== STAGE 3: Downloading Orthophoto Assets ===")
    os.makedirs(results_dir, exist_ok=True)
    task.download_assets(results_dir)

    print("Downloaded files:")
    for root, _, files in os.walk(results_dir):
        for f in files:
            print("  ", os.path.join(root, f))

    ortho_path = find_orthophoto(results_dir)

    if ortho_path:
        print(f"\nFound orthophoto file at: {ortho_path}")
        print("\n=== STAGE 4: Visualizing Orthomosaic ===")
        visualize_orthophoto(ortho_path)
    else:
        print("Warning: Could not locate a .tif orthophoto file in downloaded assets.")


if __name__ == "__main__":
    run_pipeline()