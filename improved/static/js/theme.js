const html = document.documentElement;
const themeToggle = document.getElementById("themeToggle");
const hamburger = document.getElementById("hamburger");
const mobileMenu = document.getElementById("mobileMenu");

// Theme
const savedTheme = localStorage.getItem("theme");
if (savedTheme) html.setAttribute("data-theme", savedTheme);
updateThemeIcon();

function updateThemeIcon() {
    if (themeToggle) {
        themeToggle.textContent = html.getAttribute("data-theme") === "dark" ? "🌙" : "☀️";
    }
}

if (themeToggle) {
    themeToggle.addEventListener("click", () => {
        const next = html.getAttribute("data-theme") === "dark" ? "light" : "dark";
        html.setAttribute("data-theme", next);
        localStorage.setItem("theme", next);
        updateThemeIcon();
    });
}

// Hamburger menu
if (hamburger && mobileMenu) {
    hamburger.addEventListener("click", () => {
        mobileMenu.classList.toggle("open");
        hamburger.textContent = mobileMenu.classList.contains("open") ? "✕" : "☰";
    });
}

// Active nav link highlight
document.querySelectorAll('.nav-links a, .mobile-menu a').forEach(link => {
    if (link.href === window.location.href) {
        link.style.color = 'var(--primary)';
        link.style.background = 'var(--primary-dim)';
    }
});
