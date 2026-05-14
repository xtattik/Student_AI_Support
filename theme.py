from pathlib import Path
from PIL import Image
import customtkinter as ctk

# School colours — sampled from Marsden Park Anglican College logo
TEAL        = "#0D6B7A"
TEAL_HOVER  = "#0A5361"
TEAL_LIGHT  = "#1A8A9C"
SKY_BLUE    = "#47B8D4"
LIME_GREEN  = "#6DC23A"
CHARCOAL    = "#2C2C2C"
WHITE       = "#FFFFFF"
OFF_WHITE   = "#F4F7F8"

ASSETS_DIR = Path(__file__).parent / "assets"


def load_logo(size: tuple[int, int]) -> ctk.CTkImage:
    img = Image.open(ASSETS_DIR / "logo.png").convert("RGBA")
    return ctk.CTkImage(light_image=img, dark_image=img, size=size)


def load_logo_pil(size: tuple[int, int]) -> Image.Image:
    return Image.open(ASSETS_DIR / "logo.png").convert("RGBA").resize(size, Image.LANCZOS)
