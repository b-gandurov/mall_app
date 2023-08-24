const logoutBtn = document.getElementById('logout-btn');
logoutBtn.onclick = (event) => {
    event.preventDefault();
    const form = document.getElementById('logout-form');
    form.submit();
}

function startTimer(reservationId, reservationTime, reservationTimerMinutes) {
    var countdownDate = new Date(reservationTime).getTime() + reservationTimerMinutes * 60 * 1000;
    var x = setInterval(function () {
        var now = new Date().getTime();
        var distance = countdownDate - now;
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);
        document.getElementById("timer-" + reservationId).innerHTML = minutes + "m " + seconds + "s ";

        if (distance < 0) {
            clearInterval(x);
            let el = document.getElementById("timer-" + reservationId)
            el.innerHTML = "Your reservation has expired";
        }
    }, 1000);
}

function showSection(section) {
    document.getElementById('profile-section').style.display = 'none';
    document.getElementById('reservations-section').style.display = 'none';
    document.getElementById('tickets-section').style.display = 'none';

    switch (section) {
        case 'profile':
            document.getElementById('profile-section').style.display = 'block';
            break;
        case 'reservations':
            document.getElementById('reservations-section').style.display = 'block';
            break;
        case 'tickets':
            document.getElementById('tickets-section').style.display = 'block';
            break;
    }
}

document.getElementById('profile-btn').addEventListener('click', function () {
    showSection('profile');
});

document.getElementById('reservations-btn').addEventListener('click', function () {
    showSection('reservations');
});

document.getElementById('tickets-btn').addEventListener('click', function () {
    showSection('tickets');
});

// Hide reservations and tickets sections on page load
document.getElementById('reservations-section').style.display = 'none';
document.getElementById('tickets-section').style.display = 'none';
