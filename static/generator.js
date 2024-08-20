document.addEventListener('DOMContentLoaded', function () {
    const inputMode = document.getElementById('input-mode');
    const selectOptions = document.getElementById('select-options');
    const customOptions = document.getElementById('custom-options');

    inputMode.addEventListener('change', function () {
        if (inputMode.value === 'select') {
            selectOptions.style.display = 'block';
            customOptions.style.display = 'none';
        } else {
            selectOptions.style.display = 'none';
            customOptions.style.display = 'block';
        }
    });
});



