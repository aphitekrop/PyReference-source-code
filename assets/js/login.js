const authForm = document.getElementById("authForm");
const authName = document.getElementById("authName");
const authEmail = document.getElementById("authEmail");
const authPassword = document.getElementById("authPassword");
const authError = document.getElementById("authError");
const localLoginBtn = document.getElementById("localLoginBtn");
const upgradeBtn = document.getElementById("upgradeBtn");

document.addEventListener("DOMContentLoaded", init);

function init() {
  PyRef.loadUserData();
  PyRef.applyI18n();

  const user = PyRef.getUser();

  if (user) {
    if (user.local) {
      authEmail.value = user.email;
      authName.value = user.name;
      upgradeBtn.hidden = false;
      localLoginBtn.hidden = true;
    } else {
      location.href = "index.html";
      return;
    }
  }

  authForm.addEventListener("submit", async event => {
    event.preventDefault();
    const action = event.submitter ? event.submitter.dataset.action : "login";
    const name = authName.value.trim();
    const email = authEmail.value.trim();
    const password = authPassword.value;

    authError.hidden = true;

    if (!email) {
      authError.textContent = "Введите email";
      authError.hidden = false;
      return;
    }

    try {
      const result = action === "register"
        ? await PyRef.register(name || email.split("@")[0], email, password)
        : await PyRef.login(email, password);

      if (result && result.local) {
        alert("Вход выполнен локально. Избранное будет храниться на этом устройстве.");
      }

      location.href = "index.html";
    } catch (err) {
      authError.textContent = err.message || "Ошибка входа";
      authError.hidden = false;
    }
  });

  localLoginBtn.addEventListener("click", () => {
    const name = authName.value.trim();
    const email = authEmail.value.trim() || "local@device.local";

    PyRef.loginLocal(name || email.split("@")[0], email);
    alert("Локальный профиль создан. Избранное хранится на этом устройстве.");
    location.href = "index.html";
  });

  upgradeBtn.addEventListener("click", async () => {
    const email = authEmail.value.trim();
    const password = authPassword.value;

    authError.hidden = true;

    if (!email || !password) {
      authError.textContent = "Введите email и пароль";
      authError.hidden = false;
      return;
    }

    try {
      await PyRef.upgradeLocal(email, password);
      alert("Профиль успешно привязан к серверу!");
      location.href = "index.html";
    } catch (err) {
      authError.textContent = err.message || "Ошибка привязки";
      authError.hidden = false;
    }
  });
}