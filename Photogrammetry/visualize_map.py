import os
import numpy as np
import laspy
import open3d as o3d


def load_laz_as_pcd(path: str) -> o3d.geometry.PointCloud:
    las = laspy.read(path)
    pts = np.vstack((las.x, las.y, las.z)).T
    pts -= pts.mean(axis=0)  # recenter; avoids float issues with large coords

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pts)

    if all(d in las.point_format.dimension_names for d in ("red", "green", "blue")):
        rgb = np.vstack((las.red, las.green, las.blue)).T.astype(np.float64)
        rgb /= 65535.0 if rgb.max() > 255 else 255.0
        pcd.colors = o3d.utility.Vector3dVector(rgb)
    return pcd


def visualize_point_cloud(path: str):
    if not os.path.exists(path):
        print(f"Error: '{path}' does not exist.")
        return

    pcd = load_laz_as_pcd(path) if path.lower().endswith((".laz", ".las")) \
        else o3d.io.read_point_cloud(path)

    if pcd.is_empty():
        print("Error: Loaded point cloud is empty.")
        return

    print(f"Loaded {len(pcd.points)} points.")
    o3d.io.write_point_cloud(os.path.splitext(path)[0] + ".ply", pcd)  # optional PLY export
    o3d.visualization.draw_geometries([pcd], window_name="PyODM Point Cloud Map")