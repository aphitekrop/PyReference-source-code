const ADMIN_EMAIL = "aphitekrop@gmail.com";

let showFavoritesOnly = false;

const search = document.getElementById("search");
const typeFilter = document.getElementById("typeFilter");
const categoryFilter = document.getElementById("categoryFilter");
const list = document.getElementById("list");
const meta = document.getElementById("meta");

const menuBtn = document.getElementById("menuBtn");
const drawer = document.getElementById("drawer");
const drawerBackdrop = document.getElementById("drawerBackdrop");
const closeDrawerBtn = document.getElementById("closeDrawerBtn");

const userBox = document.getElementById("userBox");
const navHome = document.getElementById("navHome");
const navFavorites = document.getElementById("navFavorites");
const navArticles = document.getElementById("navArticles");
const installBtn = document.getElementById("installBtn");

const langSelect = document.getElementById("langSelect");
const notifyPython = document.getElementById("notifyPython");
const notifyNews = document.getElementById("notifyNews");
const pythonVersionBox = document.getElementById("pythonVersionBox");
const apiBaseInput = document.getElementById("apiBase");

const favFilterBtn = document.getElementById("favFilterBtn");

let deferredPrompt = null;

document.addEventListener("DOMContentLoaded", init);

async function init() {
  try {
    PyRef.loadUserData();
    await PyRef.pullFavorites().catch(() => {});
    PyRef.applyI18n();
    bindEvents();
    await loadData();
  } catch (err) {
    console.error("Init error:", err);
  }

  try {
    renderAll();
  } catch (err) {
    console.error("Render error:", err);
    list.innerHTML = `<div class="empty">Ошибка. Обновите страницу.</div>`;
  }
}

async function loadData() {
  try {
    await PyRef.loadEntries();
  } catch (error) {
    console.error(error);
    meta.textContent = "Error";
    list.innerHTML = `
      <div class="empty">
        Не удалось загрузить справочник.<br>
        <pre>python scripts/build_all.py</pre>
        <pre>python server.py</pre>
      </div>
    `;
  }
}

function bindEvents() {
  menuBtn.addEventListener("click", openDrawer);
  closeDrawerBtn.addEventListener("click", closeDrawer);
  drawerBackdrop.addEventListener("click", closeDrawer);

  navHome.addEventListener("click", () => {
    showFavoritesOnly = false;
    applyFilters();
    closeDrawer();
  });

  navFavorites.addEventListener("click", () => {
    if (!requireLogin()) return;
    showFavoritesOnly = true;
    applyFilters();
    closeDrawer();
  });

  favFilterBtn.addEventListener("click", () => {
    if (!requireLogin()) return;
    showFavoritesOnly = !showFavoritesOnly;
    applyFilters();
  });

  search.addEventListener("input", applyFilters);
  typeFilter.addEventListener("change", applyFilters);
  categoryFilter.addEventListener("change", applyFilters);

  langSelect.addEventListener("change", () => {
    PyRef.setLang(langSelect.value);
    renderAll();
  });

  if (apiBaseInput) {
    apiBaseInput.value = PyRef.getApiBase();
    apiBaseInput.addEventListener("change", () => {
      PyRef.setApiBase(apiBaseInput.value);
    });
  }

  notifyPython.addEventListener("change", () => {
    PyRef.notificationSettings.python = notifyPython.checked;
    PyRef.saveNotificationSettings();
  });

  list.addEventListener("click", event => {
    const favoriteButton = event.target.closest("[data-action='favorite']");

    if (favoriteButton) {
      event.preventDefault();
      const cardElement = event.target.closest("[data-id]");
      if (!cardElement) return;

      const changed = PyRef.toggleFavorite(cardElement.dataset.id);
      if (!changed) {
        location.href = "login.html";
        return;
      }
      applyFilters();
      return;
    }

    const cardElement = event.target.closest("[data-id]");
    if (!cardElement) return;
    location.href = `entry.html?id=${encodeURIComponent(cardElement.dataset.id)}`;
  });

  userBox.addEventListener("click", event => {
    const actionButton = event.target.closest("[data-action]");
    if (!actionButton) return;

    if (actionButton.dataset.action === "login") {
      location.href = "login.html";
    }
    if (actionButton.dataset.action === "logout") {
      PyRef.logout();
      showFavoritesOnly = false;
      renderAll();
    }
  });

  window.addEventListener("beforeinstallprompt", event => {
    event.preventDefault();
    deferredPrompt = event;
    installBtn.hidden = false;
  });

  installBtn.addEventListener("click", async () => {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    await deferredPrompt.userChoice;
    deferredPrompt = null;
    installBtn.hidden = true;
  });

  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("sw.js").catch(() => {});
    });
  }
}

function requireLogin() {
  if (!PyRef.getUser()) {
    location.href = "login.html";
    return false;
  }
  return true;
}

function openDrawer() { drawer.classList.add("open"); }
function closeDrawer() { drawer.classList.remove("open"); }

function renderAll() {
  PyRef.applyI18n();
  langSelect.value = PyRef.lang;
  if (apiBaseInput) apiBaseInput.value = PyRef.getApiBase();
  renderUserBox();
  renderPythonVersionBox();
  syncNotificationCheckboxes();
  initFilters();
  applyFilters();
}

