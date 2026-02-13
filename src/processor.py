import os
import cv2
import numpy as np
import subprocess
import shutil
import math
import re
import tempfile
from pathlib import Path

# Try importing RIFE
try:
    from rife_ncnn_vulkan_python import Rife
    HAS_RIFE = True
except ImportError:
    HAS_RIFE = False

class MangaAnimator:
    def __init__(self, gpuid=0, mock_mode=False):
        """
        Initialize the MangaAnimator.

        Args:
            gpuid (int): GPU ID to use for RIFE.
            mock_mode (bool): If True, use simple blending instead of RIFE.
        """
        self.mock_mode = mock_mode
        self.rife = None

        if not self.mock_mode:
            if HAS_RIFE:
                try:
                    # Initialize RIFE
                    # Note: Depending on the specific version of the wrapper,
                    # arguments might vary. We assume standard usage.
                    self.rife = Rife(gpuid=gpuid)
                except Exception as e:
                    print(f"Failed to initialize RIFE: {e}")
                    print("Falling back to MOCK mode.")
                    self.mock_mode = True
            else:
                print("RIFE not installed. Falling back to MOCK mode.")
                self.mock_mode = True

    def natural_sort_key(self, s):
        """
        Sorts strings with embedded numbers naturally.
        e.g., ["img1.png", "img2.png", "img10.png"] instead of ["img1.png", "img10.png", "img2.png"]
        """
        return [int(text) if text.isdigit() else text.lower()
                for text in re.split('([0-9]+)', str(s))]

    def load_images(self, image_paths):
        """
        Loads images from the provided paths, sorting them naturally.
        """
        if not image_paths:
            return []

        # Sort paths naturally based on filename
        sorted_paths = sorted(image_paths, key=lambda p: self.natural_sort_key(os.path.basename(p)))

        images = []
        for p in sorted_paths:
            img = cv2.imread(str(p))
            if img is not None:
                images.append(img)
            else:
                print(f"Warning: Could not read image {p}")
        return images

    def interpolate_segment(self, img1, img2, multiplier):
        """
        Generates intermediate frames between img1 and img2.
        multiplier must be a power of 2 (2, 4, 8, ...).
        Returns a list of frames: [img1, ...intermediates..., img2]
        """
        # Ensure multiplier is at least 1
        if multiplier < 1:
            multiplier = 1

        if multiplier == 1:
            return [img1, img2]

        if self.mock_mode:
            # Simple linear blending
            frames = [img1]
            for i in range(1, multiplier):
                alpha = i / multiplier
                blended = cv2.addWeighted(img1, 1 - alpha, img2, alpha, 0)
                frames.append(blended)
            frames.append(img2)
            return frames

        # RIFE Logic
        frames = [img1, img2]

        # Calculate number of passes needed
        passes = int(math.log2(multiplier))

        for _ in range(passes):
            new_frames = []
            for i in range(len(frames) - 1):
                f0 = frames[i]
                f1 = frames[i+1]

                # RIFE process
                try:
                    # process usually returns the middle frame
                    mid = self.rife.process(f0, f1)
                except Exception as e:
                    print(f"RIFE processing error: {e}")
                    # Fallback to blend if RIFE fails for a frame
                    mid = cv2.addWeighted(f0, 0.5, f1, 0.5, 0)

                new_frames.append(f0)
                new_frames.append(mid)
            new_frames.append(frames[-1])
            frames = new_frames

        return frames

    def process_video(self, input_paths, output_path=None, multiplier=2, fps=24):
        """
        Main processing function.
        If output_path is None, generates a temporary file path.
        Returns the path to the generated video.
        """
        # Ensure multiplier is a power of 2
        if multiplier < 1: multiplier = 1
        # Round to nearest power of 2
        multiplier = 2 ** round(math.log2(multiplier)) if multiplier > 1 else 1

        images = self.load_images(input_paths)
        if len(images) < 2:
            raise ValueError("Need at least 2 images to animate.")

        print(f"Loaded {len(images)} images. Processing with {multiplier}x interpolation...")

        all_frames = []

        # Process segments
        for i in range(len(images) - 1):
            img1 = images[i]
            img2 = images[i+1]

            # Get segment frames [img1, ..., img2]
            segment = self.interpolate_segment(img1, img2, multiplier)

            # If this is not the first segment, remove the first frame (img1)
            # because it was the last frame of the previous segment.
            if i > 0:
                segment = segment[1:]

            all_frames.extend(segment)

        print(f"Generated {len(all_frames)} frames.")

        # Generate output path if not provided
        if output_path is None:
            fd, output_path = tempfile.mkstemp(suffix='.mp4')
            os.close(fd)

        # Use a temporary directory for frames
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            frame_pattern = str(temp_dir_path / "frame_%06d.png")

            for idx, frame in enumerate(all_frames):
                cv2.imwrite(str(temp_dir_path / f"frame_{idx:06d}.png"), frame)

            # Run FFmpeg
            ffmpeg_cmd = "ffmpeg"
            if not shutil.which(ffmpeg_cmd):
                print("FFmpeg not found. Cannot generate MP4.")
                if self.mock_mode:
                     print("Creating dummy video file for mock mode.")
                     with open(output_path, 'wb') as f:
                         f.write(b'dummy video content')
                     return output_path
                else:
                    raise RuntimeError("FFmpeg not found. Please install FFmpeg.")

            # Remove existing output if any (though mkstemp creates one, ffmpeg overwrites with -y)
            if os.path.exists(output_path):
                # We need to overwrite
                pass

            cmd = [
                ffmpeg_cmd,
                "-y",
                "-framerate", str(fps),
                "-i", frame_pattern,
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-crf", "17", # High quality
                "-preset", "slow",
                output_path
            ]

            print(f"Executing FFmpeg: {' '.join(cmd)}")
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                print(f"FFmpeg failed: {e.stderr.decode()}")
                raise RuntimeError("FFmpeg video generation failed.")

        return output_path
