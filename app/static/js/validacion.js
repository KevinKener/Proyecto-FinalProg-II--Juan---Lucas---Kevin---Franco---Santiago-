document.addEventListener("DOMContentLoaded", () =>{
    const form = document.getElementById("contactForm");
    form.addEventListener("submit", function (evento){
            let valido = true;

            let name = document.getElementById("name").value.trim(); /* me de contenido del campo */
            let email = document.getElementById("email").value.trim();
            let subject = document.getElementById("subject").value.trim();
            let message = document.getElementById("message").value.trim();
            
            let primerCampoConError = false;

            // Expresiones regulares para validación
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
            //Validar Nombre
        
            if (name.split(' ').length < 2) {
                valido = false
                mostrarError("errorName", "El nombre debe tener al menos 2 palabras")
                if(!primerCampoConError) primerCampoConError = document.getElementById("name");
            }   
            //Validacion de email
            
            if (!emailRegex.test(email)){
                valido = false
                mostrarError("errorEmail" , "El correo electronico no es valido");
                if(!primerCampoConError) primerCampoConError = document.getElementById("email");
            } else if (email.length < 5 || email.length > 254 ){
                valido = false
                mostrarError("errorEmail" , "La longitud del correo electrónico debe estar entre 5 y 254 caracteres.");
                if(!primerCampoConError) primerCampoConError = document.getElementById("email");
            }
            //Validacion de Asunto
            if (subject.length < 5) {
                valido = false
                mostrarError("errorSubject", "El asunto debe tener al menos 5 caracteres")
                if(!primerCampoConError) primerCampoConError = document.getElementById("subject");
            }  
            if (message.length < 15) {
                valido = false
                mostrarError("errorMessage", "El mensaje es demasiado corto ingrese un mensaje con al menos 15 caracteres")
                if(!primerCampoConError) primerCampoConError = document.getElementById("message");
            }  
            if(!valido){
                evento.preventDefault();
                if(primerCampoConError) primerCampoConError.focus()
            }
            else{
                alert("Envio Exitoso!!");
                location.reload();
            }
    });
    //Eventos input
    document.getElementById("name").addEventListener("input", () => validarNombre());
    document.getElementById("email").addEventListener("input", () => validarEmail());
    document.getElementById("subject").addEventListener("input", () => validarAsunto());
    document.getElementById("message").addEventListener("input", () => validarMensaje());

    //Funcion validar nombre
    function validarNombre(name) {
        if (name.split(' ').length >= 2) {
            ocultarError("errorName");
        } else {
            mostrarError("errorName", "El nombre debe tener al menos 2 palabras");
        }
    }
    //Funcion validar Email
    function validarEmail(email) {
        if (emailRegex.test(email) && email.length >= 5 && email.length <= 254) {
            ocultarError("errorEmail");
        } else if (!emailRegex.test(email)) {
            mostrarError("errorEmail", "El correo electrónico no es válido");
        } else {
            mostrarError("errorEmail", "La longitud del correo electrónico debe estar entre 5 y 254 caracteres.");
        }
    }
    //funcion validar asunto
    function validarAsunto(subject) {
        if (subject.length >= 5){
            ocultarError("errorSubject")
        } else{
            mostrarError("errorSubject", "El asunto debe tener al menos 5 caracteres")            
        }
    }
    //funcion validar mensaje
    function validarMensaje(message) {
        if(message.length > 15){
            ocultarError("errorMessage")
        }else{
            mostrarError("errorMessage", "El mensaje es demasiado corto ingrese un mensaje con al menos 15 caracteres")
        }
    }
    // Función para mostrar errores
    function mostrarError(id, mensaje) {
        const errorElement = document.getElementById(id);
        errorElement.textContent = mensaje;
        errorElement.classList.add("error-text");
    }

    // Función para ocultar los mensajes de error
    function ocultarError(id) {
        const errorElement = document.getElementById(id);
        errorElement.textContent = ""; // Borra el contenido del mensaje de error
    }    
});