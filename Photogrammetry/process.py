import os
import glob
from pyodm import Node
from pyodm.exceptions import TaskFailedError
from extract_frames import extract_frames
from visualize_map import visualize_point_cloud


def find_point_cloud(results_dir: str):
    """Look for a point cloud in the downloaded assets, preferring LAZ/LAS (ODM's default output)."""
    for ext in ("laz", "las", "ply"):
        matches = glob.glob(os.path.join(results_dir, "**", f"*.{ext}"), recursive=True)
        # Skip anything that isn't the main point cloud if possible
        if matches:
            matches.sort(key=lambda p: ("georeferenced_model" not in p, len(p)))
            return matches[0]
    return None


def run_pipeline():
    video_dir = "./video_file"
    frames_dir = "./image_frames"
    results_dir = "./mapping_results"

    print("=== STAGE 1: Extracting Video Frames ===")
    image_paths = extract_frames(video_directory=video_dir, output_directory=frames_dir, frame_stride=8)

    if not image_paths:
        print("Error: No images extracted. Pipeline aborted.")
        return

    print("\n=== STAGE 2: Submitting Task to PyODM / NodeODM ===")
    # Connects to your local NodeODM container running in Docker
    node = Node("localhost", 3000)

    # Only valid ODM options. ODM writes the dense point cloud as .laz by default.
    options = {
        "dsm": True,
        "pc-quality": "medium",
        "feature-quality": "high",
        "min-num-features": 8000,
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

    # wait_for_completion returning is not proof of success, so check explicitly
    info = task.info()
    if info.status.name != "COMPLETED":
        print(f"\nTask ended with status {info.status.name}. Last error: {info.last_error}")
        print("--- Last lines of task output ---")
        print("\n".join(task.output()[-30:]))
        return

    print("\n=== STAGE 3: Downloading Point Cloud Assets ===")
    os.makedirs(results_dir, exist_ok=True)
    task.download_assets(results_dir)

    # List everything that was downloaded (helps debugging)
    print("Downloaded files:")
    for root, _, files in os.walk(results_dir):
        for f in files:
            print("  ", os.path.join(root, f))

    point_cloud_path = find_point_cloud(results_dir)

    if point_cloud_path:
        print(f"\nFound point cloud file at: {point_cloud_path}")

        print("\n=== STAGE 4: Visualizing Point Map ===")
        visualize_point_cloud(point_cloud_path)
    else:
        print("Warning: Could not locate a .laz, .las or .ply point cloud file in the downloaded assets.")


if __name__ == "__main__":
    run_pipeline()