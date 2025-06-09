window.addEventListener("load", initialize);

// This script handles the search and display of tsunami data.
let currentPage = 1;
let totalPages = 1;
const pageSize = 25;

function initialize() {
  document.getElementById("tsunami_search_button").onclick = onTsunamisSearchFlexible;
  document.getElementById("tsunami_reset_button").onclick = onResetSearch;

  document.querySelectorAll("#tsunami_search_criteria_dropdown a").forEach(function(el) {
    el.onclick = function(e) {
      e.preventDefault();
      document.getElementById("tsunami_search_criteria").value = el.dataset.value;
      document.getElementById("tsunami_search_criteria_button").textContent = el.textContent;
    };
  });

  document.querySelectorAll("#tsunami_sort_criteria_dropdown a").forEach(function(el) {
    el.onclick = function(e) {
      e.preventDefault();
      document.getElementById("tsunami_sort_criteria").value = el.dataset.value;
      document.getElementById("tsunami_sort_criteria_button").textContent = el.textContent;
    };
  });

  document.querySelectorAll("#tsunami_order_criteria_dropdown a").forEach(function(el) {
    el.onclick = function(e) {
      e.preventDefault();
      document.getElementById("tsunami_order_criteria").value = el.dataset.value;
      document.getElementById("tsunami_order_criteria_button").textContent = el.textContent;
    };
  });
}

function getAPIBaseURL() {
  return (
    window.location.protocol +
    "//" +
    window.location.hostname +
    ":" +
    window.location.port +
    "/api"
  );
}

function onTsunamisSearchFlexible(resetPage = true) {
  // Reset current page when a new search is initiated
  if (resetPage) {
    currentPage = 1;
  }
  const startYear = document.getElementById("tsunami_start_year").value.trim();
  const endYear = document.getElementById("tsunami_end_year").value.trim();
  const country = document.getElementById("tsunami_country").value.trim();
  let sortField = document.getElementById("tsunami_sort_criteria").value;
  let sortOrder = document.getElementById("tsunami_order_criteria").value;
  // Set default values for sorting if not provided
  if (!sortField) {
    sortField = "wave year";
    document.getElementById("tsunami_sort_criteria").value = sortField;
    document.getElementById("tsunami_sort_criteria_button").textContent = "Year";
  }
  if (!sortOrder) {
    sortOrder = "desc";
    document.getElementById("tsunami_order_criteria").value = sortOrder;
    document.getElementById("tsunami_order_criteria_button").textContent = "Descending";
  }

  // Set base URL for the API request
  let url = getAPIBaseURL() + "/tsunamis/?";
  // Append search parameters to the URL
  if (startYear) url += 'start_year=' + encodeURIComponent(startYear) + '&';
  if (endYear) url += 'end_year=' + encodeURIComponent(endYear) + '&';
  if (country) url += 'country=' + encodeURIComponent(country) + '&';
  //Sort parameters
  url += 'sort_field=' + encodeURIComponent(sortField) + '&';
  url += 'sort_order=' + encodeURIComponent(sortOrder) + '&';
  url += 'page_size=' + pageSize + '&page=' + currentPage;
  // Fetch data from API
  fetch(url)
    .then(response => response.json())
    .then(data => {
      const tsunamis = data.tsunamis;
      currentPage = data.page;
      totalPages = Math.ceil(data.total_count / data.page_size);

      let rows = "";
      for (const t of tsunamis) {
        rows +=
          `<tr class="tsunami-row" data-waveid="${t["wave id"]}">` +
          `<td>${t["country"]}</td>` +
          `<td>${t["wave year"]}</td>` +
          `<td>${t["latitude"]}</td>` +
          `<td>${t["longitude"]}</td>` +
          `<td>${t["distance from source"]}</td>` +
          `<td>${t["travel time_hours"]}</td>` +
          `<td>${t["wave period"]}</td>` +
          `<td>${t["max_height"]}</td>` +
          `<td>${t["injuries"]}</td>` +
          `<td>${t["fatalities"]}</td>` +
          `<td>${t["houses damaged"]}</td>` +
          `<td>${t["houses destroyed"]}</td>` +
          "</tr>";
      }
      // Update the table with new rows
      //Pages and navigation update
      updatePages();
      const tbody = document.querySelector("#tsunamis_table tbody");
      if (tbody) {
        tbody.innerHTML = rows;
        Array.from(tbody.getElementsByClassName('tsunami-row')).forEach(row => {
          row.addEventListener('click', function() {
            const waveId = this.dataset.waveid;
            window.location.href = "/tsunami?wave_id=" + encodeURIComponent(waveId);
          });
        });
      }
    })
    .catch(console.error);
}

function onResetSearch() {
  currentPage = 1;
  document.getElementById("tsunami_start_year").value = "";
  document.getElementById("tsunami_end_year").value = "";
  document.getElementById("tsunami_country").value = "";
  document.getElementById("tsunami_sort_criteria").value = "distance from source";
  document.getElementById("tsunami_order_criteria").value = "asc";

  const tbody = document.querySelector("#tsunamis_table tbody");
  if (tbody) tbody.innerHTML = "";
}

function updatePages() {
  document.getElementById("tsunami_current_page").textContent = currentPage;
  document.getElementById("tsunami_total_pages").textContent = totalPages;

  document.getElementById("previous_page").disabled = (currentPage <= 1);
  document.getElementById("next_page").disabled = (currentPage >= totalPages);

  document.getElementById("previous_page").onclick = function () {
    if (currentPage > 1) {
      currentPage--;
      onTsunamisSearchFlexible(false);
    }
  };

  document.getElementById("next_page").onclick = function () {
    if (currentPage < totalPages) {
      currentPage++;
      onTsunamisSearchFlexible(false);
    }
  };
}

// Dropdown toggle handlers
document.getElementById('tsunami_order_criteria_button').addEventListener('click', function(event) {
  event.stopPropagation();
  document.getElementById('tsunami_sort_criteria_dropdown').classList.remove('show');
  document.getElementById('tsunami_order_criteria_dropdown').classList.toggle('show');
});

document.getElementById('tsunami_sort_criteria_button').addEventListener('click', function(event) {
  event.stopPropagation();
  document.getElementById('tsunami_order_criteria_dropdown').classList.remove('show');
  document.getElementById('tsunami_sort_criteria_dropdown').classList.toggle('show');
});

window.addEventListener('click', function () {
  document.getElementById('tsunami_order_criteria_dropdown').classList.remove('show');
  document.getElementById('tsunami_sort_criteria_dropdown').classList.remove('show');
});

