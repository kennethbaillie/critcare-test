// https://lunrjs.com/guides/getting_started.html

var lunrIndex, $results, documents;
var indexReady = false; // Add a flag to indicate if the index is ready


/*
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

function initLunr() {
  return new Promise((resolve, reject) => {
    $.getJSON("index.json")
      .done(function (index) {
        // ... Your existing index processing code

        indexReady = true; // Set the indexReady flag to true
        resolve(); // Resolve the promise when the index is loaded
      })
      .fail(function (jqxhr, textStatus, error) {
        var err = textStatus + ", " + error;
        console.error("Error getting Lunr index file:", err);
        reject(err); // Reject the promise in case of error
      });
  });
}
*/

function initLunr() {
  return new Promise((resolve, reject) => {
    $.getJSON("index.json")
      .done(function (index) {
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
        indexReady = true; // Set the indexReady flag to true
        resolve(); // Resolve the promise when the index is loaded
      })
      .fail(function (jqxhr, textStatus, error) {
        var err = textStatus + ", " + error;
        console.error("Error getting Lunr index file:", err);
        reject(err); // Reject the promise in case of error
      });
  });
}

function search(query) {
  if (!indexReady) { // Check if the index is ready before running the search
    return [];
  }
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
      text: result.title,
      target: result.target,
      onclick: result.onclick
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

// parse the URL query string and return the search term
function getSearchTermFromQueryString() {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const searchTerm = urlParams.get('searchterm');

  if (searchTerm) {
    return decodeURIComponent(searchTerm);
  }
  return '';
}

// Call this function on page load to read the URL query string and run the search
function initSearchFromQueryString(lunrIndexPromise) {
  lunrIndexPromise
    .then(() => {
      const searchTerm = getSearchTermFromQueryString();

      if (searchTerm) {
        const searchInput = $("#search");
        searchInput.val(searchTerm);
        const results = search(searchTerm);
        renderResults(results);
      }
    })
    .catch((error) => {
      console.error("Error initializing search from query string:", error);
    });
}

initUI();
const lunrIndexPromise = initLunr();
$(document).ready(() => initSearchFromQueryString(lunrIndexPromise));

