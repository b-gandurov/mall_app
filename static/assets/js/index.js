const stores = document.querySelectorAll('div[data-position]')
const next = document.getElementById('next-store');
const previous = document.getElementById('previous-store');

let leftmostIndex = 3;
const numberOfStoresToDisplay = 4;

stores.forEach((store) => {
    store.style.display = 'none';
})

for (let i = 0; i < numberOfStoresToDisplay; i++) {
    stores[i].style.display = 'block';
}

function rerenderStores() {
    stores.forEach((store, index) => {
        if (index < leftmostIndex) {
            store.style.display = 'none';
            return;
        }

        if (index > leftmostIndex + numberOfStoresToDisplay - 1) {
            store.style.display = 'none';
            return;
        }

        store.style.display = 'block';
    })
}

function assertNextButtonVisibility() {
    if (leftmostIndex + numberOfStoresToDisplay === stores.length) {
        next.style.display = 'none';
    } else {
        next.style.display = 'block';
    }
}

function assertPreviousButtonVisibility() {
    if (leftmostIndex === 0) {
        previous.style.opacity = '0';
    } else {
        previous.style.opacity = '1';
    }
}

rerenderStores();
assertNextButtonVisibility();
assertPreviousButtonVisibility();
next.onclick = () => {
    leftmostIndex += 1;
    assertNextButtonVisibility();
    assertPreviousButtonVisibility();
    rerenderStores();
}

previous.onclick = () => {
    if (leftmostIndex !== 0) {
        leftmostIndex -= 1;
    }
    assertNextButtonVisibility();
    assertPreviousButtonVisibility();
    rerenderStores();
}