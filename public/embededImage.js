/**
 * Anonymous function to handle iframe resizing based on the message event.
 * Listens for a postMessage event from DataWrapper iframes to adjust their height dynamically.
 * The function ensures strict mode and encapsulates the logic to prevent variable leakage.
 */
(function() {
    "use strict";

    /**
     * Event listener for 'message' event on the window object.
     * @param {MessageEvent} event - The message event which contains data and other details.
     */
    window.addEventListener("message", function(event) {
        // Check if the received message contains 'datawrapper-height' property
        if (event.data["datawrapper-height"]) {
            // Select all iframe elements on the page
            var iframes = document.querySelectorAll("iframe");

            // Loop over each property in 'datawrapper-height'
            for (var iframeId in event.data["datawrapper-height"]) {
                // Loop over each iframe element to find the correct one by matching the source
                for (var i = 0; i < iframes.length; i++) {
                    if (iframes[i].contentWindow === event.source) {
                        // Set the height of the matched iframe based on the data received in the message
                        var newHeight = event.data["datawrapper-height"][iframeId] + "px";
                        iframes[i].style.height = newHeight;
                    }
                }
            }
        }
    });

})();
