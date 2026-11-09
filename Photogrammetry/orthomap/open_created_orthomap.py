"""This file opens and visualizes an existing orthomosaic after creation."""

import os
from visualize_orthomap import visualize_orthophoto
from process_orthomap import find_orthophoto

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
results_dir = os.path.join(base_dir, "mapping_results_ortho")
ortho_path = find_orthophoto(results_dir)

if ortho_path:
    print(f"\nFound orthophoto file at: {ortho_path}")
    print("\n=== STAGE 4: Visualizing Orthomosaic ===")
    visualize_orthophoto(ortho_path)
else:
    print(f"Warning: Could not locate a .tif orthophoto file in '{results_dir}'.")