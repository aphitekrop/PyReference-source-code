const CACHE_NAME = "pyreference-v9";

const ASSETS = [
  "./",
  "./index.html",
  "./entry.html",
  "./articles.html",
  "./article.html",
  "./manifest.webmanifest",
  "./assets/css/style.css?v=9",
  "./assets/js/core.js?v=9",
  "./assets/js/index.js?v=9",
  "./assets/js/entry.js?v=9",
  "./assets/js/articles.js?v=9",
  "./assets/js/article.js?v=9"
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => Promise.allSettled(ASSETS.map(asset => cache.add(asset))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", event => {
  if (event.request.method !== "GET") return;

  const url = new URL(event.request.url);
  const isData = url.pathname.endsWith(".json");

  if (isData) {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          const copy = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy));
          return response;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(cached => {
        if (cached) return cached;
        return fetch(event.request)
          .then(response => {
            if (!response || response.status !== 200 || response.type !== "basic") return response;
            const copy = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy));
            return response;
          })
          .catch(() => caches.match("./index.html"));
      })
  );
});