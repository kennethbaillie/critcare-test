---
Title: guidelines access system
canonical_url: critcare.net/1a74f8f7b8b7e871b413c4697f68b4401fbacdf0
disable_toc: true
---

<script src="https://unpkg.com/lunr/lunr.js"></script>
<script src="https://code.jquery.com/jquery-2.1.3.min.js"></script>
<!-- https://lunrjs.com/guides/getting_started.html -->

<style>
.emergency{
  color: red;
}
.emergency:hover{
  color: red;
}
.emergency:visited{
  color: red;
}
.emergency:focus{
  color: red;
}

.searchresult{
  margin: 0 0 0 5px;
  font-size: smaller;
  color: cornflowerblue;
  display:list-item;
  list-style-type: square;
}

.container {
  /*
    redefine bootstrap container
    to have padding 0
    in order to make
    best use of screen space
  */
  width: 100%;
  padding-right: 0px;
  padding-left: 0px;
  margin-right: auto;
  margin-left: auto;
}

.add-button {
  margin-top: 10px;
  margin-left: 1px;
}
</style>


<p>Search: <input id="search" type="text" placeholder="enter search term"></p>

<div id="results"></div>

<div class="col-xs-12 col-md-6 col-lg-4">
  {!1a74f8f7b8b7e871b413c4697f68b4401fbacdf0/list.html!}
</div>

<div class="col-xs-12 col-md-6 col-lg-8">
  <button class="add-button">Add to home screen</button>
  <p>
    All of these guidelines can be found on the <a href="http://intranet.lothian.scot.nhs.uk/Directory/CriticalCare/Pages"> NHS Lothian intranet.
  </p>
</div>

<script src="search.js"></script>

<script>
  // Code to handle install prompt on desktop

let deferredPrompt;
const addBtn = document.querySelector('.add-button');
addBtn.style.display = 'none';

window.addEventListener('beforeinstallprompt', (e) => {
  console.log("beforeinstallprompt activated")
  // Prevent Chrome 67 and earlier from automatically showing the prompt
  e.preventDefault();
  // Stash the event so it can be triggered later.
  deferredPrompt = e;
  // Update UI to notify the user they can add to home screen
  addBtn.style.display = 'block';

  addBtn.addEventListener('click', () => {
    console.log("addBtn button activated")
    // hide our user interface that shows our A2HS button
    addBtn.style.display = 'none';
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
</script>







