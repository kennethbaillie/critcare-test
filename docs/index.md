---
Title: protocols access system
canonical_url: critcare.net
disable_toc: true
---

<script src="https://unpkg.com/lunr/lunr.js"></script>
<script src="https://code.jquery.com/jquery-2.1.3.min.js"></script>
<!-- https://lunrjs.com/guides/getting_started.html -->

<style>
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
</style>


<p>Search: <input id="search" type="text" placeholder="enter search term"></p>

<div id="results"></div>

<div class="col-xs-12 col-md-6 col-lg-4">
  {!list.html!}
</div>

<div class="col-xs-12 col-md-6 col-lg-8">
  <p>
    All of these guidelines can be found on the <a href="http://intranet.lothian.scot.nhs.uk/Directory/CriticalCare/Pages"> NHS Lothian intranet.
  </p>
</div>

<script src="search.js"></script>









