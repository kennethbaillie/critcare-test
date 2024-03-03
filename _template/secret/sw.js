// use a cacheName for cache versioning
var cacheName = 'v2:nocache';

// during the install phase you usually want to cache static assets
self.addEventListener('install', function(e) {
    // once the SW is installed, go ahead and fetch the resources to make this work offline
    console.log("install activated")
    /*
    e.waitUntil(
        caches.open(cacheName).then(function(cache) {
            return cache.addAll([
                './',
            ]).then(function() {
                self.skipWaiting();
            });
        })
    );
    */
});

// when the browser fetches a url
self.addEventListener('fetch', function(event) {
    // either respond with the cached object or go ahead and fetch the actual url
    event.respondWith(
        caches.match(event.request).then(function(response) {
            if (response) {
                console.log("looking in cache")
                // retrieve from cache
                // return response; // commented out to force update
            }
            // fetch as normal
            return fetch(event.request);
        })
    );
});