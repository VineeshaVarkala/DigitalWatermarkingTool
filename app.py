from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


@app.route("/", methods=["GET", "POST"])
def index():
    error = None

    if request.method == "POST":
        file = request.files.get("image")
        watermark = request.form.get("watermark", "").strip()
        position = request.form.get("position", "bottom-right")
        opacity = request.form.get("opacity", "150")

        if not file or not file.filename:
            error = "Please choose an image."
        elif "." not in file.filename or file.filename.rsplit(".", 1)[1].lower() not in ALLOWED_EXTENSIONS:
            error = "Upload a PNG, JPG, JPEG, or WEBP image."
        elif not watermark:
            error = "Please enter watermark text."
        else:
            try:
                opacity = max(30, min(255, int(opacity)))
                image = Image.open(file.stream).convert("RGBA")
                width, height = image.size

                overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
                draw = ImageDraw.Draw(overlay)

                font_size = max(16, width // 25)
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except OSError:
                    font = ImageFont.load_default(size=font_size)

                bbox = draw.textbbox((0, 0), watermark, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                margin = max(10, width // 40)

                positions = {
                    "top-left": (margin, margin),
                    "top-right": (width - text_width - margin, margin),
                    "bottom-left": (margin, height - text_height - margin),
                    "bottom-right": (
                        width - text_width - margin,
                        height - text_height - margin,
                    ),
                    "center": (
                        (width - text_width) // 2,
                        (height - text_height) // 2,
                    ),
                }

                x, y = positions.get(position, positions["bottom-right"])
                draw.text((x, y), watermark, font=font, fill=(255, 255, 255, opacity))

                result = Image.alpha_composite(image, overlay).convert("RGB")
                output = BytesIO()
                result.save(output, format="PNG")
                output.seek(0)

                return send_file(
                    output,
                    mimetype="image/png",
                    as_attachment=True,
                    download_name="watermarked_image.png",
                )

            except Exception:
                error = "Unable to process this image. Please try another file."

    return render_template("index.html", error=error)


@app.errorhandler(413)
def file_too_large(error):
    return "Image is too large. Please upload an image under 10 MB.", 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
