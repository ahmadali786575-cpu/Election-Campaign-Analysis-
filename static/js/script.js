console.log("script.js loaded");
function toggleSidebar() {

    const sidebar = document.getElementById("sidebar");
    const main = document.getElementById("main-content");

    sidebar.classList.toggle("hide");
    main.classList.toggle("full");

}
window.addEventListener("load", function () {

    const sidebar = document.getElementById("sidebar");
    const main = document.getElementById("main-content");

    if (sidebar) {
        sidebar.classList.remove("hide");
        sidebar.classList.remove("close");
    }

    if (main) {
        main.classList.remove("full");
        main.classList.remove("expand");
    }

});