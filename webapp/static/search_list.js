// search_list.js
window.addEventListener("load", initialize);

function initialize() {
  const element = document.getElementById("tsunami_search_button");
  const resetElement = document.getElementById("tsunami_reset_button");
  if (element) element.onclick = onTsunamisSearchFlexible;
  if (resetElement) resetElement.onclick = onResetSearch;
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

function onTsunamisSearchFlexible() {
  const searchEl = document.getElementById("tsunami_search_criteria");
  const orderField = document.getElementById("tsunami_order_criteria");
  const orderDir = document.getElementById("tsunami_order_direction");
  const input = document.getElementById("tsunami_search_input");
  if (!searchEl || !input) return;

  const crit = searchEl.value;
  const value = input.value.trim();
  let url = getAPIBaseURL() + "/tsunamis/";

  switch (crit) {
    case "year":
      if (!value) return;
      const year = parseInt(value, 10);
      if (isNaN(year)) return;
      url += `years?start_year=${year}&end_year=${year + 1}`;
      break;
    case "country":
      if (!value) return;
      url += `countries?country=${encodeURIComponent(value)}`;
      break;
    case "wave id":
      if (!value) return;
      const id = parseInt(value, 10);
      if (isNaN(id)) return;
      url += `id?id=${id}`;
      break;
    default:
      return;
  }

  fetch(url)
    .then((r) => r.json())
    .then((tsunamis) => {
      // sort
      const field = orderField ? orderField.value : "";
      const dir = orderDir && orderDir.value === "desc" ? -1 : 1;
      tsunamis.sort((a, b) => {
        const va = a[field],
          vb = b[field];
        const na = parseFloat(va),
          nb = parseFloat(vb);
        if (!isNaN(na) && !isNaN(nb)) {
          return (na - nb) * dir;
        }
        return va.toString().localeCompare(vb.toString()) * dir;
      });

      // build rows
      let rows = "";
      for (const t of tsunamis) {
        rows +=
          "<tr>" +
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

      const tbody = document.querySelector("#tsunamis_table tbody");
      if (tbody) tbody.innerHTML = rows;
    })
    .catch(console.error);
}

function onResetSearch() {
  const input = document.getElementById("tsunami_search_input");
  if (input) input.value = "";
  const tbody = document.querySelector("#tsunamis_table tbody");
  if (tbody) tbody.innerHTML = "";
}

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