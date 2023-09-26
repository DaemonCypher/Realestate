// Get the Sidebar
var mySidebar = document.getElementById("mySidebar");

// Get the DIV with overlay effect
var overlayBg = document.getElementById("myOverlay");

// Toggle between showing and hiding the sidebar, and add overlay effect
function w3_open() {
  if (mySidebar.style.display === 'block') {
    mySidebar.style.display = 'none';
    overlayBg.style.display = "none";
  } else {
    mySidebar.style.display = 'block';
    overlayBg.style.display = "block";
  }
}

// Close the sidebar with the close button
function w3_close() {
  mySidebar.style.display = "none";
  overlayBg.style.display = "none";
}


function switchIframe(iframeID) {
  // First, hide all iframes
  var iframeContainers = document.querySelectorAll('.iframe-container');
  for (var i = 0; i < iframeContainers.length; i++) {
      iframeContainers[i].style.display = 'none';
  }

  // Now, display the selected iframe
  document.getElementById('datawrapper-chart-' + iframeID + '-container').style.display = 'block';
}


function show(id) {
  // Get all content divs and hide them
  var contents = document.querySelectorAll('.content');
  for (var i = 0; i < contents.length; i++) {
      contents[i].style.display = 'none';
  }

  // Show the selected content div
  document.getElementById(id).style.display = 'block';
}

// Hide all content divs on page load except the overview
window.onload = function() {
  var contents = document.querySelectorAll('.content');
  for (var i = 0; i < contents.length; i++) {
      contents[i].style.display = 'none';
  }
  document.getElementById('QoQResult').style.display = 'block';
}