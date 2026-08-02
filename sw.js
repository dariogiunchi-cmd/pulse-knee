var C='pulse-v1';
self.addEventListener('install',function(e){e.waitUntil(caches.open(C).then(function(c){return c.addAll(['./','./index.html','./icon-192.png','./apple-touch-icon.png','./manifest.json'])}).then(function(){return self.skipWaiting()}).catch(function(){}))});
self.addEventListener('activate',function(e){e.waitUntil(caches.keys().then(function(ks){return Promise.all(ks.filter(function(k){return k!==C}).map(function(k){return caches.delete(k)}))}).then(function(){return self.clients.claim()}))});
self.addEventListener('fetch',function(e){
  if(e.request.method!=='GET')return;
  /* le istantanee datate non si tengono in cache: sono decine di copie da 130 KB
     e servono solo quando si va a cercarle */
  if(e.request.url.indexOf('/versioni/')>=0)return;
  e.respondWith(fetch(e.request).then(function(r){var cp=r.clone();caches.open(C).then(function(c){c.put(e.request,cp)});return r;})
   .catch(function(){return caches.match(e.request).then(function(r){return r||caches.match('./index.html')})}));
});
