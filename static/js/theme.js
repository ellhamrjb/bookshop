(function () {
    const root = document.documentElement;
    const toggleBtn = document.getElementById("theme-toggle");
    const STORAGE_KEY = "bookshop-theme";

    function applyTheme(theme) {
        root.setAttribute("data-theme", theme);
        toggleBtn.textContent = theme === "dark" ? "☀️" : "🌙";
    }

    // Load saved preference, or fall back to system preference
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
        applyTheme(saved);
    } else {
        const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
        applyTheme(prefersDark ? "dark" : "light");
    }

    toggleBtn.addEventListener("click", function () {
        const current = root.getAttribute("data-theme");
        const next = current === "dark" ? "light" : "dark";
        applyTheme(next);
        localStorage.setItem(STORAGE_KEY, next);
    });
})();