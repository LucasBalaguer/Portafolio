document.querySelectorAll('.project-card').forEach(card => {

    const maxTilt = 8; // grados máximos (pro, sutil)

    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();

        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const percentX = (x - centerX) / centerX;
        const percentY = (y - centerY) / centerY;

        const rotateY = percentX * maxTilt;
        const rotateX = percentY * -maxTilt;

        card.style.transform = `
            perspective(900px)
            rotateX(${rotateX}deg)
            rotateY(${rotateY}deg)
            translateY(-6px)
        `;

        /* brillo */
        card.style.setProperty('--x', `${x}px`);
        card.style.setProperty('--y', `${y}px`);
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = `
            perspective(900px)
            rotateX(0deg)
            rotateY(0deg)
            translateY(0)
        `;
    });

});
