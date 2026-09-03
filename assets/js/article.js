const articleRoot = document.getElementById("articleRoot");
const articleTitle = document.getElementById("articleTitle");
const langSelect = document.getElementById("langSelect");

const ADMIN_EMAIL = "aphitekrop@gmail.com";
let articles = [];
let entriesById = {};

document.addEventListener("DOMContentLoaded", init);

async function init() {
  try {
    PyRef.loadUserData();
    PyRef.applyI18n();

    if (langSelect) {
      langSelect.value = PyRef.lang;
      langSelect.addEventListener("change", () => {
        PyRef.setLang(langSelect.value);
        PyRef.applyI18n();
        langSelect.value = PyRef.lang;
        renderArticle();
      });
    }

    const user = PyRef.getUser();
    const isAdmin = user && (user.email || "").toLowerCase() === ADMIN_EMAIL.toLowerCase();

    if (!isAdmin) {
      articleTitle.textContent = PyRef.t("entryNotFound");
      articleRoot.innerHTML = `<div class="empty">Доступ закрыт.<br>Статья доступна только модераторам.</div>`;
      return;
    }

    await loadArticles();
    await loadEntriesIndex();
    renderArticle();
  } catch (err) {
    console.error("article init error:", err);
    articleRoot.innerHTML = `<div class="empty">Ошибка загрузки статьи.</div>`;
  }
}

async function loadArticles() {
  const urls = ["data/articles.json", "articles.json"];
  for (const url of urls) {
    try {
      const r = await fetch(url, { cache: "no-cache" });
      if (!r.ok) continue;
      const d = await r.json();
      articles = Array.isArray(d) ? d : (d.articles || []);
      return;
    } catch (e) {}
  }
  articles = [];
}

async function loadEntriesIndex() {
  const urls = ["data/entries.json", "entries.json"];
  for (const url of urls) {
    try {
      const r = await fetch(url, { cache: "no-cache" });
      if (!r.ok) continue;
      const d = await r.json();
      const list = Array.isArray(d) ? d : (d.entries || []);
      entriesById = {};
      list.forEach(e => { entriesById[e.id] = e; });
      return;
    } catch (e) {}
  }
}

function getArticleId() {
  return new URLSearchParams(location.search).get("id");
}

function getArticle(id) {
  return articles.find(a => a.id === id) || null;
}

function renderArticle() {
  const id = getArticleId();
  const article = getArticle(id);

  if (!article) {
    articleTitle.textContent = PyRef.t("entryNotFound");
    articleRoot.innerHTML = `<div class="empty">${PyRef.t("entryNotFound")}</div>`;
    return;
  }

  articleTitle.textContent = PyRef.localize(article.title);

  articleRoot.innerHTML = `
    ${renderIntro(article)}
    ${renderLinks(article)}
    ${renderSteps(article)}
    ${renderImages(article)}
    ${relatedEntriesBlock(article)}
  `;
}

function renderIntro(article) {
  const introText = Array.isArray(article.intro)
    ? article.intro.map(item => `<p>${PyRef.escapeHtml(PyRef.localize(item))}</p>`).join("")
    : "";

  const tags = Array.isArray(article.tags) && article.tags.length
    ? `<div class="articleMeta">${article.tags.map(t => `<span class="tag">${PyRef.escapeHtml(t)}</span>`).join("")}</div>`
    : "";

  return `
    <article class="card">
      <div class="articleSummary">${PyRef.escapeHtml(PyRef.localize(article.summary))}</div>
      ${introText}
      ${tags}
    </article>
  `;
}

function renderLinks(article) {
  if (!Array.isArray(article.links) || !article.links.length) return "";

  const links = article.links.map(link => {
    const title = PyRef.localize(link.title) || link.url || link;
    const url = link.url || link;
    return `<a href="${PyRef.escapeHtml(url)}" target="_blank" rel="noopener">${PyRef.escapeHtml(title)}</a>`;
  }).join("");

  return `
    <article class="card">
      <div class="sectionTitle">${PyRef.t("links")}</div>
      <div class="articleLinks">${links}</div>
    </article>
  `;
}

function renderSteps(article) {
  if (!Array.isArray(article.steps) || !article.steps.length) return "";

  return article.steps.map((step, index) => {
    const title = step.title
      ? `<h2 class="stepTitle">${index + 1}. ${PyRef.escapeHtml(PyRef.localize(step.title))}</h2>`
      : "";

    const text = step.text
      ? `<div class="stepText">${PyRef.escapeHtml(PyRef.localize(step.text))}</div>`
      : "";

    const code = step.code
      ? `<pre>${PyRef.escapeHtml(step.code)}</pre>`
      : "";

    const screenshot = renderScreenshot(step.screenshot);

    return `
      <article class="card articleStep">
        ${title}
        ${text}
        ${code}
        ${screenshot}
      </article>
    `;
  }).join("");
}

function renderScreenshot(screenshot) {
  if (!screenshot) return "";

  if (screenshot.src) {
    return `
      <figure class="articleImage">
        <img src="${PyRef.escapeHtml(screenshot.src)}" alt="${PyRef.escapeHtml(PyRef.localize(screenshot.alt) || "Скриншот")}">
        ${screenshot.note ? `<figcaption class="screenshotNote">${PyRef.escapeHtml(PyRef.localize(screenshot.note))}</figcaption>` : ""}
      </figure>
    `;
  }

  return `
    <div class="screenshotPlaceholder">
      <div class="icon">📷</div>
      <div>${PyRef.t("screenshotPlaceholder")}</div>
      ${screenshot.note ? `<div class="screenshotNote">${PyRef.escapeHtml(PyRef.localize(screenshot.note))}</div>` : ""}
    </div>
  `;
}

function renderImages(article) {
  if (!Array.isArray(article.images) || !article.images.length) return "";

  const images = article.images.map(image => renderScreenshot(image)).join("");

  return `
    <article class="card">
      <div class="sectionTitle">${PyRef.t("images")}</div>
      ${images}
    </article>
  `;
}

function relatedEntriesBlock(article) {
  const ids = Array.isArray(article.entries) ? article.entries : [];
  const items = ids.map(id => entriesById[id]).filter(Boolean);
  if (!items.length) return "";

  const links = items.map(e => `
    <a class="relatedCard" href="entry.html?id=${encodeURIComponent(e.id)}">
      <strong>${PyRef.escapeHtml(e.name || e.id)}</strong>
      <div class="muted">${PyRef.escapeHtml(PyRef.localize(e.summary))}</div>
    </a>
  `).join("");

  return `
    <article class="card">
      <div class="label">${PyRef.t("relatedEntries")}</div>
      <div class="relatedGrid">${links}</div>
    </article>
  `;
}