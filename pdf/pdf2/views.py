from django.shortcuts import render
from django.http import HttpResponse
import img2pdf
from PIL import Image
import io

A4_WIDTH = 2480
A4_HEIGHT = 3508

def home(request):
    if request.method == "POST":
        images = request.FILES.getlist("images")

        if not images:
            return render(request, "upload.html")

        pdf_images = []

        for img_file in images:
            img = Image.open(img_file).convert("RGB")

            # Resize while keeping aspect ratio
            img.thumbnail((A4_WIDTH, A4_HEIGHT))

            # Create white A4 background
            background = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")

            # Center image
            x = (A4_WIDTH - img.width) // 2
            y = (A4_HEIGHT - img.height) // 2
            background.paste(img, (x, y))

            img_bytes = io.BytesIO()
            background.save(img_bytes, format="JPEG", quality=95)
            pdf_images.append(img_bytes.getvalue())

        pdf_bytes = img2pdf.convert(pdf_images)

        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="images.pdf"'
        return response

    return render(request, "upload.html")
