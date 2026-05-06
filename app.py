from flask import Flask, render_template, request, send_file
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFilter
import io
import os
import random

app = Flask(__name__)

STYLES = {
    'classic': 'Classic Square',
    'rounded': 'Rounded Dots',
    'circles': 'Circles',
    'gradient_blue': 'Blue Gradient',
    'gradient_purple': 'Purple Gradient',
    'gradient_sunset': 'Sunset Gradient',
    'gradient_forest': 'Forest Gradient',
    'gradient_ocean': 'Ocean Gradient',
    'neon_green': 'Neon Green',
    'neon_pink': 'Neon Pink',
    'neon_cyan': 'Neon Cyan',
    'retro': 'Retro Vintage',
    'minimalist': 'Minimalist',
    'golden': 'Golden Luxury',
    'matrix': 'Matrix Style',
    'pixel_art': 'Pixel Art',
}

ERROR_LEVELS = {
    'L': ERROR_CORRECT_L,
    'M': ERROR_CORRECT_M,
    'Q': ERROR_CORRECT_Q,
    'H': ERROR_CORRECT_H,
}


def create_classic_qr(data, fill_color='black', back_color='white', box_size=10, border=4, error_correction=ERROR_CORRECT_M):
    qr = qrcode.QRCode(version=1, error_correction=error_correction, box_size=box_size, border=border)
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGB')


def create_rounded_qr(data, fill_color='black', back_color='white', box_size=10, border=4, error_correction=ERROR_CORRECT_M):
    qr = qrcode.QRCode(version=1, error_correction=error_correction, box_size=box_size, border=border)
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGB')

    size = len(qr.modules)
    module_size = box_size
    img_size = size * module_size + border * 2 * module_size
    img = Image.new('RGB', (img_size, img_size), back_color)
    draw = ImageDraw.Draw(img)

    radius = module_size // 2
    for y in range(size):
        for x in range(size):
            if qr.modules[y][x]:
                px = border * module_size + x * module_size
                py = border * module_size + y * module_size
                draw.rounded_rectangle(
                    [px + 1, py + 1, px + module_size - 1, py + module_size - 1],
                    radius=radius,
                    fill=fill_color
                )
    return img


def create_circle_qr(data, fill_color='black', back_color='white', box_size=10, border=4, error_correction=ERROR_CORRECT_M):
    qr = qrcode.QRCode(version=1, error_correction=error_correction, box_size=box_size, border=border)
    qr.add_data(data)
    qr.make(fit=True)

    size = len(qr.modules)
    module_size = box_size
    img_size = size * module_size + border * 2 * module_size
    img = Image.new('RGB', (img_size, img_size), back_color)
    draw = ImageDraw.Draw(img)

    for y in range(size):
        for x in range(size):
            if qr.modules[y][x]:
                px = border * module_size + x * module_size
                py = border * module_size + y * module_size
                draw.ellipse(
                    [px + 1, py + 1, px + module_size - 1, py + module_size - 1],
                    fill=fill_color
                )
    return img


def create_gradient_qr(data, color_start, color_end, back_color='white', box_size=10, border=4, error_correction=ERROR_CORRECT_M, style='square'):
    qr = qrcode.QRCode(version=1, error_correction=error_correction, box_size=box_size, border=border)
    qr.add_data(data)
    qr.make(fit=True)

    size = len(qr.modules)
    module_size = box_size
    img_size = size * module_size + border * 2 * module_size
    img = Image.new('RGB', (img_size, img_size), back_color)
    draw = ImageDraw.Draw(img)

    for y in range(size):
        for x in range(size):
            if qr.modules[y][x]:
                t = (x + y) / (2 * size) if size > 0 else 0
                r = int(color_start[0] * (1 - t) + color_end[0] * t)
                g = int(color_start[1] * (1 - t) + color_end[1] * t)
                b = int(color_start[2] * (1 - t) + color_end[2] * t)
                color = (r, g, b)

                px = border * module_size + x * module_size
                py = border * module_size + y * module_size

                if style == 'circle':
                    draw.ellipse(
                        [px + 1, py + 1, px + module_size - 1, py + module_size - 1],
                        fill=color
                    )
                elif style == 'rounded':
                    radius = module_size // 2
                    draw.rounded_rectangle(
                        [px + 1, py + 1, px + module_size - 1, py + module_size - 1],
                        radius=radius,
                        fill=color
                    )
                else:
                    draw.rectangle(
                        [px, py, px + module_size, py + module_size],
                        fill=color
                    )
    return img


