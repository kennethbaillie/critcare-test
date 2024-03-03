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
  <div class="row" style="margin-bottom: 1em;">
    <div style="float:left; margin-left:0.3em;">
    Search: <input id="search" type="text" placeholder="enter search term" style="width:200px; margin-bottom: 3px;">  
    </div>
  </div>

  <div id="results"></div>

  {% include_relative list.html %}

</div>

<script src="/assets/js/search.js"></script>

<script src="sw_load.js"></script>








