const glass = document.querySelector(".hero-glass");

if (glass) {
    glass.addEventListener("mousemove", (e) => {
        const rect = glass.getBoundingClientRect();

        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = ((y - centerY) / centerY) * -4;
        const rotateY = ((x - centerX) / centerX) * 4;

        glass.style.transform = `
            rotateX(${rotateX}deg)
            rotateY(${rotateY}deg)
        `;
    });

    glass.addEventListener("mouseleave", () => {
        glass.style.transform = `
            rotateX(0deg)
            rotateY(0deg)
        `;
    });
}
