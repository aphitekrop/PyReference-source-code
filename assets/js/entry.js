const entryTitle = document.getElementById("entryTitle");
const entryRoot = document.getElementById("entryRoot");
const favBtn = document.getElementById("favBtn");
const langSelect = document.getElementById("langSelect");

let articlesById = {};

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
        renderEntry();
      });
    }

    if (favBtn) {
      favBtn.addEventListener("click", () => {
        const id = getEntryId();
        const changed = PyRef.toggleFavorite(id);
        if (!changed) { location.href = "index.html?login=1"; return; }
        updateFavoriteButton(id);
      });
    }

    await PyRef.loadEntries();
    await loadArticlesIndex();
    renderEntry();
  } catch (error) {
    console.error("entry init error:", error);
    entryRoot.innerHTML = `<div class="empty">Не удалось загрузить карточку.</div>`;
  }
}

async function loadArticlesIndex() {
  const urls = ["data/articles.json", "articles.json"];
  for (const url of urls) {
    try {
      const r = await fetch(url, { cache: "no-cache" });
      if (!r.ok) continue;
      const d = await r.json();
      const list = Array.isArray(d) ? d : (d.articles || []);
      articlesById = {};
      list.forEach(a => { articlesById[a.id] = a; });
      return;
    } catch (e) {}
  }
}

function getEntryId() {
  return new URLSearchParams(location.search).get("id");
}

function updateFavoriteButton(id) {
  const f = PyRef.isFavorite(id);
  favBtn.textContent = f ? "★" : "☆";
  favBtn.classList.toggle("active", f);
}

function renderEntry() {
  const id = getEntryId();
  const entry = PyRef.getEntry(id);

  if (!entry) {
    entryTitle.textContent = PyRef.t("entryNotFound");
    entryRoot.innerHTML = `<div class="empty">${PyRef.t("entryNotFound")}</div>`;
    return;
  }

  entryTitle.textContent = entry.name || entry.id;
  updateFavoriteButton(id);

  entryRoot.innerHTML = `
    <article class="card">
      <div class="category">${PyRef.escapeHtml(entry.type || "entry")} • ${PyRef.escapeHtml(entry.category || "")}</div>
      <p>${PyRef.escapeHtml(PyRef.localize(entry.summary))}</p>
      <div class="detailsBody">
        ${syntaxBlock(entry)}
        ${paramsBlock(entry)}
        ${returnsBlock(entry)}
        ${errorsBlock(entry)}
        ${examplesBlock(entry)}
        ${versionBlock(entry)}
        ${tagsBlock(entry)}
        ${linksBlock(entry)}
      </div>
    </article>
    ${relatedSection("alternatives", entry.related && entry.related.alternatives)}
    ${relatedSection("complements", entry.related && entry.related.complements)}
    ${relatedSection("seealso", entry.related && entry.related.seealso)}
    ${relatedArticlesBlock(entry)}
  `;
}

function section(title, html) {
  if (!html) return "";
  return `<div><div class="label">${title}</div>${html}</div>`;
}

function syntaxBlock(e) { return e.syntax ? section(PyRef.t("syntax"), `<pre>${PyRef.escapeHtml(e.syntax)}</pre>`) : ""; }

function paramsBlock(e) {
  if (!Array.isArray(e.params) || !e.params.length) return "";
  const items = e.params.map(p => {
    const d = p.default ? ` = <code>${PyRef.escapeHtml(String(p.default))}</code>` : "";
    const t = p.type ? ` <span class="muted">(${PyRef.escapeHtml(p.type)})</span>` : "";
    return `<li><code>${PyRef.escapeHtml(p.name)}</code>${d}${t}: ${PyRef.escapeHtml(PyRef.localize(p.description))}</li>`;
  }).join("");
  return section(PyRef.t("params"), `<ul class="params">${items}</ul>`);
}

function returnsBlock(e) { return e.returns ? section(PyRef.t("returns"), `<div>${PyRef.escapeHtml(PyRef.localize(e.returns))}</div>`) : ""; }

