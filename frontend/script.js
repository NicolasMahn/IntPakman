window.onload = function () {
    var liste = document.getElementById("liste");
    var karte = document.getElementById("karte");
    liste.addEventListener("click", function () { liste.style.backgroundColor = "#FFCC00"; karte.style.backgroundColor = "gray"; });
    karte.addEventListener("click", function () { karte.style.backgroundColor = "#FFCC00"; liste.style.backgroundColor = "gray"; });
};
//# sourceMappingURL=script.js.map