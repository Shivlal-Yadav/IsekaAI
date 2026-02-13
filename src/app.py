import gradio as gr
import os
import shutil
# Add current directory to path to allow importing processor
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from processor import MangaAnimator
except ImportError:
    # Fallback if running from root
    from src.processor import MangaAnimator

# Initialize Animator
animator = MangaAnimator(mock_mode=False)

def animate_manga(files, multiplier, fps):
    if not files:
        raise gr.Error("Please upload images.")

    # Process video
    try:
        # Pass output_path=None to generate a unique temporary file
        processed_video = animator.process_video(files, output_path=None, multiplier=int(multiplier), fps=int(fps))
        return processed_video
    except Exception as e:
        raise gr.Error(f"Error: {str(e)}")

css = """
body { background-color: #1a1a1a; color: #ffffff; }
"""

with gr.Blocks(title="ISEKAI: Manga to Motion AI", css=css, theme=gr.themes.Monochrome()) as demo:
    gr.Markdown("# ISEKAI: Manga to Motion AI")
    gr.Markdown("Upload your manga panels (numbered filenames) to generate a fluid animation using RIFE interpolation.")

    with gr.Row():
        with gr.Column():
            files = gr.File(file_count="multiple", label="Upload Manga Panels (Images)", file_types=["image"])
            multiplier = gr.Slider(minimum=2, maximum=16, step=2, value=2, label="Interpolation Multiplier (Smoothness)")
            fps = gr.Slider(minimum=12, maximum=60, step=1, value=24, label="Output FPS")
            btn = gr.Button("Animate", variant="primary")

        with gr.Column():
            video_out = gr.Video(label="Generated Animation")

    btn.click(animate_manga, inputs=[files, multiplier, fps], outputs=video_out)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