function errorsBlock(e) {
  if (!Array.isArray(e.errors) || !e.errors.length) return "";
  const items = e.errors.map(er => `<li><code>${PyRef.escapeHtml(er.type)}</code>: ${PyRef.escapeHtml(PyRef.localize(er.when || er.description || ""))}</li>`).join("");
  return section(PyRef.t("errors"), `<ul class="params">${items}</ul>`);
}

function examplesBlock(e) {
  let items = [];
  if (Array.isArray(e.examples) && e.examples.length) items = e.examples;
  else if (e.example) items = [e.example];
  if (!items.length) return "";
  const html = items.map(ex => {
    if (typeof ex === "string") return `<pre>${PyRef.escapeHtml(ex)}</pre>`;
    const t = PyRef.localize(ex.title);
    return `${t ? `<div class="muted">${PyRef.escapeHtml(t)}</div>` : ""}<pre>${PyRef.escapeHtml(ex.code || "")}</pre>`;
  }).join("");
  return section(PyRef.t("examples"), html);
}

function versionBlock(e) {
  if (!e.version) return "";
  const parts = [];
  if (e.version.since) parts.push(`<span>${PyRef.t("since")}: <code>${PyRef.escapeHtml(e.version.since)}</code></span>`);
  if (e.version.deprecated) parts.push(`<span>${PyRef.t("deprecated")}: <code>${PyRef.escapeHtml(e.version.deprecated)}</code></span>`);
  if (e.version.removed) parts.push(`<span>${PyRef.t("removed")}: <code>${PyRef.escapeHtml(e.version.removed)}</code></span>`);
  if (e.version.checked) parts.push(`<span>${PyRef.t("checked")}: <code>${PyRef.escapeHtml(e.version.checked)}</code></span>`);
  if (!parts.length) return "";
  return section(PyRef.t("version"), `<div class="versionLine">${parts.join("")}</div>`);
}

function tagsBlock(e) {
  if (!Array.isArray(e.tags) || !e.tags.length) return "";
  return section(PyRef.t("tags"), `<div class="tags">${e.tags.map(t => `<span class="tag">${PyRef.escapeHtml(t)}</span>`).join("")}</div>`);
}

function linksBlock(e) {
  if (!Array.isArray(e.links) || !e.links.length) return "";
  return section(PyRef.t("links"), e.links.map(l => `<div><a href="${PyRef.escapeHtml(l)}" target="_blank" rel="noopener">${PyRef.escapeHtml(l)}</a></div>`).join(""));
}

function relatedSection(key, items) {
  if (!Array.isArray(items) || !items.length) return "";
  return `<article class="card"><div class="label">${PyRef.t(key)}</div><div class="relatedGrid">${items.map(relatedItemHtml).join("")}</div></article>`;
}

function relatedItemHtml(item) {
  if (typeof item === "string") item = { id: item };
  const note = item.note ? `<div class="muted">${PyRef.escapeHtml(PyRef.localize(item.note))}</div>` : "";
  if (item.id) {
    const e = PyRef.getEntry(item.id);
    if (e) return `<a class="relatedCard" href="entry.html?id=${PyRef.escapeHtml(e.id)}"><strong>${PyRef.escapeHtml(e.name || e.id)}</strong><div class="muted">${PyRef.escapeHtml(PyRef.localize(e.summary))}</div>${note}</a>`;
  }
  return `<div class="relatedCard"><strong>${PyRef.escapeHtml(item.name || item.id || "")}</strong>${item.syntax ? `<pre>${PyRef.escapeHtml(item.syntax)}</pre>` : ""}${note}</div>`;
}

function relatedArticlesBlock(entry) {
  const ids = Array.isArray(entry.articles) ? entry.articles : [];
  const items = ids.map(id => articlesById[id]).filter(Boolean);
  if (!items.length) return "";
  const links = items.map(a => `<a class="relatedCard" href="article.html?id=${encodeURIComponent(a.id)}"><strong>${PyRef.escapeHtml(PyRef.localize(a.title))}</strong><div class="muted">${PyRef.escapeHtml(PyRef.localize(a.summary))}</div></a>`).join("");
  return `<article class="card"><div class="label">${PyRef.t("relatedArticles")}</div><div class="relatedGrid">${links}</div></article>`;
}