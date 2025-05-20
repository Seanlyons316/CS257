// document.querySelector('.dropbtn').addEventListener('click', function() {
//     document.querySelector('.dropdown-content').classList.toggle('show') });

// document.getElementById('years-btn').addEventListener('click', function(event) {
    // event.stopPropagation();
// Hide the other dropdowns
// document.getElementById('measurements-menu').classList.remove('show');
// document.getElementById('damages-menu').classList.remove('show');
    // Toggle this one
    // document.getElementById('years-menu').classList.toggle('show');
// });

document.getElementById('measurements-btn').addEventListener('click', function(event) {
    event.stopPropagation();
    // document.getElementById('years-menu').classList.remove('show');
    document.getElementById('damages-menu').classList.remove('show');
    document.getElementById('measurements-menu').classList.toggle('show');
});

document.getElementById('damages-btn').addEventListener('click', function(event) {
    event.stopPropagation();
    // document.getElementById('years-menu').classList.remove('show');
    document.getElementById('measurements-menu').classList.remove('show');
    document.getElementById('damages-menu').classList.toggle('show');
});

// click anywhere else to close the dropdowns
window.addEventListener('click', function() {
    // document.getElementById('years-menu').classList.remove('show');
    document.getElementById('measurements-menu').classList.remove('show');
    document.getElementById('damages-menu').classList.remove('show');
});