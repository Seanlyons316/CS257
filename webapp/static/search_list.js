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

function getTsunamiInfo(waveId) {
  
}
function onTsunamisSearchFlexible() {
  // Get the search criteria, input value, and sets the base URL for the API call
  var crit = document.getElementById("tsunami_search_criteria").value;
  var value = document.getElementById("tsunami_search_input").value.trim();
  let url = getAPIBaseURL() + "/tsunamis/";
  // Differentiate the search criteria and build the URL accordingly
  switch (crit) {
    case "year":
      if (isNaN(value)) return;
      var year = parseInt(value, 10);
      if (isNaN(year)) return;
      url += "years?start_year=" + year + "&end_year=" + (year + 1);
      break;
    case "country":
      if (!value) return;
      url += "countries?country=" + encodeURIComponent(value);
      break;
    case "wave id":
      if (!value) return;
      var id = parseInt(value, 10);
      if (isNaN(id)) return;
      url += "id?id=" + id;
      break;
    default:
      return;
  }
  // Fetch the data from the API
  fetch(url)
    .then(function(r) { return r.json(); })
    .then(function(tsunamis) {
      // Sets the conditions of the sorting
      var field = document.getElementById("tsunami_sort_criteria").value;
      var dir = document.getElementById("tsunami_order_criteria").value === "desc" ? -1 : 1;
      // Sort the tsunamis based on the selected field and direction
      tsunamis.sort(function(a, b) {
        var va = parseFloat(a[field]);
        var vb = parseFloat(b[field]);
        if (va < vb) return -1 * dir;
        if (va > vb) return 1 * dir;
        return 0;
      });

      // Clear the existing table rows
      let rows = "";
      // Create the table header
      for (const t of tsunamis) {
        rows +=
          `<tr class="tsunami-row" data-waveid="{t["wave id"]}">` +
          `<td>${t["source id"]}</td>` +
          `<td>${t["wave id"]}</td>` +
          `<td>${t["distance from source"]}</td>` +
          `<td>${t["travel time_hours"]}</td>` +
          `<td>${t["validity"]}</td>` +
          `<td>${t["measurement type"]}</td>` +
          `<td>${t["wave period"]}</td>` +
          `<td>${t["first motion"]}</td>` +
          `<td>${t["max_height"]}</td>` +
          `<td>${t["horizonrtal innundation"]}</td>` + 
          `<td>${t["injuries"]}</td>` +
          `<td>${t["injury estimate"]}</td>` +
          `<td>${t["fatalities"]}</td>` +
          `<td>${t["fatality estimate"]}</td>` +
          `<td>${t["houses damaged"]}</td>` +
          `<td>${t["houses damaged estimate"]}</td>` +
          `<td>${t["houses destroyed"]}</td>` +
          `<td>${t["houses destroyed estimate"]}</td>` +
          `<td>${t["region code"]}</td>` +
          `<td>${t["country"]}</td>` +
          `<td>${t["wave year"]}</td>` +
          `<td>${t["wave month"]}</td>` +
          `<td>${t["wave day"]}</td>` +
          `<td>${t["state"]}</td>` +
          `<td>${t["location"]}</td>` +
          `<td>${t["latitude"]}</td>` +
          `<td>${t["longitude"]}</td>` +
          "</tr>";
      }
      // Insert the new rows into the table body
      const tbody = document.querySelector("#tsunamis_table tbody");
      if (tbody) tbody.innerHTML = rows;
    })

    // Had to look up how to store the wave id stuff here before doing window.location.href = 'tsunami_info.html'
    Array.from(tbody.getElementByClassName('tsunami-row')).forEach(row => {
      row.addEventListener('click', function(){
        const waveId = this.dataset.waveid;
        sessionStorage.setItem('selectedWaveId', waveId)
        window.location.href = 'tsunami_info.html'
      })
    })

    // Clickable rows to load tsunami_info for that specific tsunami
    
    .catch(console.error);
}
// Function to reset the search input and clear the table
function onResetSearch() {
  var value = document.getElementById("tsunami_search_input");
  if (input) value.value = "";
  const tbody = document.querySelector("#tsunamis_table tbody");
  if (tbody) tbody.innerHTML = "";
}
// Event listeners for the dropdown buttons to toggle visibility
document.getElementById('tsunami_search_criteria_button').addEventListener('click', function(event) {
    event.stopPropagation();
    // document.getElementById('years-menu').classList.remove('show');
    document.getElementById('tsunami_sort_criteria_dropdown').classList.remove('show');
    document.getElementById('tsunami_order_criteria_dropdown').classList.remove('show');
    document.getElementById('tsunami_search_criteria_dropdown').classList.toggle('show');
});

document.getElementById('tsunami_order_criteria_button').addEventListener('click', function(event) {
    event.stopPropagation();
    // document.getElementById('years-menu').classList.remove('show');
    document.getElementById('tsunami_sort_criteria_dropdown').classList.remove('show');
    document.getElementById('tsunami_order_criteria_dropdown').classList.toggle('show');
    document.getElementById('tsunami_search_criteria_dropdown').classList.remove('show');
});

document.getElementById('tsunami_sort_criteria_button').addEventListener('click', function(event) {
    event.stopPropagation();
    // document.getElementById('years-menu').classList.remove('show');
    document.getElementById('tsunami_order_criteria_dropdown').classList.remove('show');
    document.getElementById('tsunami_search_criteria_dropdown').classList.remove('show');
    document.getElementById('tsunami_sort_criteria_dropdown').classList.toggle('show');
});

// click anywhere else to close the dropdowns
window.addEventListener('click', function() {
    document.getElementById('tsunami_order_criteria_dropdown').classList.remove('show');
    document.getElementById('tsunami_search_criteria_dropdown').classList.remove('show');
    document.getElementById('tsunami_sort_criteria_dropdown').classList.remove('show');
});