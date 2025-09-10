document.addEventListener('DOMContentLoaded', () => {
    // === Funcionalidade do Menu Hambúrguer ===
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }

    // === Animações de Rolagem (IntersectionObserver) ===
    
    // Define os elementos que terão a animação de rolagem
    const animatedElements = document.querySelectorAll(
        'h1, h2, h3, p, .content-image, .content-image img, .btn-voltar, foote, section, .section-content, .integrante, .integrante-card, .btn-voltar, .btn-tentar-novamete'
    );

    const observer = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Adiciona a classe 'visible' para iniciar a animação e parar de observar
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 }); // O threshold define o ponto de disparo da animação

    // Começa a observar cada elemento animado
    animatedElements.forEach(element => {
        observer.observe(element);
    });
});


// gustavo
