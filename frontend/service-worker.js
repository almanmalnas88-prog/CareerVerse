const CACHE_NAME = "careerverse-v1";

const FILES_TO_CACHE = [
    "/",
    "/index.html",
    "/style.css",
    "/script.js",
    "/manifest.json"
];


// =========================================
// INSTALL SERVICE WORKER & CACHE STATIC ASSETS
// =========================================
self.addEventListener("install", function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME).then(function(cache) {
            return cache.addAll(FILES_TO_CACHE);
        })
    );
    self.skipWaiting();
});


// =========================================
// ACTIVATE SERVICE WORKER
// =========================================
self.addEventListener("activate", function(event) {
    event.waitUntil(
        caches.keys().then(function(keyList) {
            return Promise.all(
                keyList.map(function(key) {
                    if (key !== CACHE_NAME) {
                        return caches.delete(key);
                    }
                })
            );
        })
    );
    self.clients.claim();
});


// =========================================
// FETCH EVENT (IGNORE API CALLS)
// =========================================
self.addEventListener("fetch", function(event) {
    // Agar Request POST hai ya /api/ route par hai, toh seedhe Backend/Network par bhejo
    if (event.request.method !== "GET" || event.request.url.includes("/api/")) {
        return; // Normal network request hone do
    }

    // Static Assets (HTML, CSS, JS) ke liye Cache First Strategy
    event.respondWith(
        caches.match(event.request).then(function(response) {
            return response || fetch(event.request);
        })
    );
});