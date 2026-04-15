document.addEventListener("DOMContentLoaded", () => {

    // =====================================================
    // 1. ENTRADA ESCALONADA — .fade-slide
    //    Para tarjetas de proyectos y skills (en cuadrícula)
    //    El CSS aplica transition-delay escalonado por nth-child
    // =====================================================

    const staggerElements = document.querySelectorAll(".fade-slide");

    const staggerObserver = new IntersectionObserver(
        (entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.1 }
    );

    staggerElements.forEach(el => staggerObserver.observe(el));


    // =====================================================
    // 2. SCROLL REVEAL — .fade-in-section
    //    Para secciones de texto (detalle de proyecto)
    //    Entran una a una al hacer scroll
    // =====================================================

    const sectionElements = document.querySelectorAll(".fade-in-section");

    const sectionObserver = new IntersectionObserver(
        (entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );

    sectionElements.forEach(el => sectionObserver.observe(el));

});
