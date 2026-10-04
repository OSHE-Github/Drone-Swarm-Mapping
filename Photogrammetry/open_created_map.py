"""This file is used to open a map to visualize after it is already created"""

import os
import glob
from pyodm import Node
from pyodm.exceptions import TaskFailedError
from extract_frames import extract_frames
from visualize_map import visualize_point_cloud
from process import find_point_cloud

results_dir = "./mapping_results"
point_cloud_path = find_point_cloud(results_dir)

if point_cloud_path:
    print(f"\nFound point cloud file at: {point_cloud_path}")

    print("\n=== STAGE 4: Visualizing Point Map ===")
    visualize_point_cloud(point_cloud_path)
else:
    print("Warning: Could not locate a .laz, .las or .ply point cloud file in the downloaded assets.")