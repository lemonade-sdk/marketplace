#!/usr/bin/env python3
"""
Copy and resize logos from assets repo to marketplace repo.
"""

import shutil
from pathlib import Path
from PIL import Image

# Paths
ASSETS_MARKETPLACE = Path(r"C:\work\lsdk\assets\app\marketplace")
ASSETS_PARTNER = Path(r"C:\work\lsdk\assets\partner_logos")
MARKETPLACE_APPS = Path(r"C:\work\lsdk\marketplace\apps")

# Target size
TARGET_SIZE = (128, 128)

# Mapping: app_id -> source file
LOGO_SOURCES = {
    "open-webui": ASSETS_PARTNER / "openwebui.jpg",
    "n8n": ASSETS_MARKETPLACE / "n8n.png",
    "gaia": ASSETS_MARKETPLACE / "gaia.png",
    "infinity-arcade": ASSETS_MARKETPLACE / "infinity_arcade.png",
    "continue": ASSETS_MARKETPLACE / "continue.png",
    "github-copilot": ASSETS_MARKETPLACE / "github_copilot.png",
    "openhands": ASSETS_MARKETPLACE / "openhands.png",
    "dify": ASSETS_MARKETPLACE / "dify.png",
    "deep-tutor": ASSETS_MARKETPLACE / "deep_tutor.png",
    "iterate-ai": ASSETS_MARKETPLACE / "iterate_ai.png",
    "perplexica": ASSETS_MARKETPLACE / "perplexica.png",
    "hugging-face": ASSETS_MARKETPLACE / "hugging_face.png",
    # From partner_logos
    "ai-toolkit": ASSETS_PARTNER / "ai_toolkit.png",
    "ai-dev-gallery": ASSETS_PARTNER / "ai_dev_gallery.webp",
    "anythingllm": ASSETS_PARTNER / "anything_llm.png",
    "codegpt": ASSETS_PARTNER / "codegpt.jpg",
}


def resize_image(src: Path, dst: Path, size: tuple):
    """Resize image to target size, maintaining aspect ratio with padding."""
    with Image.open(src) as img:
        # Convert to RGBA if needed
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        
        # Calculate aspect-preserving resize
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Create new image with padding if needed
        new_img = Image.new("RGBA", size, (0, 0, 0, 0))
        offset = ((size[0] - img.width) // 2, (size[1] - img.height) // 2)
        new_img.paste(img, offset)
        
        # Save as PNG
        new_img.save(dst, "PNG", optimize=True)


def main():
    for app_id, src_path in LOGO_SOURCES.items():
        dst_dir = MARKETPLACE_APPS / app_id
        dst_path = dst_dir / "logo.png"
        
        if not src_path.exists():
            print(f"[WARN] Source not found: {src_path}")
            continue
        
        if not dst_dir.exists():
            print(f"[WARN] App dir not found: {dst_dir}")
            continue
        
        try:
            resize_image(src_path, dst_path, TARGET_SIZE)
            print(f"[OK] {app_id}: {src_path.name} -> logo.png")
        except Exception as e:
            print(f"[ERROR] {app_id}: {e}")


if __name__ == "__main__":
    main()
