// Minimal PDF Editor: Two-canvas architecture for robust PDF+overlay editing
// Uses PDF.js for rendering and Fabric.js for overlay text editing

let pdfDoc = null;
let currentPage = 1;
let fabricCanvas = null;
let scale = 1.5;

// DOMContentLoaded: Setup file input and navigation
window.addEventListener('DOMContentLoaded', () => {
    document.getElementById('pdfFile').addEventListener('change', handleFileSelect);
    document.getElementById('prevPage').addEventListener('click', () => changePage(-1));
    document.getElementById('nextPage').addEventListener('click', () => changePage(1));
    document.getElementById('saveButton').addEventListener('click', saveEdits);
    showStatus('Please select a PDF file');
});

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (!file || file.type !== 'application/pdf') {
        showStatus('Please select a valid PDF file.');
        return;
    }
    const reader = new FileReader();
    reader.onload = function(ev) {
        loadPdf(ev.target.result);
    };
    reader.readAsArrayBuffer(file);
}

async function loadPdf(data) {
    showStatus('Loading PDF...');
    pdfjsLib.getDocument({ data }).promise.then(doc => {
        pdfDoc = doc;
        window.pdfDoc = doc;
        currentPage = 1;
        renderPage(currentPage);
        showStatus('PDF loaded.');
    }).catch(() => showStatus('Failed to load PDF.'));
}

function changePage(offset) {
    if (!pdfDoc) return;
    const newPage = currentPage + offset;
    if (newPage < 1 || newPage > pdfDoc.numPages) return;
    currentPage = newPage;
    renderPage(currentPage);
}

async function renderPage(pageNum) {
    showStatus('Rendering page...');
    const page = await pdfDoc.getPage(pageNum);
    const viewport = page.getViewport({ scale });
    const pdfCanvas = document.getElementById('pdfCanvas');
    const overlayCanvas = document.getElementById('overlayCanvas');
    const container = document.getElementById('pdfContainer');
    // High-DPI support
    const dpr = window.devicePixelRatio || 1;
    [pdfCanvas, overlayCanvas].forEach(c => {
        c.width = viewport.width * dpr;
        c.height = viewport.height * dpr;
        c.style.width = viewport.width + 'px';
        c.style.height = viewport.height + 'px';
    });
    if (container) {
        container.style.width = viewport.width + 'px';
        container.style.height = viewport.height + 'px';
        container.style.minWidth = viewport.width + 'px';
        container.style.minHeight = viewport.height + 'px';
    }
    // Render PDF page to background canvas at high DPI
    const ctx = pdfCanvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, pdfCanvas.width, pdfCanvas.height);
    await page.render({ canvasContext: ctx, viewport }).promise;
    // Setup Fabric.js overlay and overlay all PDF text as editable textboxes
    await setupFabricOverlayWithPdfText(overlayCanvas, page, viewport, dpr);
    showStatus(`Page ${pageNum} of ${pdfDoc.numPages}`);
}

function setupFabricOverlay(canvas, width, height) {
    if (fabricCanvas) {
        fabricCanvas.dispose();
    }
    fabricCanvas = new fabric.Canvas(canvas, {
        selection: true,
        backgroundColor: null
    });
    window.fabricCanvas = fabricCanvas;
    fabricCanvas.setWidth(width);
    fabricCanvas.setHeight(height);
    fabricCanvas.backgroundColor = null;
    // Double-click to add text
    fabricCanvas.on('mouse:dblclick', function(opt) {
        const pointer = fabricCanvas.getPointer(opt.e);
        const textbox = new fabric.Textbox('Edit me', {
            left: pointer.x,
            top: pointer.y,
            fontSize: 16,
            fill: '#000',
            width: 120,
            backgroundColor: ''
        });
        fabricCanvas.add(textbox).setActiveObject(textbox);
    });
}

async function setupFabricOverlayWithPdfText(canvas, page, viewport, dpr) {
    if (fabricCanvas) {
        fabricCanvas.dispose();
    }
    fabricCanvas = new fabric.Canvas(canvas, {
        selection: true,
        backgroundColor: null
    });
    fabricCanvas.setWidth(viewport.width * dpr);
    fabricCanvas.setHeight(viewport.height * dpr);
    fabricCanvas.backgroundColor = null;
    // Extract PDF text and overlay as editable textboxes
    const textContent = await page.getTextContent();
    textContent.items.forEach(item => {
        if (!item.str.trim()) return;
        const [a, b, c, d, e, f] = item.transform;
        // PDF.js coordinates: e, f are the bottom-left of the text box
        // Fabric.js: left, top are top-left, so adjust for font size
        const fontSize = Math.abs(d) * dpr;
        const left = e * dpr;
        const top = (viewport.height - f) * dpr - fontSize;
        const textbox = new fabric.Textbox(item.str, {
            left,
            top,
            fontSize,
            fill: '#000',
            width: item.width * dpr,
            backgroundColor: '',
            fontFamily: 'Arial',
            selectable: true,
            editable: true
        });
        fabricCanvas.add(textbox);
    });
    // Double-click to add new text
    fabricCanvas.on('mouse:dblclick', function(opt) {
        const pointer = fabricCanvas.getPointer(opt.e);
        const textbox = new fabric.Textbox('Edit me', {
            left: pointer.x,
            top: pointer.y,
            fontSize: 16 * dpr,
            fill: '#000',
            width: 120 * dpr,
            backgroundColor: ''
        });
        fabricCanvas.add(textbox).setActiveObject(textbox);
    });
}

function saveEdits() {
    if (!fabricCanvas) return;
    fabricCanvas.discardActiveObject();
    const dataURL = fabricCanvas.toDataURL({ format: 'png' });
    const link = document.createElement('a');
    link.href = dataURL;
    link.download = 'pdf-edits-overlay.png';
    link.click();
    showStatus('Overlay exported as image. (Integrate PDF merging for full solution)');
}

function showStatus(msg) {
    const status = document.getElementById('status');
    if (status) status.textContent = msg;
}