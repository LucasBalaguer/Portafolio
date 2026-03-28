document.addEventListener("DOMContentLoaded", () => {
    const elements = document.querySelectorAll(".fade-slide");

    // Evitar re-animar si ya se ha animado en esta sesión
    const alreadyAnimated = sessionStorage.getItem("projectsAnimated");

    const observer = new IntersectionObserver(
        (entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    observer.unobserve(entry.target);
                }
            });
        },
        {
            threshold: 0.15
        }
    );

    if (!alreadyAnimated) {
        elements.forEach(el => observer.observe(el));
        sessionStorage.setItem("projectsAnimated", "true");
    } else {
        // Si ya se animó, mostrar directamente sin esperar
        elements.forEach(el => el.classList.add("visible"));
    }
});
