// Get the current URL path
const currentPath = window.location.pathname;

// Check if the current path matches the /games page
if (currentPath === '/games') {
    // Add the 'active' class to the #games element
    const gamesElement = document.getElementById('gamesLink');
    gamesElement.classList.add('active');
}
else if (currentPath === '/model/') {
    // Add the 'active' class to the #games element
    const gamesElement = document.getElementById('predictionsLink');
    gamesElement.classList.add('active');
}
else if (currentPath === '/teams') {
    // Add the 'active' class to the #games element
    const gamesElement = document.getElementById('teamsLink');
    gamesElement.classList.add('active');
}
else if (currentPath === '/support') {
    // Add the 'active' class to the #games element
    const gamesElement = document.getElementById('supportLink');
    gamesElement.classList.add('active');
}
else if (currentPath === '/stats') {
    // Add the 'active' class to the #games element
    const gamesElement = document.getElementById('statsLink');
    gamesElement.classList.add('active');
}