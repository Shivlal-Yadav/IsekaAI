import sys
import os
import cv2
import numpy as np
import shutil
from pathlib import Path

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from processor import MangaAnimator

def test_pipeline():
    # Setup
    input_dir = Path("test_input")
    if input_dir.exists():
        shutil.rmtree(input_dir)
    input_dir.mkdir()

    # Create dummy images
    img1 = np.zeros((100, 100, 3), dtype=np.uint8)
    img1[:, :] = [0, 0, 255] # Red
    img2 = np.zeros((100, 100, 3), dtype=np.uint8)
    img2[:, :] = [255, 0, 0] # Blue

    # Use numbered filenames
    f1 = str(input_dir / "001.png")
    f2 = str(input_dir / "002.png")
    cv2.imwrite(f1, img1)
    cv2.imwrite(f2, img2)

    # Initialize animator in mock mode
    animator = MangaAnimator(mock_mode=True)

    print("Starting pipeline test...")

    output_video = "test_output.mp4"
    if os.path.exists(output_video):
        os.remove(output_video)

    try:
        # Test 1: Specific output path
        files = [f2, f1] # Reverse order to test sort
        res_path = animator.process_video(files, output_path=output_video, multiplier=4, fps=10)
        print(f"Test 1 Result Path: {res_path}")

        if os.path.exists(output_video) and res_path == output_video:
             print("Test 1 Passed: Output path respected.")
        else:
             print("Test 1 Failed.")

        # Test 2: Auto temp path
        res_path_auto = animator.process_video(files, output_path=None, multiplier=2, fps=10)
        print(f"Test 2 Result Path: {res_path_auto}")
        if os.path.exists(res_path_auto):
            print("Test 2 Passed: Auto temp file created.")
            # Cleanup auto file
            os.remove(res_path_auto)
        else:
            print("Test 2 Failed.")

    except Exception as e:
        print(f"Test Failed with exception: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        if input_dir.exists():
            shutil.rmtree(input_dir)
        if os.path.exists(output_video):
            os.remove(output_video)

if __name__ == "__main__":
    test_pipeline()
