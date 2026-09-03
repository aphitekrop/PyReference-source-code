#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LOGIN_HTML = '''<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#111827">
  <title>Вход — PyReference</title>
  <link rel="manifest" href="manifest.webmanifest">
  <link rel="icon" href="assets/icons/icon-192.png">
  <link rel="apple-touch-icon" href="assets/icons/icon-180.png">
  <link rel="stylesheet" href="assets/css/style.css?v=12">
</head>
<body>
  <header>
    <div class="top">
      <a class="iconBtn" href="index.html" aria-label="Назад">←</a>
      <h1 data-i18n="loginTitle">Вход</h1>
    </div>
  </header>

  <main style="padding: 16px; max-width: 600px; margin: 0 auto;">
    <div id="loginContent" class="card">
      <p data-i18n="loginDescription">Создайте аккаунт или войдите, чтобы сохранять избранное.</p>

      <form id="authForm" class="dialogBox" style="border: 0; padding: 0;">
        <label for="authName" data-i18n="name">Имя</label>
        <input id="authName" placeholder="Как к вам обращаться">

        <label for="authEmail" data-i18n="email">Email</label>
        <input id="authEmail" type="email" required placeholder="you@example.com">

        <label for="authPassword" data-i18n="password">Пароль</label>
        <input id="authPassword" type="password" minlength="6" placeholder="Минимум 6 символов">

        <div id="authError" class="authError" hidden></div>

        <div class="row">
          <button type="submit" data-action="register" data-i18n="register">Регистрация</button>
          <button type="submit" data-action="login" data-i18n="login">Войти</button>
        </div>
      </form>

      <div class="authDivider"><span>или</span></div>

      <div class="socialLogin">
        <button class="socialBtn" id="localLoginBtn">
          <span>📱</span>
          <span>Войти локально (без сервера)</span>
        </button>
        <button class="socialBtn" id="upgradeBtn" hidden>
          <span>☁️</span>
          <span>Привязать к серверу</span>
        </button>
        <button class="socialBtn" disabled>
          <span>🔵</span>
          <span>Войти через Google (скоро)</span>
        </button>
        <button class="socialBtn" disabled>
          <span>⚫</span>
          <span>Войти через GitHub (скоро)</span>
        </button>
      </div>

      <div class="authNote">
        <strong>Как это работает:</strong><br>
        • <em>Регистрация / Войти</em> — сохранит профиль на сервере, избранное синхронизируется.<br>
        • <em>Войти локально</em> — профиль и избранное хранятся только на этом устройстве.<br>
        • <em>Привязать к серверу</em> — если уже вошли локально, можно сохранить профиль на сервер.
      </div>
    </div>
  </main>

  <script src="assets/js/core.js?v=12"></script>
  <script src="assets/js/login.js?v=12"></script>
</body>
</html>
'''

LOGIN_JS = '''const authForm = document.getElementById("authForm");
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
'''


def main():
    (ROOT / "login.html").write_text(LOGIN_HTML, encoding="utf-8")

    js_dir = ROOT / "assets" / "js"
    js_dir.mkdir(parents=True, exist_ok=True)
    (js_dir / "login.js").write_text(LOGIN_JS, encoding="utf-8")

    print("Созданы:")
    print(" ", ROOT / "login.html")
    print(" ", js_dir / "login.js")


if __name__ == "__main__":
    main()