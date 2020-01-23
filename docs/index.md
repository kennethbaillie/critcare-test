---
Title: critical care guidelines
canonical_url: baillielab.net
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
</style>


<p class='small' style="color:red;">*DEMO ONLY. Protocols out of date*</p>

<p>Search: <input id="search" type="text" placeholder="enter search term"></p>

<div id="results"></div>

<script>
	var lunrIndex, $results, documents;

    function initLunr() {
      // retrieve the index file
      $.getJSON("index.json")
        .done(function(index) {
            documents = index;

            lunrIndex = lunr(function(){
              this.ref('href')
              this.field('content')
              this.field("title", {
                  boost: 10
              });

              documents.forEach(function(doc) {
                try {
                  this.add(doc)
                } catch (e) {}
              }, this)
            })
        })
        .fail(function(jqxhr, textStatus, error) {
            var err = textStatus + ", " + error;
            console.error("Error getting Lunr index file:", err);
        });
    }

    function search(query) {
      return lunrIndex.search(query).map(function(result) {
        return documents.filter(function(page) {
          try {
            return page.href === result.ref;
          } catch (e) {
            console.log('whoops')
          }
        })[0];
      });
    }

    function renderResults(results) {
      if (!results.length) {
        return;
      }
      // show first twenty results
      results.slice(0, 20).forEach(function(result) {
        var $result = $("<li class='searchresult'>");
        $result.append($("<a>", {
          href: result.href,
          text: result.title
        }));
        $results.append($result);
      });
    }

    function initUI() {
      $results = $("#results");

      $("#search").keyup(function(){
        // empty previous results
        $results.empty();
        // trigger search when at least two chars provided.
        var query = $(this).val();
        if (query.length < 2) {
          return;
        }
        var results = search(query);
        renderResults(results);
      });
    }

    initLunr();
    initUI();

</script>

<div class="col-xs-12 col-md-6">
{!list.html!}
</div>

<div class="col-xs-12 col-md-6">
<p>
  All of these guidelines can be found on the NHS Lothian intranet.
</p>
</div>
