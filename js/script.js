let selectedStyle = 'squares';
let qrGenerated = false;

const ecLevels = ['L (7%)', 'M (15%)', 'Q (25%)', 'H (30%)'];
const ecMap = { 0: 'L', 1: 'M', 2: 'Q', 3: 'H' };

document.getElementById('fg-color').addEventListener('input', function() {
    document.getElementById('fg-value').textContent = this.value;
    clearFgPreset();
});

document.getElementById('bg-color').addEventListener('input', function() {
    document.getElementById('bg-value').textContent = this.value;
    clearBgPreset();
});

document.getElementById('size-slider').addEventListener('input', function() {
    document.getElementById('size-value').textContent = this.value;
});

document.getElementById('margin-slider').addEventListener('input', function() {
    document.getElementById('margin-value').textContent = this.value;
});

document.getElementById('ec-slider').addEventListener('input', function() {
    document.getElementById('ec-value').textContent = ecLevels[this.value];
});

function selectStyle(el) {
    document.querySelectorAll('.style-card').forEach(c => c.classList.remove('active'));
    el.classList.add('active');
    selectedStyle = el.dataset.style;
}

function setFgColor(el) {
    document.querySelectorAll('#fg-presets .preset-color').forEach(c => c.classList.remove('active'));
    el.classList.add('active');
    document.getElementById('fg-color').value = el.dataset.color;
    document.getElementById('fg-value').textContent = el.dataset.color;
}

function setBgColor(el) {
    document.querySelectorAll('#bg-presets .preset-color').forEach(c => c.classList.remove('active'));
    el.classList.add('active');
    document.getElementById('bg-color').value = el.dataset.color;
    document.getElementById('bg-value').textContent = el.dataset.color;
}

function clearFgPreset() {
    document.querySelectorAll('#fg-presets .preset-color').forEach(c => c.classList.remove('active'));
}

function clearBgPreset() {
    document.querySelectorAll('#bg-presets .preset-color').forEach(c => c.classList.remove('active'));
}

function showError(msg) {
    document.getElementById('error-message').textContent = msg;
    document.getElementById('error-alert').style.display = 'block';
}

function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : { r: 0, g: 0, b: 0 };
}

function generateQR() {
    const url = document.getElementById('url-input').value.trim();
    if (!url) {
        showError('Please enter a URL or text!');
        return;
    }

    document.getElementById('error-alert').style.display = 'none';

    const size = parseInt(document.getElementById('size-slider').value);
    const margin = parseInt(document.getElementById('margin-slider').value);
    const ecLevel = ecMap[document.getElementById('ec-slider').value];
    const fgColor = document.getElementById('fg-color').value;
    const bgColor = document.getElementById('bg-color').value;

    try {
        const qr = qrcode(0, ecLevel);
        qr.addData(url);
        qr.make();

        const moduleCount = qr.getModuleCount();
        const cellSize = Math.floor((size - margin * 2) / moduleCount);
        const actualSize = cellSize * moduleCount + margin * 2;

        const canvas = document.getElementById('qr-canvas');
        canvas.width = actualSize;
        canvas.height = actualSize;
        const ctx = canvas.getContext('2d');

        ctx.fillStyle = bgColor;
        ctx.fillRect(0, 0, actualSize, actualSize);

        ctx.fillStyle = fgColor;

        for (let row = 0; row < moduleCount; row++) {
            for (let col = 0; col < moduleCount; col++) {
                if (qr.isDark(row, col)) {
                    const x = margin + col * cellSize;
                    const y = margin + row * cellSize;

                    switch (selectedStyle) {
                        case 'squares':
                            ctx.fillRect(x, y, cellSize, cellSize);
                            break;

                        case 'dots':
                            ctx.beginPath();
                            ctx.arc(x + cellSize / 2, y + cellSize / 2, cellSize / 2, 0, Math.PI * 2);
                            ctx.fill();
                            break;

                        case 'rounded':
                            const r = cellSize * 0.3;
                            ctx.beginPath();
                            ctx.moveTo(x + r, y);
                            ctx.lineTo(x + cellSize - r, y);
                            ctx.quadraticCurveTo(x + cellSize, y, x + cellSize, y + r);
                            ctx.lineTo(x + cellSize, y + cellSize - r);
                            ctx.quadraticCurveTo(x + cellSize, y + cellSize, x + cellSize - r, y + cellSize);
                            ctx.lineTo(x + r, y + cellSize);
                            ctx.quadraticCurveTo(x, y + cellSize, x, y + cellSize - r);
                            ctx.lineTo(x, y + r);
                            ctx.quadraticCurveTo(x, y, x + r, y);
                            ctx.closePath();
                            ctx.fill();
                            break;

                        case 'diamonds':
                            ctx.beginPath();
                            ctx.moveTo(x + cellSize / 2, y);
                            ctx.lineTo(x + cellSize, y + cellSize / 2);
                            ctx.lineTo(x + cellSize / 2, y + cellSize);
                            ctx.lineTo(x, y + cellSize / 2);
                            ctx.closePath();
                            ctx.fill();
                            break;

                        case 'star':
                            drawStar(ctx, x + cellSize / 2, y + cellSize / 2, 5, cellSize / 2, cellSize / 4);
                            ctx.fill();
                            break;

                        case 'striped':
                            const stripeWidth = cellSize / 3;
                            for (let s = 0; s < 3; s++) {
                                ctx.fillRect(x + s * stripeWidth, y, stripeWidth - 1, cellSize);
                            }
                            break;
                    }
                }
            }
        }

        document.getElementById('preview-container').classList.add('show');
        document.getElementById('download-btn').disabled = false;
        qrGenerated = true;

    } catch (e) {
        showError('Error generating QR code: ' + e.message);
    }
}

function drawStar(ctx, cx, cy, spikes, outerRadius, innerRadius) {
    let rot = Math.PI / 2 * 3;
    let step = Math.PI / spikes;

    ctx.beginPath();
    ctx.moveTo(cx, cy - outerRadius);

    for (let i = 0; i < spikes; i++) {
        ctx.lineTo(cx + Math.cos(rot) * outerRadius, cy + Math.sin(rot) * outerRadius);
        rot += step;
        ctx.lineTo(cx + Math.cos(rot) * innerRadius, cy + Math.sin(rot) * innerRadius);
        rot += step;
    }

    ctx.lineTo(cx, cy - outerRadius);
    ctx.closePath();
}

function downloadQR() {
    if (!qrGenerated) {
        showError('Please generate a QR code first!');
        return;
    }

    const canvas = document.getElementById('qr-canvas');
    const link = document.createElement('a');
    link.download = 'qrcode.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
}

document.getElementById('url-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') generateQR();
});

function submitReport() {
    const message = document.getElementById('report-message').value.trim();
    if (!message) {
        alert('Please describe the issue you encountered.');
        return;
    }

    const name = document.getElementById('report-name').value.trim() || 'Anonymous';
    const email = document.getElementById('report-email').value.trim() || 'Not provided';
    const type = document.getElementById('report-type').value;

    const subject = encodeURIComponent(`[QR Generator] ${type}: Report from ${name}`);
    const body = encodeURIComponent(
        `Name: ${name}\nEmail: ${email}\nIssue Type: ${type}\n\nDescription:\n${message}\n\n---\nBrowser: ${navigator.userAgent}\nURL: ${window.location.href}`
    );

    window.location.href = `mailto:joni911@example.com?subject=${subject}&body=${body}`;

    $('#reportModal').modal('hide');
    document.getElementById('report-form').reset();

    alert('Thank you for your report! Your email client will open to send the report.');
}