def create_neon_qr(data, neon_color, back_color='black', box_size=10, border=4, error_correction=ERROR_CORRECT_M):
    qr = qrcode.QRCode(version=1, error_correction=error_correction, box_size=box_size, border=border)
    qr.add_data(data)
    qr.make(fit=True)

    size = len(qr.modules)
    module_size = box_size
    img_size = size * module_size + border * 2 * module_size
    img = Image.new('RGB', (img_size, img_size), back_color)
    draw = ImageDraw.Draw(img)

    for y in range(size):
        for x in range(size):
            if qr.modules[y][x]:
                px = border * module_size + x * module_size
                py = border * module_size + y * module_size
                draw.rectangle(
                    [px, py, px + module_size, py + module_size],
                    fill=neon_color
                )
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    return img


def create_retro_qr(data, box_size=10, border=4, error_correction=ERROR_CORRECT_M):
    qr = qrcode.QRCode(version=1, error_correction=error_correction, box_size=box_size, border=border)
    qr.add_data(data)
    qr.make(fit=True)

    size = len(qr.modules)
    module_size = box_size
    img_size = size * module_size + border * 2 * module_size
    img = Image.new('RGB', (img_size, img_size), (245, 222, 179))
    draw = ImageDraw.Draw(img)

    for y in range(size):
        for x in range(size):
            if qr.modules[y][x]:
                px = border * module_size + x * module_size
                py = border * module_size + y * module_size
                draw.rectangle(
                    [px + 1, py + 1, px + module_size - 1, py + module_size - 1],
                    fill=(60, 40, 30)
                )
    return img


