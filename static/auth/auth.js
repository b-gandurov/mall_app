const logoutBtn = document.getElementById('logout-btn');
logoutBtn.onclick = (event) => {
    event.preventDefault();
    const form = document.getElementById('logout-form');
    form.submit()
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
            document.getElementById("timer-" + reservationId).innerHTML = "EXPIRED";
            fetch(`/increase_item_quantity/?reservation_id=${reservationId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        console.log('Item quantity increased by 1.');
                    } else if (data.status === 'already_increased') {
                        console.log('Item quantity was already increased.');
                    }
                });
        }
    }, 1000);
}


function updateTimers() {
    // Get all the elements with class timer
    var timers = document.getElementsByClassName('timer');
    if (!timers.length) {
        return;
    }

    // Loop through each timer element
    for (var i = 0; i < timers.length; i++) {
        // Get the start time for this timer
        var startTime = new Date(parseInt(timers[i].dataset.startTime) * 1000);

        // Calculate the time remaining
        var now = new Date();
        var timeRemaining = startTime - now;

        // Check if the time remaining is positive
        if (timeRemaining > 0) {
            // Calculate hours, minutes, and seconds
            var hours = Math.floor(timeRemaining / (1000 * 60 * 60));
            var minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);

            // Update the display
            timers[i].innerText = hours + "h " + minutes + "m " + seconds + "s remaining";
        } else {
            // If the time remaining is not positive, the movie has started
            timers[i].innerText = "Movie has started";
        }
    }
}

// Update the timers every second
setInterval(updateTimers, 1000);


window.addEventListener('load', function () {
    const messagesDiv = document.getElementById('messages-anchor');
    if (messagesDiv) {
        messagesDiv.scrollIntoView({behavior: 'smooth'});
    }
});
document.getElementById('profile-btn').addEventListener('click', function () {
    document.getElementById('profile-section').style.display = 'block';
    document.getElementById('reservations-section').style.display = 'none';
    document.getElementById('tickets-section').style.display = 'none';
});

document.getElementById('reservations-btn').addEventListener('click', function () {
    document.getElementById('profile-section').style.display = 'none';
    document.getElementById('reservations-section').style.display = 'block';
    document.getElementById('tickets-section').style.display = 'none';
});

document.getElementById('tickets-btn').addEventListener('click', function () {
    document.getElementById('profile-section').style.display = 'none';
    document.getElementById('reservations-section').style.display = 'none';
    document.getElementById('tickets-section').style.display = 'block';
});

// Hide reservations and tickets sections on page load
document.getElementById('reservations-section').style.display = 'none';
document.getElementById('tickets-section').style.display = 'none';

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('show-profile').addEventListener('click', function () {
        showSection('profile');
    });

    document.getElementById('show-reservations').addEventListener('click', function () {
        showSection('reservations');
    });

    document.getElementById('show-tickets').addEventListener('click', function () {
        showSection('tickets');
    });

    var unbookButtons = document.querySelectorAll('.unbook-form button');
    unbookButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            showSection('tickets');
        });
    });
});

function showSection(section) {
    // Hide all sections
    var sections = document.querySelectorAll('.section');
    sections.forEach(function (sec) {
        sec.style.display = 'none';
    });

    // Show the selected section
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
