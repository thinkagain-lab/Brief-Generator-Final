document.getElementById('download-brief').addEventListener('click', function () {
    const button = this;
    const spinner = document.getElementById('loading-spinner');

    button.textContent = 'Downloading...'; // Change button text
    spinner.style.display = 'inline-block'; // Show spinner

    const content = document.getElementById('brief-output').value;
    const option = document.getElementById('download-options').value;

    if (option === 'text') {
        downloadTextFile(content);
    } else if (option === 'pdf') {
        downloadPDF(content);
    } else if (option === 'image') {
        downloadImage(); // Updated function call
    }

    // Reset button text and hide spinner after 2 seconds (adjust time as needed)
    setTimeout(() => {
        button.textContent = 'Download';
        spinner.style.display = 'none'; // Hide spinner
    }, 2000);
});


function downloadTextFile(content) {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'brief.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function downloadPDF(content) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    const lines = doc.splitTextToSize(content, 180); // Auto-split text into lines that fit within the page width
    doc.text(lines, 10, 10);
    doc.save('brief.pdf');
}



// function downloadImage() {
//     const contentElement = document.getElementById('brief-output'); // The element you want to capture

//     // Use html2canvas to capture the content as a canvas
//     html2canvas(contentElement, {
//         scale: 2, // Increase resolution for better quality
//         // backgroundColor: null // Set background color to null if you want it to be transparent
//     }).then(canvas => {
//         // Convert the canvas to a data URL and then to a Blob for downloading
//         canvas.toBlob(function(blob) {
//             const url = URL.createObjectURL(blob);
//             const a = document.createElement('a');
//             a.href = url;
//             a.download = 'brief.png'; // Set your desired filename
//             document.body.appendChild(a);
//             a.click();
//             document.body.removeChild(a);

//             // Revoke the object URL to free up memory
//             URL.revokeObjectURL(url);
//         });
//     });
// }

function downloadImage() {
    return new Promise((resolve) => {
        const contentElement = document.getElementById('generated-brief'); // Element containing the text and background

        // Use html2canvas to capture the content as a canvas
        html2canvas(contentElement, {
            onrendered: function (canvas) {
                // Convert the canvas to an image file
                canvas.toBlob(function (blob) {
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'brief.jpg';
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    resolve();
                });
            }
        });
    });
}


// BELOW IS FOR GIVING THE DOWNLOAD EFFECT WHILE DOWNLOADING


// document.getElementById('download-brief').addEventListener('click', function () {
//     const button = this;
//     const spinner = document.getElementById('loading-spinner');

//     button.textContent = 'Downloading...'; // Change button text
//     spinner.style.display = 'inline-block'; // Show spinner

//     const content = document.getElementById('brief-output').value;
//     const option = document.getElementById('download-options').value;

//     // Determine which download function to call
//     if (option === 'text') {
//         downloadTextFile(content).then(() => resetButton(button, spinner));
//     } else if (option === 'pdf') {
//         downloadPDF(content).then(() => resetButton(button, spinner));
//     } else if (option === 'image') {
//         downloadImage().then(() => resetButton(button, spinner));
//     }
// });

// function resetButton(button, spinner) {
//     button.textContent = 'Download'; // Reset button text
//     spinner.style.display = 'none';  // Hide spinner
// }

// function downloadTextFile(content) {
//     return new Promise((resolve) => {
//         const blob = new Blob([content], { type: 'text/plain' });
//         const url = URL.createObjectURL(blob);
//         const a = document.createElement('a');
//         a.href = url;
//         a.download = 'brief.txt';
//         document.body.appendChild(a);
//         a.click();
//         document.body.removeChild(a);
//         resolve();
//     });
// }

// function downloadPDF(content) {
//     return new Promise((resolve) => {
//         const { jsPDF } = window.jspdf;
//         const doc = new jsPDF();
//         const lines = doc.splitTextToSize(content, 180); // Auto-split text into lines that fit within the page width
//         doc.text(lines, 10, 10);
//         doc.save('brief.pdf');
//         resolve();
//     });
// }

// function downloadImage() {
//     return new Promise((resolve) => {
//         const contentElement = document.getElementById('generated-brief'); // Element containing the text and background

//         // Use html2canvas to capture the content as a canvas
//         html2canvas(contentElement, {
//             onrendered: function (canvas) {
//                 // Convert the canvas to an image file
//                 canvas.toBlob(function (blob) {
//                     const url = URL.createObjectURL(blob);
//                     const a = document.createElement('a');
//                     a.href = url;
//                     a.download = 'brief.jpg';
//                     document.body.appendChild(a);
//                     a.click();
//                     document.body.removeChild(a);
//                     resolve();
//                 });
//             }
//         });
//     });
// }
