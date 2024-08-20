document.addEventListener("DOMContentLoaded", function() {
    const copyButton = document.getElementById('copy-brief');
    const modifyButton = document.getElementById('modify-brief');
    const briefOutput = document.getElementById('brief-output');

    copyButton.addEventListener('click', function() {
        document.execCommand('copy');
        briefOutput.select();
        alert('Brief copied to clipboard');
    });

    modifyButton.addEventListener('click', function() {
        briefOutput.removeAttribute('readonly');
        // briefOutput.focus();
        alert('Now you can modify your brief as you want..');

    });
});

document.getElementById('input-mode').addEventListener('change', function () {
    if (this.checked) {
        document.getElementById('available-options').style.display = 'none';
        document.getElementById('custom-inputs').style.display = 'block';
        document.getElementById('input-mode-label').innerText = 'Use Available Options';
    } else {
        document.getElementById('available-options').style.display = 'block';
        document.getElementById('custom-inputs').style.display = 'none';
        document.getElementById('input-mode-label').innerText = 'Use Custom Input';
    }
});

document.getElementById('generate-brief-form').addEventListener('submit', function (e) {
    let mode = document.getElementById('input-mode').checked;
    let valid = true;

    // Validation logic
    if (mode) {
        if (!document.getElementById('custom-brief-type').value.trim() || !document.getElementById('custom-domain').value.trim()) {
            valid = false;
        }
    } else {
        if (!document.getElementById('brief-type').value || !document.getElementById('domain').value) {
            valid = false;
        }
    }

    if (!valid) {
        e.preventDefault();
        alert('Please fill in all required fields.');
        return; // Exit if validation fails
    }

    // Add the dots and change button text after validation
    const button = document.getElementById('generate-button');
    button.innerHTML = `
        <section class="dots-container">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        </section>
    `;

    // Simulate a generation process with a timeout (Replace this with your actual generation logic)
    setTimeout(() => {
        button.textContent = 'Generate'; // Revert button to the original state
        // Submit the form programmatically if needed
        document.getElementById('generate-brief-form').submit();
    },3000); // Adjust the time to match your generation process
});
// Function to initialize the history panel state based on the toggle
function initializeHistoryPanel() {
    const historySections = document.getElementById('history-sections');
    const toggleHistory = document.getElementById('toggle-history');

    if (toggleHistory.checked) {
        // If the toggle is checked, show the history panel
        historySections.style.display = 'block';
        gethistory();  // Load history from the server
    } else {
        // If the toggle is not checked, hide the history panel
        historySections.style.display = 'none';
    }
}

// Event listener for the toggle button
document.getElementById('toggle-history').addEventListener('change', function() {
    const historySections = document.getElementById('history-sections');
    
    if (this.checked) {
        // Show history
        historySections.style.display = 'block';
        gethistory();  // Load history from the server
    } else {
        // Hide history
        historySections.style.display = 'none';
    }
});

// Function to fetch and display user history
function gethistory() {
    fetch('/history')  // Endpoint to get user history
        .then(response => response.json())
        .then(data => {
            // Define sections for today, yesterday, past week, and past month
            const sections = {
                today: document.getElementById('history-today'),
                yesterday: document.getElementById('history-yesterday'),
                week: document.getElementById('history-week'),
                month: document.getElementById('history-month')
            };

            // Clear previous content in sections
            for (const key in sections) {
                sections[key].innerHTML = `<h4>${key.charAt(0).toUpperCase() + key.slice(1)}</h4>`;
            }

            // Populate history sections based on the timestamp
            data.forEach(item => {
                const date = new Date(item.timestamp);
                const sectionKey = getSectionKey(date);
                const section = sections[sectionKey];
                if (section) {
                    const briefItem = document.createElement('div');
                    briefItem.className = 'brief-item';
                    briefItem.textContent = `Domain: ${item.domain}, Type: ${item.type}`;
                    briefItem.addEventListener('click', function() {
                        showFullHistory(item);  // Display full history in the text area
                    });
                    section.appendChild(briefItem);
                }
            });
        })
        .catch(error => console.error('Error fetching history:', error));
}

// Function to determine which section the history item belongs to
function getSectionKey(date) {
    const now = new Date();
    const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24));
    if (diffDays === 0) return 'today';
    if (diffDays === 1) return 'yesterday';
    if (diffDays <= 7) return 'week';
    if (diffDays <= 30) return 'month';
    return null; // History older than a month is not displayed
}

// Function to display full history in the text area
function showFullHistory(item) {
    const briefOutput = document.getElementById('brief-output');
    briefOutput.value = `Domain: ${item.domain}\nType: ${item.type}\n\nBrief:\n${item.brief}`;
}

// Initialize the history panel when the page loads
initializeHistoryPanel();
