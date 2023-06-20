var formulario = new Vue({
  el: '#formulario',
  data: {
    formData: {
      nombre: '',
      edad: '',
      traps: [],
    }
  },
  methods: {
    submitForm() {
      // Realiza la solicitud POST
      fetch("guardar", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(this.formData)
      })
      .then(response => {
        if (response.ok) {
          alert("Los datos se han enviado correctamente.");
          this.formData = {}; // Resetea el formulario
        } else {
          alert("Hubo un error al enviar los datos. Por favor, inténtalo de nuevo.");
        }
      })
      .catch(error => {
        alert("Hubo un error al enviar los datos. Por favor, inténtalo de nuevo.");
        console.log(error);
      });
    }
  }
});