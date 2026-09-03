const articlesRoot = document.getElementById("articlesRoot");
const articlesMeta = document.getElementById("articlesMeta");
const articleSearch = document.getElementById("articleSearch");
const langSelect = document.getElementById("langSelect");

const ADMIN_EMAIL = "aphitekrop@gmail.com";
let articles = [];

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
        renderArticles();
      });
    }

    if (articleSearch) articleSearch.addEventListener("input", renderArticles);

    const user = PyRef.getUser();
    const isAdmin = user && (user.email || "").toLowerCase() === ADMIN_EMAIL.toLowerCase();

    if (!isAdmin) {
      articlesRoot.innerHTML = `<div class="empty">Доступ закрыт.<br>Раздел доступен только модераторам.</div>`;
      return;
    }

    await loadArticles();
    renderArticles();
  } catch (err) {
    console.error("articles init error:", err);
    articlesRoot.innerHTML = `<div class="empty">Ошибка загрузки статей.</div>`;
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

function normalize(v) { return String(v ?? "").toLowerCase().replace(/\s+/g, " ").trim(); }

function matches(a, q) {
  const n = normalize(q);
  if (!n) return true;
  const text = normalize(JSON.stringify(a));
  return n.split(" ").filter(Boolean).every(p => text.includes(p));
}

function renderArticles() {
  const query = articleSearch ? articleSearch.value.trim() : "";

  const filtered = articles
    .slice()
    .sort((a, b) => (a.rank ?? 10000) - (b.rank ?? 10000))
    .filter(a => matches(a, query));

  if (articlesMeta) articlesMeta.textContent = `${PyRef.t("found")}: ${filtered.length}`;

  if (!filtered.length) {
    articlesRoot.innerHTML = `<div class="empty">${PyRef.t("nothingFound")}</div>`;
    return;
  }

  articlesRoot.innerHTML = filtered.map(articleCard).join("");
}

function articleCard(a) {
  const tags = Array.isArray(a.tags) && a.tags.length
    ? `<div class="articleMeta">${a.tags.map(t => `<span class="tag">${PyRef.escapeHtml(t)}</span>`).join("")}</div>`
    : "";

  return `
    <a class="card clickable articleCard" href="article.html?id=${encodeURIComponent(a.id)}">
      <h2 class="articleTitle">${PyRef.escapeHtml(PyRef.localize(a.title))}</h2>
      <div class="articleSummary">${PyRef.escapeHtml(PyRef.localize(a.summary))}</div>
      ${tags}
    </a>
  `;
}