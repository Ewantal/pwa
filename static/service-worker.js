const CACHE_NAME = 'image-upload-pwa-cache-v2'; // Increment version
const urlsToCache = [
    '/',
    '/static/app.js',
    '/static/manifest.json',
    '/static/style.css',
    '/static/icon.png',
    '/static/icon-512.png',
    '/static/icon-maskable.png',
    
    // Add any other assets you want to cache
];

// Install event - cache necessary files
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Opened cache');
                return cache.addAll(urlsToCache);
            })
    );
});

// Fetch event - serve cached content when offline
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Return cached file if available, otherwise fetch from network
                return response || fetch(event.request);
            })
    );
});

// Activate event - cleanup old caches
self.addEventListener('activate', event => {
    console.log('Service Worker activated');
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.filter(cacheName => cacheName !== CACHE_NAME)
                          .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});
