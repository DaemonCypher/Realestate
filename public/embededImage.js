!function() {
    "use strict";
    window.addEventListener("message", function(a) {
        if (void 0 !== a.data["datawrapper-height"]) {
            var e = document.querySelectorAll("iframe");
            for (var t in a.data["datawrapper-height"]) {
                for (var r = 0; r < e.length; r++) {
                    if (e[r].contentWindow === a.source) {
                        var i = a.data["datawrapper-height"][t] + "px";
                        e[r].style.height = i;
                    }
                }
            }
        }
    });
}();