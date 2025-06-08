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

  // Require start and end year, but country is optional
  if (!startYear || !endYear) {
    alert("Please fill in BOTH Start Year and End Year.");
    return;
  }

  let url = "";
  if (country) {
    url = getAPIBaseURL() +
      "/tsunamis/country_years?country=" + encodeURIComponent(country) +
      "&start_year=" + encodeURIComponent(startYear) +
      "&end_year=" + encodeURIComponent(endYear);
  } else {
    url = getAPIBaseURL() +
      "/tsunamis/years?start_year=" + encodeURIComponent(startYear) +
      "&end_year=" + encodeURIComponent(endYear);
  }

  fetch(url)
    .then(response => response.json())
    .then(tsunamis => {
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
          // `<td>${t["source id"]}</td>` +
          // `<td>${t["wave id"]}</td>` +
          `<td>${t["distance from source"]}</td>` +
          `<td>${t["travel time_hours"]}</td>` +
          // `<td>${t["validity"]}</td>` +
          // `<td>${t["measurement type"]}</td>` +
          `<td>${t["wave period"]}</td>` +
          // `<td>${t["first motion"]}</td>` +
          `<td>${t["max_height"]}</td>` +
          // `<td>${t["horizonrtal innundation"]}</td>` + 
          `<td>${t["injuries"]}</td>` +
          // `<td>${t["injury estimate"]}</td>` +
          `<td>${t["fatalities"]}</td>` +
          // `<td>${t["fatality estimate"]}</td>` +
          `<td>${t["houses damaged"]}</td>` +
          // `<td>${t["houses damaged estimate"]}</td>` +
          `<td>${t["houses destroyed"]}</td>` +
          // `<td>${t["houses destroyed estimate"]}</td>` +
          // `<td>${t["region code"]}</td>` +
          // `<td>${t["country"]}</td>` +
          // `<td>${t["wave year"]}</td>` +
          // `<td>${t["wave month"]}</td>` +
          // `<td>${t["wave day"]}</td>` +
          // `<td>${t["state"]}</td>` +
          // `<td>${t["location"]}</td>` +
          // `<td>${t["latitude"]}</td>` +
          // `<td>${t["longitude"]}</td>` +
          "</tr>";
      }

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
