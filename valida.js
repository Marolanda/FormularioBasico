document.getElementById("meuFormulario").addEventListener("submit", function (event) {
    event.preventDefault();
  
    const nome = document.getElementById("nome").value.trim();
    const email = document.getElementById("email").value.trim();
    const senha = document.getElementById("senha").value;
  
    let mensagem = "";
  
    if (nome.length < 3) {
      mensagem += "O nome deve ter pelo menos 3 caracteres.<br />";
    }
  
    const emailValido = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailValido.test(email)) {
      mensagem += "E-mail inválido.<br />";
    }
  
    const senhaValida = /^(?=.*[A-Z])(?=.*\d).{8,}$/;
    if (!senhaValida.test(senha)) {
      mensagem += "A senha deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula e um número.<br />";
    }
  
    document.getElementById("mensagem").innerHTML = mensagem;
  
    if (mensagem === "") {
      // Envia para o servidor Flask
      fetch("http://127.0.0.1:5000/cadastro", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ nome, email, senha }),
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === "sucesso") {
          alert("Servidor respondeu: " + data.mensagem);
        } else {
          document.getElementById("mensagem").innerHTML = data.mensagens.join("<br />");
        }
      })
      .catch(error => {
        console.error("Erro:", error);
        document.getElementById("mensagem").innerHTML = "Erro ao conectar com o servidor.";
      });
    }
  });
  