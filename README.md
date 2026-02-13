# ISEKAI: Manga to Motion AI

## About

**ISEKAI** is a web application that transforms static manga panels into fluid, cinematic animations. It uses **RIFE (Real-Time Intermediate Flow Estimation)** AI to interpolate frames between two images, creating smooth transitions.

Designed for creators and animators, this tool leverages GPU acceleration (NVIDIA) for high-performance rendering.

## Features

*   **Number-based Sequencing:** Automatically orders uploaded images by their numbered filenames (e.g., `001.png`, `002.png`).
*   **Adjustable Smoothness:** Choose interpolation multipliers (2x, 4x, 8x, etc.) to control the fluidity of the animation.
*   **Custom FPS:** Set the output frame rate for the final video.
*   **Local Processing:** Runs entirely on your machine for privacy and speed.

## Prerequisites (Windows)

Before running the application, ensure you have the following installed:

1.  **Python 3.10+**: [Download Here](https://www.python.org/downloads/)
    *   **IMPORTANT:** During installation, check the box **"Add Python to PATH"**.
2.  **FFmpeg**: [Download Here](https://ffmpeg.org/download.html)
    *   This is required for video generation.
    *   After downloading, extract the folder and add the `bin` folder to your System Environment Variables (PATH).
    *   [Guide: How to Install FFmpeg on Windows](https://phoenixnap.com/kb/ffmpeg-windows)
3.  **NVIDIA Drivers & CUDA**:
    *   Ensure you have the latest drivers for your NVIDIA GPU.
    *   The application uses `rife-ncnn-vulkan`, which generally works out-of-the-box with recent drivers.

## How to Run

1.  **Clone or Download** this repository.
2.  **Double-click `run.bat`**.
    *   This script will automatically:
        *   Check for Python and FFmpeg.
        *   Create a virtual environment (`venv`).
        *   Install all necessary dependencies.
        *   Launch the web interface.
3.  **Open your browser**.
    *   The script will show a URL, typically `http://127.0.0.1:7860`.
    *   Click the link or copy-paste it into your browser.

## Usage

1.  **Prepare Images:**
    *   Name your manga panels in sequence (e.g., `frame_01.jpg`, `frame_02.jpg`).
    *   Ensure they are the same resolution for best results.
2.  **Upload:**
    *   Drag and drop your images into the "Upload Manga Panels" box.
3.  **Settings:**
    *   **Interpolation Multiplier:** Higher values = smoother animation but slower processing.
    *   **Output FPS:** Standard animation is often 24fps.
4.  **Animate:**
    *   Click the **Animate** button.
    *   Watch the progress in the console window.
    *   Download the generated video when complete.

## Troubleshooting

*   **"FFmpeg not found"**: The app will run in "Mock Mode" (blending images without AI) if FFmpeg is missing. Ensure `ffmpeg` command works in a new Command Prompt window.
*   **RIFE Errors**: If the AI interpolation fails (e.g., due to GPU issues), the app falls back to linear blending. Check the console window for error messages.
*   **Memory Issues**: High multipliers (8x, 16x) on high-resolution images require significant VRAM. If it crashes, try reducing the multiplier or image size.
