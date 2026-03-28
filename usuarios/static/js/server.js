function handleCredentialResponse(response) {
  fetch(window.GOOGLE_LOGIN_URL || "/usuarios/google/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    credentials: "include",
    body: JSON.stringify({
      token: response.credential
    })
  })
    .then(async (res) => {
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || "Erro no login");
      }
      return data;
    })
    .then((data) => {
      console.log("Login OK:", data);
      window.location.href = "/";
    })
    .catch((err) => {
      console.error("Erro no login Google:", err);
      alert("Erro no servidor: " + err.message);
    });
}

window.addEventListener("load", function () {
  if (!window.GOOGLE_CLIENT_ID || window.GOOGLE_CLIENT_ID === "GOOGLE_CLIENT_ID") {
    console.error("GOOGLE_CLIENT_ID não configurado no HTML.");
    return;
  }

  if (!window.google || !google.accounts || !google.accounts.id) {
    console.error("Biblioteca do Google não carregou corretamente.");
    return;
  }

  google.accounts.id.initialize({
    client_id: window.GOOGLE_CLIENT_ID,
    callback: handleCredentialResponse,
    auto_select: false,
    itp_support: true,
    cancel_on_tap_outside: true
  });

  const googleButtonContainer = document.getElementById("google-signin-button");

  if (googleButtonContainer) {
    google.accounts.id.renderButton(
      googleButtonContainer,
      {
        theme: "outline",
        size: "large",
        shape: "pill",
        text: "continue_with",
        width: 260
      }
    );
  }
});