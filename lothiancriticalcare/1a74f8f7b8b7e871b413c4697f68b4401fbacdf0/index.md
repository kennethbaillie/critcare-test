---
title: guidelines access system
layout: page
redirect_from:
  - /1a74f8f7b8b7e871b413c4697f68b4401fbacdf0/
---

<script src="https://unpkg.com/lunr/lunr.js"></script>
<script src="https://code.jquery.com/jquery-2.1.3.min.js"></script>
<!-- https://lunrjs.com/guides/getting_started.html -->

<div class="col-xs-12 col-md-10 col-lg-8">
  <div class="row">
    <div id="errorbox404">
    </div>
  </div>
  <div class="row">
    <div class="searchbox">
    Search: <input id="search" type="text" placeholder="enter search term">  
    </div>
  </div>

  <div id="results" class="searchresult"></div>

  {% include_relative list.html %}

</div>

<script src="{{ site.baseurl }}/assets/js/search.js"></script>

<script src="sw_load.js"></script>

<script>
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const error404 = urlParams.get('404');
if (error404) {
  console.log("404 detected");
  document.getElementById("errorbox404").innerHTML = `<h3>404 error</h3> The page ${error404} was not found.<br>Try this search instead: `;
}
</script>





