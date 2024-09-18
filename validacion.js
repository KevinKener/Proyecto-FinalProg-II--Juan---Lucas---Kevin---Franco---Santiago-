function validarDatos(){
    let name = document.getElementById("name").value.trim(); /* me de contenido del campo */

    let email = document.getElementById("email").value.trim();

    let subject = document.getElementById("subject").value.trim();

    let message = document.getElementById("message").value.trim();

    /* Alertas
    alert(message);
    alert(subject);
    alert(name);
    alert(email);
    */


    // Expresiones regulares para validación
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;


    //Validacion de Asunto

    if (subject.length < 5){
        alert("El asunto tiene que tener al menos 5 caracteres")
        return false;
    }

    //Validar Nombre

    if (name.split(' ').length < 2) {
        alert("Ingrese el nombre completo");
        return false;
    }

    //Validar Mensaje

    if (message.length < 15) {
        alert("El mensaje tiene que tener al menos 15 caracteres para ser enviado");
        return false;
    }


    return true;
}

