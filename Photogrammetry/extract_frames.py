import glob
import os
import cv2


def extract_frames(video_directory: str = "./video_file", output_directory: str = "./image_frames", frame_stride: int = 15):
    """
    Extracts frame images from a video file at a fixed interval.
    :param frame_stride: Extract every Nth frame (e.g., 15 = 2 frames/sec for 30fps video).
    """
    os.makedirs(output_directory, exist_ok=True)

    # Find the video file inside video_directory
    video_extensions = ("*.mp4", "*.mov", "*.avi", "*.mkv")
    video_files = []
    for ext in video_extensions:
        video_files.extend(glob.glob(os.path.join(video_directory, ext)))

    if not video_files:
        raise FileNotFoundError(f"No video file found in '{video_directory}'. Please place a video there.")

    video_path = video_files[0]
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise RuntimeError(f"Failed to open video file: {video_path}")

    print(f"Extracting frames from '{os.path.basename(video_path)}'...")
    
    frame_idx = 0
    saved_count = 0
    extracted_paths = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % frame_stride == 0:
            frame_name = f"frame_{saved_count:04d}.jpg"
            out_path = os.path.join(output_directory, frame_name)
            cv2.imwrite(out_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
            extracted_paths.append(out_path)
            saved_count += 1

        frame_idx += 1

    cap.release()
    print(f"Extracted {saved_count} photos to '{output_directory}'.")
    return extracted_paths