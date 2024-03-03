---
title: guidelines access system
layout: page
---

<script src="https://unpkg.com/lunr/lunr.js"></script>
<script src="https://code.jquery.com/jquery-2.1.3.min.js"></script>
<!-- https://lunrjs.com/guides/getting_started.html -->

<div class="col-xs-12 col-md-6 col-lg-4">
<div class="row" style="margin-bottom: 1em;">
  <div style="float:left">
  Search: <input id="search" type="text" placeholder="enter search term" style="width:150px; margin-bottom: 3px;">  
  </div>
</div>

<div id="results"></div>

{% include_relative list.html %}

</div>

<script src="/assets/js/search.js"></script>

<script src="sw_load.js"></script>








