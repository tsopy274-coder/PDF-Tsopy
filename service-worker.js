// PDF-Tsopy Service Worker v1.2
// Offline support & caching strategy

const CACHE_NAME = 'pdf-tsopy-v1.2';
const STATIC_CACHE = 'pdf-tsopy-static-v1.2';

// Αρχεία που αποθηκεύονται για offline χρήση
const STATIC_FILES = [
  './',
  './index.html',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
  // PDF.js από CDN — αποθηκεύεται κι αυτό
  'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js',
];

// ─── Install ───────────────────────────────────────────────────────────────
self.addEventListener('install', (event) => {
  console.log('[SW] Installing PDF-Tsopy v1.2...');
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => {
      // Αποθηκεύουμε τα τοπικά αρχεία — αγνοούμε αποτυχίες CDN
      return cache.addAll(['./', './index.html', './manifest.json'])
        .then(() => {
          console.log('[SW] Core files cached.');
        });
    })
  );
  self.skipWaiting();
});

// ─── Activate ──────────────────────────────────────────────────────────────
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating PDF-Tsopy...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== STATIC_CACHE && name !== CACHE_NAME)
          .map((name) => {
            console.log('[SW] Deleting old cache:', name);
            return caches.delete(name);
          })
      );
    })
  );
  self.clients.claim();
});

// ─── Fetch Strategy: Cache-First για static, Network-First για άλλα ────────
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Αγνοούμε non-GET requests
  if (event.request.method !== 'GET') return;

  // Αγνοούμε chrome-extension και άλλα σχήματα
  if (!['http:', 'https:'].includes(url.protocol)) return;

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        // Cache hit — επιστρέφουμε cached και ανανεώνουμε στο background
        fetch(event.request)
          .then((networkResponse) => {
            if (networkResponse && networkResponse.status === 200) {
              caches.open(STATIC_CACHE).then((cache) => {
                cache.put(event.request, networkResponse.clone());
              });
            }
          })
          .catch(() => {}); // offline — δεν πειράζει
        return cachedResponse;
      }

      // Δεν υπάρχει στο cache — network request
      return fetch(event.request)
        .then((networkResponse) => {
          if (!networkResponse || networkResponse.status !== 200) {
            return networkResponse;
          }

          // Αποθηκεύουμε στο cache για μελλοντική χρήση
          const responseToCache = networkResponse.clone();
          caches.open(STATIC_CACHE).then((cache) => {
            cache.put(event.request, responseToCache);
          });

          return networkResponse;
        })
        .catch(() => {
          // Offline fallback — επιστρέφουμε την κύρια σελίδα
          if (event.request.destination === 'document') {
            return caches.match('./index.html');
          }
        });
    })
  );
});

// ─── Background Sync (για μελλοντική χρήση) ───────────────────────────────
self.addEventListener('sync', (event) => {
  console.log('[SW] Background sync:', event.tag);
});

// ─── Push Notifications (για μελλοντική χρήση) ────────────────────────────
self.addEventListener('push', (event) => {
  if (event.data) {
    const data = event.data.json();
    self.registration.showNotification(data.title || 'PDF-Tsopy', {
      body: data.body || '',
      icon: './icons/icon-192.png',
      badge: './icons/icon-96.png',
    });
  }
});
