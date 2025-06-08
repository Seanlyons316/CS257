// search_list.js
window.addEventListener("load", initialize);

function initialize() {
  document.getElementById("tsunami_search_button").onclick = onTsunamisSearchFlexible;
  document.getElementById("tsunami_reset_button").onclick = onResetSearch;
  // Set the default values for the dropdowns
  document.querySelectorAll("#tsunami_search_criteria_dropdown a").forEach(function(el) {
    el.onclick = function(e) {
      e.preventDefault();
      // Set the search criteria based on the clicked element
      document.getElementById("tsunami_search_criteria").value = el.dataset.value;
      document.getElementById("tsunami_search_criteria_button").textContent = el.textContent;
    };
});
  // Set the default values for the sort criteria dropdown
  document.querySelectorAll("#tsunami_sort_criteria_dropdown a").forEach(function(el) {
    el.onclick = function(e) {
      e.preventDefault();
      // Set the sort criteria based on the clicked element
      document.getElementById("tsunami_sort_criteria").value = el.dataset.value;
      document.getElementById("tsunami_sort_criteria_button").textContent = el.textContent;
    };
});
  // Set the default values for the order criteria dropdown
  document.querySelectorAll("#tsunami_order_criteria_dropdown a").forEach(function(el) {
    el.onclick = function(e) {
      e.preventDefault();
      
      document.getElementById("tsunami_order_criteria").value = el.dataset.value;
      document.getElementById("tsunami_order_criteria_button").textContent = el.textContent;
    };
  });
}
// Function to get the base URL for the API
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
function onTsunamisSearchFlexible() {
  const startYear = document.getElementById("tsunami_start_year").value.trim();
  const endYear = document.getElementById("tsunami_end_year").value.trim();
  const country = document.getElementById("tsunami_country").value.trim();
  let currentPage = 1;
  let totalPages = 1;
  const pageSize = 25;

  let url = getAPIBaseURL() + "/tsunamis/?";

  if (startYear && endYear && country) {
    url += 'start_year=' + encodeURIComponent(startYear) +
           '&end_year=' + encodeURIComponent(endYear) +
           '&country=' + encodeURIComponent(country);
  } else if (startYear && endYear) {
    url += 'start_year=' + encodeURIComponent(startYear) +
           '&end_year=' + encodeURIComponent(endYear);
  } else if (startYear && country) {
    url += 'start_year=' + encodeURIComponent(startYear) +
           '&country=' + encodeURIComponent(country);
  } else if (endYear && country) {
    url += 'end_year=' + encodeURIComponent(endYear) +
           '&country=' + encodeURIComponent(country);
  } else if (country) {
    url += 'country=' + encodeURIComponent(country);
  } else if (startYear) {
    url += 'start_year=' + encodeURIComponent(startYear);
  } else if (endYear) {
    url += 'end_year=' + encodeURIComponent(endYear);
  }

  fetch(url)
    .then(response => response.json())
    .then(data => {
      const tsunamis = data.tsunamis;
      currentPage = data.page;
      totalPages = Math.ceil(data.total_count / data.page_size);
      // Sorting (same as before)
      var field = document.getElementById("tsunami_sort_criteria").value;
      var dir = document.getElementById("tsunami_order_criteria").value === "desc" ? -1 : 1;

      tsunamis.sort(function(a, b) {
      let va = a[field];
      let vb = b[field];
      if (va === null && vb === null) {
        return 0;
      }
      if (va === null) {
        return 1;
      }
      if (vb === null) {
        return -1;
      }

      if (!isNaN(parseFloat(va)) && !isNaN(parseFloat(vb))){
        va = parseFloat(va);
        vb = parseFloat(vb);
        if (va < vb){
          return -1 * dir;
        }
        if (va > vb){
          return 1 * dir;
        }
        return 0;
      }

      else {
        va = String(va).toUpperCase();
        vb = String(vb).toUpperCase();
        if (va < vb){
          return -1 * dir;
        }
        if (va > vb) {
          return 1 * dir;
        }
        return 0;
      }
      });
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


// Function to reset the search input and clear the table
function onResetSearch() {
  document.getElementById("tsunami_start_year").value = "";
  document.getElementById("tsunami_end_year").value = "";
  document.getElementById("tsunami_country").value = "";
  const tbody = document.querySelector("#tsunamis_table tbody");
  if (tbody) tbody.innerHTML = "";
  document.getElementById("tsunami_sort_criteria").value = "distance from source";
  document.getElementById("tsunami_order_criteria").value = "asc";
}

function updatePages() {
  document.getElementById("tsunami_current_page").textContent = currentPage;
  document.getElementById("tsunami_total_pages").textContent = totalPages;
  document.getElementById("previous_page").disabled = (currentPage <= 1);
  document.getElementById("next_page").disabled = (currentPage >= totalPages);
  document.getElementById("previous_page").onclick = function() {
    if (currentPage > 1) {
      currentPage--;
      onTsunamisSearchFlexible();
    }
  };
  document.getElementById("next_page").onclick = function() {
    if (currentPage < totalPages) {
      currentPage++;
      onTsunamisSearchFlexible();
    }
  };
}



document.getElementById('tsunami_order_criteria_button').addEventListener('click', function(event) {
    event.stopPropagation();
    // document.getElementById('years-menu').classList.remove('show');
    document.getElementById('tsunami_sort_criteria_dropdown').classList.remove('show');
    document.getElementById('tsunami_order_criteria_dropdown').classList.toggle('show');
});

document.getElementById('tsunami_sort_criteria_button').addEventListener('click', function(event) {
    event.stopPropagation();
    // document.getElementById('years-menu').classList.remove('show');
    document.getElementById('tsunami_order_criteria_dropdown').classList.remove('show');
    document.getElementById('tsunami_sort_criteria_dropdown').classList.toggle('show');
});

// click anywhere else to close the dropdowns
window.addEventListener('click', function() {
    document.getElementById('tsunami_order_criteria_dropdown').classList.remove('show');
    document.getElementById('tsunami_sort_criteria_dropdown').classList.remove('show');
});
