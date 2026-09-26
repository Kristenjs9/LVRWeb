"""Generate the printable Sick Calf Exam QR code (PNG + barn-card PDF).

Points at the permanent public URL, with the LVR logo centered and high error
correction (H) so the logo overlay stays scannable. Run from anywhere:

    python qr/make_qr.py

Requires: pip install qrcode pillow
Outputs (into this qr/ folder): sick_calf_qr.png, sick_calf_qr_card.pdf, sick_calf_qr_card.png
"""
import os
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
URL = "https://livestockveterinaryresources.com/health_records/sick_calf"
LOGO = os.path.join(HERE, "LVRlogo.jpg")

DARK = (28, 28, 26)      # near-black modules, max contrast for scanning
GREEN = (29, 110, 86)    # (kept for reference; card uses navy below)
NAVY = (13, 34, 64)      # LVR brand navy
WHITE = (255, 255, 255)

# ---------- 1. Build the QR (ECC High) ----------
qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=40, border=4)
qr.add_data(URL)
qr.make(fit=True)
qr_img = qr.make_image(fill_color=DARK, back_color=WHITE).convert("RGBA")
qw, qh = qr_img.size

# ---------- 2. Overlay logo in center (~20% of QR width) ----------
logo = Image.open(LOGO).convert("RGBA")
target = int(qw * 0.20)
lr = logo.width / logo.height
if lr >= 1:
    lw, lh = target, int(target / lr)
else:
    lw, lh = int(target * lr), target
logo = logo.resize((lw, lh), Image.LANCZOS)

pad = int(target * 0.14)
pw, ph = lw + pad * 2, lh + pad * 2
plate = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
pd = ImageDraw.Draw(plate)
pd.rounded_rectangle([0, 0, pw - 1, ph - 1], radius=int(pad * 1.6), fill=WHITE)
plate.paste(logo, (pad, pad), logo)
qr_img.alpha_composite(plate, ((qw - pw) // 2, (qh - ph) // 2))

qr_png = qr_img.convert("RGB")
png_path = os.path.join(HERE, "sick_calf_qr.png")
qr_png.save(png_path, "PNG", dpi=(600, 600))
print("QR px:", qr_png.size, "->", png_path)

# ---------- 3. Barn-card / hutch-sign PDF (5x7 in @ 300 dpi) ----------
DPI = 300
CW, CH = 5 * DPI, 7 * DPI

def font(paths, size):
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

BOLD = [r"C:\Windows\Fonts\arialbd.ttf"]
REG = [r"C:\Windows\Fonts\arial.ttf"]
f_title = font(BOLD, 150)
f_sub = font(REG, 62)
f_url = font(REG, 40)
f_brand = font(BOLD, 46)

card = Image.new("RGB", (CW, CH), WHITE)
d = ImageDraw.Draw(card)

def centered(text, f, y, fill):
    bb = d.textbbox((0, 0), text, font=f)
    d.text(((CW - (bb[2] - bb[0])) // 2, y), text, font=f, fill=fill)
    return y + (bb[3] - bb[1])

band_h = 300
d.rectangle([0, 0, CW, band_h], fill=NAVY)
bb = d.textbbox((0, 0), "SICK CALF EXAM", font=f_title)
d.text(((CW - (bb[2] - bb[0])) // 2, (band_h - (bb[3] - bb[1])) // 2 - bb[1]),
       "SICK CALF EXAM", font=f_title, fill=WHITE)

y = band_h + 70
y = centered("Scan with your phone camera", f_sub, y, DARK) + 40

qr_box = 980
qr_for_card = qr_png.resize((qr_box, qr_box), Image.LANCZOS)
qx = (CW - qr_box) // 2
qy = y + 20
card.paste(qr_for_card, (qx, qy))
d.rectangle([qx - 6, qy - 6, qx + qr_box + 6, qy + qr_box + 6], outline=(221, 217, 208), width=4)

centered("livestockveterinaryresources.com/health_records/sick_calf", f_url, qy + qr_box + 60, (107, 106, 100))
centered("Livestock Veterinary Resources, LLC", f_brand, CH - 150, NAVY)

pdf_path = os.path.join(HERE, "sick_calf_qr_card.pdf")
card.save(pdf_path, "PDF", resolution=DPI)
card.save(os.path.join(HERE, "sick_calf_qr_card.png"), "PNG", dpi=(DPI, DPI))
print("Card ->", pdf_path)
