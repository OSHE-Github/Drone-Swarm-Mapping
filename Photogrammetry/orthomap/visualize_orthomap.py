import os
import matplotlib.pyplot as plt

try:
    import rasterio
    from rasterio.plot import show
    HAS_RASTERIO = True
except ImportError:
    HAS_RASTERIO = False
    from PIL import Image


def visualize_orthophoto(path: str):
    if not os.path.exists(path):
        print(f"Error: '{path}' does not exist.")
        return

    print(f"Loading orthophoto from: {path}")

    plt.figure(figsize=(12, 10))
    plt.title("PyODM Orthomosaic Map", fontsize=14)

    if HAS_RASTERIO:
        with rasterio.open(path) as src:
            show(src)
    else:
        img = Image.open(path)
        plt.imshow(img)
        plt.axis("off")

    plt.tight_layout()
    plt.show()