function renderUserBox() {
  const user = PyRef.getUser();

  if (user) {
    const isAdmin = (user.email || "").toLowerCase() === ADMIN_EMAIL;

    let html = `
      <div><strong>${PyRef.escapeHtml(user.name)}</strong></div>
      <div class="muted">${PyRef.escapeHtml(user.email)}</div>
    `;
    if (user.local) html += `<div class="adminBadge">Локальный профиль</div>`;
    if (isAdmin) html += `<div class="adminBadge">Модератор</div>`;

    html += `<button class="menuBtn" data-action="logout">${PyRef.t("logout")}</button>`;
    userBox.innerHTML = html;

    if (navArticles) {
      if (isAdmin) {
        navArticles.removeAttribute("disabled");
        navArticles.setAttribute("href", "articles.html");
        navArticles.textContent = PyRef.t("articles");
      } else {
        navArticles.setAttribute("disabled", "true");
        navArticles.removeAttribute("href");
        navArticles.textContent = PyRef.t("articles") + " (закрыто)";
      }
    }
  } else {
    userBox.innerHTML = `
      <button class="menuBtn" data-action="login">${PyRef.t("login")}</button>
      <div class="muted">${PyRef.t("loginRequired")}</div>
    `;

    if (navArticles) {
      navArticles.setAttribute("disabled", "true");
      navArticles.removeAttribute("href");
      navArticles.textContent = PyRef.t("articles") + " (закрыто)";
    }
  }
}

function renderPythonVersionBox() {
  const versions = Array.isArray(PyRef.state.meta.pythonVersions) ? PyRef.state.meta.pythonVersions : [];
  const latest = PyRef.getLatestPythonVersion();
  let html = `<div class="label">${PyRef.t("latestPython")}</div>`;
  if (latest) html += `<div><strong>${PyRef.escapeHtml(latest.version)}</strong> <span class="muted">${PyRef.escapeHtml(latest.status || "")}</span></div>`;
  if (versions.length) html += `<div class="muted">${versions.map(v => PyRef.escapeHtml(v.version)).join(", ")}</div>`;
  pythonVersionBox.innerHTML = html;
}

function syncNotificationCheckboxes() {
  notifyPython.checked = Boolean(PyRef.notificationSettings.python);
  notifyNews.checked = Boolean(PyRef.notificationSettings.news);
}

function initFilters() {
  fillSelect(typeFilter, PyRef.uniqueSorted(PyRef.state.entries.map(e => e.type)), PyRef.t("allTypes"));
  fillSelect(categoryFilter, PyRef.uniqueSorted(PyRef.state.entries.map(e => e.category)), PyRef.t("allCategories"));
}

function fillSelect(select, values, allLabel) {
  const current = select.value;
  const options = values.map(v => `<option value="${PyRef.escapeHtml(v)}">${PyRef.escapeHtml(v)}</option>`).join("");
  select.innerHTML = `<option value="">${PyRef.escapeHtml(allLabel)}</option>${options}`;
  if (current) select.value = current;
}

function applyFilters() {
  const query = search.value.trim();
  const type = typeFilter.value;
  const category = categoryFilter.value;

  const sorted = PyRef.state.entries.slice().sort((a, b) => {
    const ra = a.rank ?? 10000, rb = b.rank ?? 10000;
    if (ra !== rb) return ra - rb;
    return String(a.name || "").toLowerCase().localeCompare(String(b.name || "").toLowerCase());
  });

  let filtered = sorted.filter(e =>
    (!type || e.type === type) &&
    (!category || e.category === category) &&
    PyRef.matches(e, query)
  );

  if (showFavoritesOnly) filtered = filtered.filter(e => PyRef.isFavorite(e.id));

  renderList(filtered);
  updateFavFilterButton();
}

function updateFavFilterButton() {
  favFilterBtn.textContent = showFavoritesOnly ? "★" : "☆";
  favFilterBtn.classList.toggle("active", showFavoritesOnly);
}

function renderList(items) {
  meta.textContent = `${PyRef.t("found")}: ${items.length}`;
  if (!items.length) {
    list.innerHTML = `<div class="empty">${showFavoritesOnly ? PyRef.t("noFavorites") : PyRef.t("nothingFound")}</div>`;
    return;
  }
  list.innerHTML = items.slice(0, 200).map(card).join("");
}

function card(entry) {
  const favorite = PyRef.isFavorite(entry.id);
  return `
    <article class="card clickable" data-id="${PyRef.escapeHtml(entry.id)}">
      <div class="cardHead">
        <div>
          <h2>${PyRef.escapeHtml(entry.name || entry.id)}</h2>
          <div class="category">${PyRef.escapeHtml(entry.type || "entry")} • ${PyRef.escapeHtml(entry.category || "")}</div>
        </div>
        <div class="cardActions">
          <button class="iconBtn ${favorite ? "active" : ""}" data-action="favorite" aria-label="Favorite">${favorite ? "★" : "☆"}</button>
        </div>
      </div>
      <p>${PyRef.escapeHtml(PyRef.localize(entry.summary))}</p>
    </article>
  `;
}