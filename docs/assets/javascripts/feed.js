/**
 * Curated AI Feed — client-side rendering, filtering, and read tracking.
 * Only activates on the feed page (looks for #feed-container).
 */
(function () {
  "use strict";

  var container = document.getElementById("feed-container");
  if (!container) return;

  var filtersEl = document.getElementById("feed-filters");
  var metaEl = document.getElementById("feed-meta");
  var gridEl = document.getElementById("feed-grid");

  var STORAGE_KEY = "feed-read";
  var FEED_URL = "/assets/data/feed.json";

  // --- Read tracking (localStorage) ---

  function getReadUrls() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
    } catch (e) {
      return [];
    }
  }

  function markRead(url) {
    try {
      var read = getReadUrls();
      if (read.indexOf(url) === -1) {
        read.push(url);
        if (read.length > 500) read = read.slice(-500);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(read));
      }
    } catch (e) {
      // localStorage unavailable (private browsing, disabled, or quota exceeded)
    }
  }

  function isRead(url) {
    return getReadUrls().indexOf(url) !== -1;
  }

  // --- Relative time ---

  function timeAgo(isoString) {
    var seconds = Math.floor((Date.now() - new Date(isoString).getTime()) / 1000);
    if (seconds < 60) return "just now";
    var minutes = Math.floor(seconds / 60);
    if (minutes < 60) return minutes + "m ago";
    var hours = Math.floor(minutes / 60);
    if (hours < 24) return hours + "h ago";
    var days = Math.floor(hours / 24);
    if (days === 1) return "1 day ago";
    return days + " days ago";
  }

  // --- Safe DOM helpers ---

  function el(tag, className, textContent) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (textContent) node.textContent = textContent;
    return node;
  }

  // --- Render ---

  function renderFilters(categories, active) {
    filtersEl.textContent = "";
    var bar = el("div", "feed-chip-bar");

    function makeChip(label, category) {
      var btn = el("button", "feed-chip", label);
      if (category === active) btn.classList.add("feed-chip--active");
      btn.setAttribute("data-category", category);
      bar.appendChild(btn);
    }

    makeChip("All", "All");
    categories.forEach(function (cat) {
      makeChip(cat, cat);
    });
    filtersEl.appendChild(bar);
  }

  function renderMeta(updated, itemCount) {
    metaEl.textContent = "";
    var p = el("p", "feed-meta");
    p.textContent =
      "Showing " + itemCount + " items \u00b7 Last updated " + timeAgo(updated);
    metaEl.appendChild(p);
  }

  function renderCards(items) {
    gridEl.textContent = "";

    if (items.length === 0) {
      gridEl.appendChild(el("p", "feed-empty", "No items in this category yet."));
      return;
    }

    var cardsDiv = el("div", "feed-cards");

    items.forEach(function (item) {
      var card = document.createElement("a");
      card.href = item.url;
      card.target = "_blank";
      card.rel = "noopener";
      card.className = "feed-card" + (isRead(item.url) ? " feed-card--read" : "");
      card.setAttribute("data-url", item.url);

      var header = el("div", "feed-card__header");
      header.appendChild(el("span", "feed-card__source", item.source));
      header.appendChild(el("span", "feed-card__time", timeAgo(item.published)));
      card.appendChild(header);

      card.appendChild(el("div", "feed-card__title", item.title));

      if (item.excerpt) {
        card.appendChild(el("div", "feed-card__excerpt", item.excerpt));
      }

      card.appendChild(el("span", "feed-card__category", item.category));
      cardsDiv.appendChild(card);
    });

    gridEl.appendChild(cardsDiv);
  }

  // --- Main ---

  function init() {
    gridEl.textContent = "";
    gridEl.appendChild(el("p", "feed-loading", "Loading feed..."));

    fetch(FEED_URL)
      .then(function (resp) {
        if (!resp.ok) throw new Error("Feed unavailable");
        return resp.json();
      })
      .then(function (data) {
        var allItems = data.items || [];
        var categories = data.categories || [];
        // Read ?category= from URL to pre-select a filter
        var params = new URLSearchParams(window.location.search);
        var paramCategory = params.get("category");
        var activeFilter =
          paramCategory && categories.indexOf(paramCategory) !== -1
            ? paramCategory
            : "All";

        function render() {
          var filtered =
            activeFilter === "All"
              ? allItems
              : allItems.filter(function (i) {
                  return i.category === activeFilter;
                });
          renderFilters(categories, activeFilter);
          renderMeta(data.updated, filtered.length);
          renderCards(filtered);
        }

        render();

        // Filter click handler (event delegation)
        filtersEl.addEventListener("click", function (e) {
          var chip = e.target.closest(".feed-chip");
          if (!chip) return;
          activeFilter = chip.getAttribute("data-category");
          render();
        });

        // Read tracking click handler (event delegation)
        gridEl.addEventListener("click", function (e) {
          var card = e.target.closest(".feed-card");
          if (!card) return;
          var url = card.getAttribute("data-url");
          if (url) {
            markRead(url);
            card.classList.add("feed-card--read");
          }
        });
      })
      .catch(function () {
        gridEl.textContent = "";
        gridEl.appendChild(
          el("p", "feed-empty", "Feed unavailable \u2014 try refreshing the page.")
        );
      });
  }

  // MkDocs Material instant navigation: re-run on page change
  if (typeof document$ !== "undefined") {
    document$.subscribe(function () {
      if (document.getElementById("feed-container")) init();
    });
  } else {
    init();
  }
})();
