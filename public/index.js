/**
 * Sidebar management and dynamic iframe content handling.
 */

// Obtain references to the sidebar and its overlay.
const mySidebar = document.getElementById("mySidebar");
const overlayBg = document.getElementById("myOverlay");

/**
 * Toggle the sidebar's visibility and manage its overlay effect.
 * If the sidebar is displayed, this function will hide it and vice versa.
 */
function w3_open() {
    if (mySidebar.style.display === 'block') {
        mySidebar.style.display = 'none';
        overlayBg.style.display = "none";
    } else {
        mySidebar.style.display = 'block';
        overlayBg.style.display = "block";
    }
}

/**
 * Close the sidebar and hide its overlay effect.
 */
function w3_close() {
    mySidebar.style.display = "none";
    overlayBg.style.display = "none";
}

/**
 * Switch the currently displayed iframe.
 * @param {string} iframeID - The ID of the iframe to display.
 */
function switchIframe(iframeID) {
    // Hide all iframes first.
    const iframeContainers = document.querySelectorAll('.iframe-container');
    iframeContainers.forEach(iframe => {
        iframe.style.display = 'none';
    });

    // Display the desired iframe.
    document.getElementById('datawrapper-chart-' + iframeID + '-container').style.display = 'block';
}

/**
 * Show a specific content div while hiding others.
 * @param {string} id - The ID of the content div to display.
 */
function show(id) {
    // Hide all content divs.
    const contents = document.querySelectorAll('.content');
    contents.forEach(content => {
        content.style.display = 'none';
    });

    // Display the desired content div.
    document.getElementById(id).style.display = 'block';
}

// On page load, hide all content divs except the 'summary'.
window.onload = function() {
    const contents = document.querySelectorAll('.content');
    contents.forEach(content => {
        content.style.display = 'none';
    });
    document.getElementById('summary').style.display = 'block';
}
