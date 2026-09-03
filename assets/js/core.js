const DEFAULT_API_BASE = "https://Aphitekrop.pythonanywhere.com";
const PyRef = (() => {
  const I18N = {
    ru: {
      appTitle: "PyReference", searchPlaceholder: "Поиск: print, if, json, pip, ipconfig...",
      allTypes: "Все типы", allCategories: "Все категории", found: "Найдено",
      nothingFound: "Ничего не найдено", noFavorites: "В избранном пока пусто",
      menu: "Меню", home: "Справочник", favorites: "Избранное", install: "Установить приложение",
      language: "Язык", notifications: "Уведомления",
      notifyPython: "Сообщать о новых версиях Python", notifyNews: "Новости программирования (скоро)",
      login: "Войти", logout: "Выйти", loginTitle: "Вход",
      loginDescription: "Если сервер недоступен, вход выполняется локально.",
      name: "Имя", email: "Email", password: "Пароль", register: "Регистрация", cancel: "Отмена",
      syntax: "Синтаксис", params: "Параметры", returns: "Возвращает", errors: "Ошибки",
      examples: "Примеры", version: "Версии Python", since: "Доступно с", deprecated: "Устарело с",
      removed: "Удалено в", checked: "Проверено на", tags: "Теги", links: "Ссылки",
      latestPython: "Версии Python", pythonVersionBanner: "Доступна новая версия Python", later: "Позже",
      loginRequired: "Войдите, чтобы сохранять избранное",
      alternatives: "Альтернативы", complements: "Дополнения", seealso: "Смотрите также",
      back: "Назад", entryNotFound: "Карточка не найдена",
      articles: "Полезные статьи", articlesSearchPlaceholder: "Поиск статей...",
      screenshotPlaceholder: "Место для скриншота",
      relatedArticles: "Полезные статьи по теме", relatedEntries: "Связанные карточки справочника",
      server: "Сервер для синхронизации"
    },
    en: {
      appTitle: "PyReference", searchPlaceholder: "Search: print, if, json, pip...",
      allTypes: "All types", allCategories: "All categories", found: "Found",
      nothingFound: "Nothing found", noFavorites: "Favorites are empty",
      menu: "Menu", home: "Reference", favorites: "Favorites", install: "Install app",
      language: "Language", notifications: "Notifications",
      notifyPython: "Notify about new Python versions", notifyNews: "Programming news (soon)",
      login: "Sign in", logout: "Sign out", loginTitle: "Sign in",
      loginDescription: "If the server is unavailable, you sign in locally.",
      name: "Name", email: "Email", password: "Password", register: "Register", cancel: "Cancel",
      syntax: "Syntax", params: "Parameters", returns: "Returns", errors: "Errors",
      examples: "Examples", version: "Python versions", since: "Since", deprecated: "Deprecated since",
      removed: "Removed in", checked: "Checked on", tags: "Tags", links: "Links",
      latestPython: "Python versions", pythonVersionBanner: "New Python version is available", later: "Later",
      loginRequired: "Sign in to save favorites",
      alternatives: "Alternatives", complements: "Complements", seealso: "See also",
      back: "Back", entryNotFound: "Entry not found",
      articles: "Useful articles", articlesSearchPlaceholder: "Search articles...",
      screenshotPlaceholder: "Screenshot placeholder",
      relatedArticles: "Related articles", relatedEntries: "Related reference cards",
      server: "Sync server"
    }
  };

  let lang = localStorage.getItem("pyref_lang") || "ru";
  let currentUser = JSON.parse(localStorage.getItem("pyref_current_user") || "null");
  let token = localStorage.getItem("pyref_token") || null;
  let favorites = new Set();
  let notificationSettings = { python: false, news: false };
  const state = { meta: {}, entries: [] };

  function t(k){ return (I18N[lang]&&I18N[lang][k])||I18N.ru[k]||k; }
  function setLang(v){ lang=v; localStorage.setItem("pyref_lang",lang); }
  function localize(v){ if(v==null)return""; if(typeof v==="string"||typeof v==="number")return String(v); if(Array.isArray(v))return v.map(localize).join(", "); if(typeof v==="object")return v[lang]||v.ru||v.en||Object.values(v)[0]||""; return String(v); }
  function escapeHtml(v){ return String(v??"").replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&#039;"); }
  function normalize(v){ return String(v??"").toLowerCase().replace(/\s+/g," ").trim(); }

  function getApiBase(){ return (localStorage.getItem("pyref_api_base")||"").replace(/\/+$/,""); }
  function setApiBase(v){ localStorage.setItem("pyref_api_base",(v||"").trim()); }

  function favoritesKey(){ return `pyref_favorites_${currentUser?currentUser.email:"guest"}`; }
  function notificationsKey(){ return `pyref_notifications_${currentUser?currentUser.email:"guest"}`; }
  function loadFavorites(){ if(!currentUser){favorites=new Set();return;} try{favorites=new Set(JSON.parse(localStorage.getItem(favoritesKey())||"[]"));}catch{favorites=new Set();} }
  function loadNotificationSettings(){ try{notificationSettings={python:false,news:false,...JSON.parse(localStorage.getItem(notificationsKey())||"{}")};}catch{notificationSettings={python:false,news:false};} }
  function loadUserData(){ loadFavorites(); loadNotificationSettings(); }
  function saveFavorites(){ if(!currentUser)return; localStorage.setItem(favoritesKey(),JSON.stringify([...favorites])); }
  function saveNotificationSettings(){ localStorage.setItem(notificationsKey(),JSON.stringify(notificationSettings)); }

  async function api(path, options={}){
    const base = getApiBase();
    const url = base ? base+path : path;
    const headers = {"Content-Type":"application/json"};
    if(token) headers["Authorization"]="Bearer "+token;

    let res;
    try{ res = await fetch(url,{...options,headers}); }
    catch(e){ const err=new Error("offline"); err.code="offline"; throw err; }

    const text = await res.text();
    let data=null;
    try{ data=JSON.parse(text); }
    catch(e){ const err=new Error("offline"); err.code="offline"; throw err; }

    if(!res.ok){ const err=new Error((data&&data.error)||("HTTP "+res.status)); err.code="http"; err.status=res.status; throw err; }
    return data;
  }

  function enterLocal(name,email){
    currentUser={ name: name||email.split("@")[0], email };
    token=null; localStorage.removeItem("pyref_token");
    localStorage.setItem("pyref_current_user",JSON.stringify(currentUser));
    loadUserData();
  }

  async function register(name,email,password){
    try{
      const d=await api("/api/register",{method:"POST",body:JSON.stringify({name,email,password})});
      token=d.token; currentUser=d.user;
      localStorage.setItem("pyref_token",token);
      localStorage.setItem("pyref_current_user",JSON.stringify(currentUser));
      loadUserData(); await pushFavorites();
      return {local:false};
    }catch(e){
      if(e.code==="offline"){ enterLocal(name,email); return {local:true}; }
      throw e;
    }
  }

  async function login(email,password){
    try{
      const d=await api("/api/login",{method:"POST",body:JSON.stringify({email,password})});
      token=d.token; currentUser=d.user;
      localStorage.setItem("pyref_token",token);
      localStorage.setItem("pyref_current_user",JSON.stringify(currentUser));
      loadUserData(); await pullFavorites();
      return {local:false};
    }catch(e){
      if(e.code==="offline"){ enterLocal(null,email); return {local:true}; }
      throw e;
    }
  }
function loginLocal(name, email) {
  currentUser = { name: name || email.split("@")[0], email, local: true };
  token = null;
  localStorage.removeItem("pyref_token");
  localStorage.setItem("pyref_current_user", JSON.stringify(currentUser));
  loadUserData();
}
async function upgradeLocal(email, password) {
  if (!currentUser || !currentUser.local) {
    throw new Error("Нет локального профиля");
  }

  const base = getApiBase();
  if (!base) {
    throw new Error("Укажите адрес сервера в меню");
  }

  try {
    const data = await api("/api/upgrade", {
      method: "POST",
      body: JSON.stringify({ email, password, name: currentUser.name })
    });

    token = data.token;
    currentUser = data.user;
    localStorage.setItem("pyref_token", token);
    localStorage.setItem("pyref_current_user", JSON.stringify(currentUser));
    await pushFavorites();
  } catch (e) {
    if (e.code === "offline") {
      throw new Error("Сервер недоступен");
    }
    throw e;
  }
}
  function logout(){ token=null; currentUser=null; favorites=new Set(); localStorage.removeItem("pyref_token"); localStorage.removeItem("pyref_current_user"); loadUserData(); }

  async function pullFavorites(){ if(!token)return; try{ const d=await api("/api/favorites"); favorites=new Set(d.favorites||[]); saveFavorites(); }catch(e){ if(e.status===401){token=null;localStorage.removeItem("pyref_token");} } }
  async function pushFavorites(){ if(!token)return; try{ await api("/api/favorites",{method:"PUT",body:JSON.stringify({favorites:[...favorites]})}); }catch(e){} }

  function isFavorite(id){ return favorites.has(id); }
  function toggleFavorite(id){ if(!currentUser)return false; if(favorites.has(id))favorites.delete(id); else favorites.add(id); saveFavorites(); pushFavorites(); return true; }
  function getUser(){ return currentUser; }

  async function loadEntries(){ const urls=["data/entries.json","entries.json"]; let last=null; for(const u of urls){ try{ const r=await fetch(u,{cache:"no-cache"}); if(!r.ok)throw new Error("HTTP "+r.status); const d=await r.json(); if(Array.isArray(d)){state.meta={};state.entries=d;}else{state.meta=d.meta||{};state.entries=Array.isArray(d.entries)?d.entries:[];} return state; }catch(e){last=e;} } throw last||new Error("no entries"); }
  function getEntry(id){ return state.entries.find(e=>e.id===id)||null; }
  function matches(entry,q){ const n=normalize(q); if(!n)return true; const text=normalize(JSON.stringify(entry)); return n.split(" ").filter(Boolean).every(p=>text.includes(p)); }
  function uniqueSorted(v){ return [...new Set(v.filter(Boolean))].sort(); }
  function applyI18n(root=document){ document.documentElement.lang=lang; root.querySelectorAll("[data-i18n]").forEach(el=>{el.textContent=t(el.dataset.i18n);}); root.querySelectorAll("[data-i18n-placeholder]").forEach(el=>{el.placeholder=t(el.dataset.i18nPlaceholder);}); }
  function getLatestPythonVersion(){ const v=Array.isArray(state.meta.pythonVersions)?state.meta.pythonVersions:[]; return v.find(i=>i.status==="latest")||v[0]||null; }

  return { get lang(){return lang;}, state, notificationSettings,
    t,setLang,localize,escapeHtml,normalize,getApiBase,setApiBase,
    loadUserData,saveNotificationSettings,register,login,logout,pullFavorites,pushFavorites,
    isFavorite,toggleFavorite,getUser,loadEntries,getEntry,matches,uniqueSorted,applyI18n,getLatestPythonVersion,
  register, login, loginLocal, upgradeLocal, logout, pullFavorites, pushFavorites };
})();