(function () {
  function initCarousel() {
    if (typeof Swiper === "undefined") return;
    var el = document.querySelector(".party-carousel");
    if (!el) return;

    // Destruir instancia previa si existe (navegación SPA de Material)
    if (el.swiper) el.swiper.destroy(true, true);

    new Swiper(".party-carousel", {
      loop: true,
      slidesPerView: 1,
      pagination: {
        el: ".party-carousel .swiper-pagination",
        clickable: true,
      },
      navigation: {
        nextEl: ".party-carousel .swiper-button-next",
        prevEl: ".party-carousel .swiper-button-prev",
      },
      autoplay: {
        delay: 5000,
        disableOnInteraction: false,
        pauseOnMouseEnter: true,
      },
      keyboard: { enabled: true },
    });
  }

  // document$ es el observable de navegación de MkDocs Material
  // Se dispara en cada carga de página (incluida la primera)
  if (typeof document$ !== "undefined") {
    document$.subscribe(initCarousel);
  } else {
    document.addEventListener("DOMContentLoaded", initCarousel);
  }
})();
