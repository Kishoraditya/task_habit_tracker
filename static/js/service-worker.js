const CACHE_NAME = 'task-habit-cache-v1';
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/manifest.json',
  '/login',
  '/register',
  '/dashboard',
  '/static/js/offline-sync.js'
];

// Install event: cache specified resources
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

// Activate event: clear old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.filter(name => name !== CACHE_NAME)
          .map(name => caches.delete(name))
      );
    })
  );
});

// Fetch event: serve cached resources when offline
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        return response || fetch(event.request);
      })
  );
});
