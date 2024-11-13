const nombreIngresado = document.getElementById("name");
const emailIngresado = document.getElementById("email");
const msjIngresado = document.getElementById("message");
const asuntoIngresado = document.getElementById("subject");

const nombreError = document.getElementById("errorName");
const emailError = document.getElementById("errorEmail");
const msjError = document.getElementById("errorMessage");
const asuntoError = document.getElementById("errorSubject");

// Declaro funciones de validación

function validarNombre() {
  const ERLetras = /^[A-Za-z\s]+$/;
  const nombre = nombreIngresado.value.trim();

  //validaciones
  if (nombre === "") {
    nombreError.textContent = "Ingrese nombre";
    return false;
  }
  if (nombre.split(' ').length < 2)
  {
    nombreError.textContent = "El nombre debe tener al menos 2 palabras";
    return false;
  }
  if (!ERLetras.test(nombre)) {
    nombreError.textContent = "El nombre no debe contener caracteres especiales";
    return false;
  }
  if (nombre.length < 3) {
    nombreError.textContent = "El nombre debe tener al menos 3 caracteres";
    return false;
  }

  nombreError.textContent = ""; //si todo esta okey, limpia el contenido de la clase del error (es decir, que no aparezca más)
  return true;
}

function validarEmail() {
  const EREmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const email = emailIngresado.value.trim();

  //Validaciones
  if (email === "") {
    emailError.textContent = "Ingrese email";
    return false;
  }
  if (!EREmail.test(email)) {
    emailError.textContent = "Email inválido. Verifique el formato";
    return false;
  }

  emailError.textContent = "";
  return true;
}

function validarAsunto() {
  const asunto = asuntoIngresado.value.trim();

  //Validaciones
  if (asunto.length < 5) {
    asuntoError.textContent = "El asunto debe tener al menos 5 caracteres";
    return false;
  }

  asuntoError.textContent = "";
  return true;
}

function validarMensaje() {
  const msj = msjIngresado.value.trim();

  //Validaciones
  if (msj.length < 10) {
    msjError.textContent = "El mensaje debe tener al menos 10 caracteres";
    return false;
  }

  msjError.textContent = "";
  return true;
}

// Agrego evento blur a cada input, esto hará que cuando se desenfoque muestre inmediatamente si hay algún error

nombreIngresado.addEventListener("blur", validarNombre);
emailIngresado.addEventListener("blur", validarEmail);
asuntoIngresado.addEventListener("blur", validarAsunto);
msjIngresado.addEventListener("blur", validarMensaje);


// Por último, solo queda prevenir que el formulario se envíe teniendo errores con la línea 153
// De hecho, no sólo se debe prevenir si no que al llamar a cada una de las funciones de validación
// se marcan los errores de aquellos inputs que no hayan sido enfocadas antes (lo que no arrojaría mensaje de error)

const formulario = document.getElementById("contactForm");

formulario.addEventListener("submit", function (event) {
  event.preventDefault();
  const validez_nombre = validarNombre();
  const validez_email = validarEmail();
  const validez_asunto = validarAsunto();
  const validez_msj = validarMensaje();

  if (validez_nombre && validez_email && validez_asunto && validez_msj) {
    formulario.submit();
    alert("Formulario enviado");
  }
});