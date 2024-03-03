if ('serviceWorker' in navigator) {
navigator.serviceWorker.register('sw.js').then(function(reg) {
    console.log('Successfully registered service worker', reg);
}).catch(function(err) {
    console.warn('Error whilst registering service worker', err);
});
}

// Code to handle install prompt on desktop
let deferredPrompt;
const addBtn = document.querySelector('.add-button');
addBtn.style.display = 'none';
const homeBtn = document.querySelector('.home-button'); 
homeBtn.style.display = 'inline';

// JKB addition to hide home button if loaded from bookmark
if (window.matchMedia('(display-mode: standalone)').matches) {
  console.log("App loaded from bookmark (android)");
  homeBtn.style.display = 'none';
}

window.addEventListener('beforeinstallprompt', (e) => {
  console.log("beforeinstallprompt activated")
  // Prevent Chrome 67 and earlier from automatically showing the prompt
  e.preventDefault();
  // Stash the event so it can be triggered later.
  deferredPrompt = e;
  // Update UI to notify the user they can add to home screen
  addBtn.style.display = 'inline';
  homeBtn.style.display = 'none';

  addBtn.addEventListener('click', () => {
    console.log("addBtn button activated")
    // hide our user interface that shows our A2HS button
    addBtn.style.display = 'none';
    homeBtn.style.display = 'none';
    // Show the prompt
    deferredPrompt.prompt();
    // Wait for the user to respond to the prompt
    deferredPrompt.userChoice.then((choiceResult) => {
      if (choiceResult.outcome === 'accepted') {
        console.log('User accepted the A2HS prompt');
      } else {
        console.log('User dismissed the A2HS prompt');
      }
      deferredPrompt = null;
    });
  });
});

window.addEventListener("beforeinstallprompt", function(e) {
  // log the platforms provided as options in an install prompt
  console.log(e.platforms); // e.g., ["web", "android", "windows"]
  e.userChoice.then(function(choiceResult) {
    console.log(choiceResult.outcome); // either "accepted" or "dismissed"
  });
});