def create_minimalist_qr(data, box_size=10, border=4, error_correction=ERROR_CORRECT_M):
    qr = qrcode.QRCode(version=1, error_correction=error_correction, box_size=box_size, border=border)
    qr.add_data(data)
    qr.make(fit=True)

    size = len(qr.modules)
    module_size = box_size
    img_size = size * module_size + border * 2 * module_size
    img = Image.new('RGB', (img_size, img_size), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    for y in range(size):
        for x in range(size):
            if qr.modules[y][x]:
                px = border * module_size + x * module_size
                py = border * module_size + y * module_size
                draw.line(
                    [px + module_size // 2, py + 1, px + module_size // 2, py + module_size - 1],
                    fill=(0, 0, 0),
                    width=2
                )
    return img


def create_golden_qr(data, box_size=10, border=4, error_correction=ERROR_CORRECT_M):
    return create_gradient_qr(data, (255, 215, 0), (184, 134, 11), back_color='#1a1a2e', box_size=box_size, border=border, error_correction=error_correction, style='rounded')


def create_matrix_qr(data, box_size=10, border=4, error_correction=ERROR_CORRECT_M):
    return create_gradient_qr(data, (0, 255, 0), (0, 100, 0), back_color='black', box_size=box_size, border=border, error_correction=error_correction, style='square')


def create_pixel_art_qr(data, box_size=10, border=4, error_correction=ERROR_CORRECT_M):
    qr = qrcode.QRCode(version=1, error_correction=error_correction, box_size=box_size, border=border)
    qr.add_data(data)
    qr.make(fit=True)

    size = len(qr.modules)
    module_size = box_size
    img_size = size * module_size + border * 2 * module_size
    img = Image.new('RGB', (img_size, img_size), (240, 240, 255))
    draw = ImageDraw.Draw(img)

    colors = [(255, 100, 100), (100, 200, 255), (150, 255, 150), (255, 200, 100), (200, 150, 255)]
    for y in range(size):
        for x in range(size):
            if qr.modules[y][x]:
                px = border * module_size + x * module_size
                py = border * module_size + y * module_size
                color = colors[(x + y) % len(colors)]
                draw.rectangle(
                    [px + 2, py + 2, px + module_size - 2, py + module_size - 2],
                    fill=color
                )
    return img


def generate_qr(url, style, error_correction='M', size=10, border=4):
    ec = ERROR_LEVELS.get(error_correction, ERROR_CORRECT_M)

    generators = {
        'classic': lambda: create_classic_qr(url, error_correction=ec, box_size=size, border=border),
        'rounded': lambda: create_rounded_qr(url, error_correction=ec, box_size=size, border=border),
        'circles': lambda: create_circle_qr(url, error_correction=ec, box_size=size, border=border),
        'gradient_blue': lambda: create_gradient_qr(url, (0, 123, 255), (0, 200, 255), error_correction=ec, box_size=size, border=border, style='rounded'),
        'gradient_purple': lambda: create_gradient_qr(url, (128, 0, 128), (255, 100, 200), error_correction=ec, box_size=size, border=border, style='circle'),
        'gradient_sunset': lambda: create_gradient_qr(url, (255, 100, 50), (255, 200, 100), error_correction=ec, box_size=size, border=border, style='rounded'),
        'gradient_forest': lambda: create_gradient_qr(url, (34, 139, 34), (144, 238, 144), error_correction=ec, box_size=size, border=border, style='circle'),
        'gradient_ocean': lambda: create_gradient_qr(url, (0, 100, 200), (0, 200, 255), back_color='#f0f8ff', error_correction=ec, box_size=size, border=border, style='rounded'),
        'neon_green': lambda: create_neon_qr(url, (0, 255, 0), error_correction=ec, box_size=size, border=border),
        'neon_pink': lambda: create_neon_qr(url, (255, 20, 147), error_correction=ec, box_size=size, border=border),
        'neon_cyan': lambda: create_neon_qr(url, (0, 255, 255), error_correction=ec, box_size=size, border=border),
        'retro': lambda: create_retro_qr(url, error_correction=ec, box_size=size, border=border),
        'minimalist': lambda: create_minimalist_qr(url, error_correction=ec, box_size=size, border=border),
        'golden': lambda: create_golden_qr(url, error_correction=ec, box_size=size, border=border),
        'matrix': lambda: create_matrix_qr(url, error_correction=ec, box_size=size, border=border),
        'pixel_art': lambda: create_pixel_art_qr(url, error_correction=ec, box_size=size, border=border),
    }

    return generators.get(style, generators['classic'])()


@app.route('/')
def index():
    return render_template('index.html', styles=STYLES)


@app.route('/generate', methods=['POST'])
def generate():
    url = request.form.get('url', '').strip()
    style = request.form.get('style', 'classic')
    error_correction = request.form.get('error_correction', 'M')
    size = int(request.form.get('size', 10))
    border = int(request.form.get('border', 4))

    if not url:
        return render_template('index.html', styles=STYLES, error='URL is required!')

    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        qr_img = generate_qr(url, style, error_correction, size, border)

        img_io = io.BytesIO()
        qr_img.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name=f'qrcode_{style}.png')
    except Exception as e:
        return render_template('index.html', styles=STYLES, error=f'Error: {str(e)}')


@app.route('/preview', methods=['POST'])
def preview():
    url = request.form.get('url', '').strip()
    style = request.form.get('style', 'classic')
    error_correction = request.form.get('error_correction', 'M')
    size = int(request.form.get('size', 10))
    border = int(request.form.get('border', 4))

    if not url:
        return render_template('index.html', styles=STYLES, error='URL is required!')

    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        qr_img = generate_qr(url, style, error_correction, size, border)

        img_io = io.BytesIO()
        qr_img.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        return render_template('index.html', styles=STYLES, error=f'Error: {str(e)}')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
