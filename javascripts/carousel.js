(function () {
  function initCarousel(el) {
    var track = el.querySelector(".carousel-track");
    var slides = el.querySelectorAll(".carousel-slide");
    if (!track || slides.length === 0) return;

    var current = 0;
    var autoTimer = null;

    // Crear dots dinámicamente según el número real de slides
    var dotsEl = el.querySelector(".carousel-dots");
    dotsEl.innerHTML = "";
    slides.forEach(function (_, i) {
      var dot = document.createElement("button");
      dot.className = "carousel-dot" + (i === 0 ? " active" : "");
      dot.setAttribute("aria-label", "Imagen " + (i + 1));
      dot.addEventListener("click", function () { goTo(i); });
      dotsEl.appendChild(dot);
    });

    function updateDots() {
      dotsEl.querySelectorAll(".carousel-dot").forEach(function (dot, i) {
        dot.classList.toggle("active", i === current);
      });
    }

    function goTo(index) {
      current = ((index % slides.length) + slides.length) % slides.length;
      track.scrollTo({ left: track.clientWidth * current, behavior: "smooth" });
      updateDots();
    }

    el.querySelector(".carousel-prev").addEventListener("click", function () {
      goTo(current - 1);
    });
    el.querySelector(".carousel-next").addEventListener("click", function () {
      goTo(current + 1);
    });

    el.setAttribute("tabindex", "0");
    el.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft")  goTo(current - 1);
      if (e.key === "ArrowRight") goTo(current + 1);
    });

    function startAutoplay() {
      autoTimer = setInterval(function () { goTo(current + 1); }, 5000);
    }
    function stopAutoplay() {
      clearInterval(autoTimer);
    }

    el.addEventListener("mouseenter", stopAutoplay);
    el.addEventListener("mouseleave", startAutoplay);
    el.addEventListener("focusin",    stopAutoplay);
    el.addEventListener("focusout",   startAutoplay);

    startAutoplay();
  }

  function initAll() {
    // El atributo data-carousel-init evita inicializar dos veces el mismo elemento
    document.querySelectorAll(".party-carousel:not([data-carousel-init])").forEach(function (el) {
      el.setAttribute("data-carousel-init", "1");
      initCarousel(el);
    });
  }

  // Ejecutar inmediatamente: el script está al final del body,
  // el DOM ya existe aunque document$ aún no haya emitido.
  initAll();

  // Además subscribirse a document$ para que funcione con la navegación
  // SPA de MkDocs Material (cuando el usuario navega entre páginas).
  if (typeof document$ !== "undefined") {
    document$.subscribe(initAll);
  }
})();
