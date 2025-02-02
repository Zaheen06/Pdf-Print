function countPages() {
    const fileInput = document.getElementById("pdfFile");
    const pageCountDisplay = document.getElementById("pageCount");

    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        const reader = new FileReader();

        reader.onload = function (e) {
            const pdfData = new Uint8Array(e.target.result);
            const pdfjsLib = window['pdfjs-dist/build/pdf'];

            pdfjsLib.getDocument(pdfData).promise.then(function (pdf) {
                pageCountDisplay.textContent = `Pages: ${pdf.numPages}`;
            });
        };

        reader.readAsArrayBuffer(file);
    }
}
