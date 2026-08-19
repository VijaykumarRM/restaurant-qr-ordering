const CACHE_NAME = 'hotel-app-v2';
const ASSETS_TO_CACHE = [
    './',
    'index.html',
    'frontend/menu.html',
    'frontend/admin.html',
    'frontend/kitchen.html',
    'manifest.json'
];

// Install Event - Caching fundamental files
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                return cache.addAll(ASSETS_TO_CACHE);
            })
    );
    self.skipWaiting();
});

// Activate Event - Clearing old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cache => {
                    if (cache !== CACHE_NAME) {
                        return caches.delete(cache);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// Fetch Event - Network first, falling back to cache
self.addEventListener('fetch', event => {
    event.respondWith(
        fetch(event.request).catch(() => caches.match(event.request))
    );
});
