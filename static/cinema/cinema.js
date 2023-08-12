function updateSeatColor(label) {
    const input = label.querySelector('input');
    if (input.checked || input.disabled) {
        label.style['background-color'] = 'red';
    } else {
        label.style['background-color'] = 'green';
    }
}

document.querySelectorAll('.seat-booking-form label').forEach((label) => {
    const input = label.querySelector('input');
    updateSeatColor(label);
    input.addEventListener('change', () => {
        updateSeatColor(label);
    });
});


const screeningForms = document.querySelectorAll('.seat-booking-form[data-screening]');

function showScreening(event) {
    screeningForms.forEach((form) => {
        if (form.dataset.screening === event.target.dataset.screening) {
            if (form.classList.contains('active')) {
                form.classList.remove('active');
            } else {
                form.classList.add('active');
            }
        } else {
            form.classList.remove('active');
        }
    });
}


document.querySelectorAll('.screening-btn[data-screening]').forEach((btn) => {
    btn.onclick = showScreening;
})