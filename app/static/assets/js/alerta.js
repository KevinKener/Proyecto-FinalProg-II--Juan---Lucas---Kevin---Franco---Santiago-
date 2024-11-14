/** Alerta personalizadas */
function mensajeAlerta(msg, tipo_msg = '') {
    document.querySelector('.text-2').textContent = msg; // Establece el mensaje

    const toast = document.querySelector(".toast"),
          progress = document.querySelector(".progress"),
          closeIcon = document.querySelector(".close");

    // Aplica una clase basada en el tipo de mensaje
    toast.classList.add("active", tipo_msg);
    progress.classList.add("active");

    setTimeout(() => {
        toast.classList.remove("active", tipo_msg);
        progress.classList.remove("active");
    }, 5000); // Duración de la alerta (5 segundos)

    closeIcon.addEventListener("click", () => {
        toast.classList.remove("active", tipo_msg);
    });
}

/** Ocultando la alerta que se dispara sin el JavaScript */
document.addEventListener("DOMContentLoaded", function() {
    const alertas = document.querySelectorAll("#alertas .alert");

    // Ocultar cada alerta después de 5 segundos
    alertas.forEach(alert => {
        setTimeout(() => {
            alert.style.display = "none";
        }, 5000);
    });

    // Añadir funcionalidad de cierre para cada alerta
    alertas.forEach(alert => {
        const closeBtn = alert.querySelector(".close");
        if (closeBtn) {
            closeBtn.addEventListener("click", () => {
                alert.style.display = "none";
            });
        }
    });
});
