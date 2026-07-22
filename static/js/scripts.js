function toggleSidebar() {

    const sidebar = document.getElementById("sidebar");
    const main = document.getElementById("main-content");

    sidebar.classList.toggle("hide");
    main.classList.toggle("full");

}