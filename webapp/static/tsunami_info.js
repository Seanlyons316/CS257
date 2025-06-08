window.addEventListener("load", initialize);

function initialize() {
    const waveId = getWaveIdFromQuery();
    if (!waveId) {
        alert("Why are you here. There is no tsunami selected!");
        return;
    }
    getTsunamiInfo(waveId);
}

function getWaveIdFromQuery() {
  const params = new URLSearchParams(window.location.search);
  return params.get('wave_id');
}

function getTsunamiInfo(waveId) {
    const url = getAPIBaseURL() + "tsunami/id?id=" + encodeURIComponent(waveId);
    fetch(url)
        .then(function(r) {return r.json()})
        .then(function(tsunami) {
            print(tsunami)
            if (Array.isArray(tsunami)) tsunami = tsunami[0];
            fillTsunamiTable(tsunami);
        })
        .catch(console.error);
}


function fillTsunamiTable(tsunami) {
    console.log("Tsunami data received:", tsunami);
    const table = document.getElementById("tsunami_table_body");
    if (!table) return;

    table.innerHTML = "";
        const fields = [
        ["Source ID", "source id"],
        ["Wave ID", "wave id"],
        ["Region Code", "region code"],
        ["Country", "country"],
        ["State", "state"],
        ["Location", "location"],
        ["Latitude", "latitude"],
        ["Longitude", "longitude"],
        ["Year", "wave year"],
        ["Month", "wave month"],
        ["Day", "wave day"],
        ["Distance from Source", "distance from source"],
        ["Travel Time (Hours)", "travel time_hours"],
        ["Validity", "validity"],
        ["Measurement Type", "measurement type"],
        ["Period", "wave period"],
        ["First Motion", "first motion"],
        ["Maximum Height", "max_height"],
        ["Horizontal Inundation", "horizonrtal innundation"],
        ["Injuries", "injuries"],
        ["Injuries Estimate", "injury estimate"],
        ["Fatalities", "fatalities"],
        ["Fatality Estimate", "fatality estimate"],
        ["Houses Damaged", "houses damaged"],
        ["Houses Damaged Estimate", "houses damaged estimate"],
        ["Houses Destroyed", "houses destroyed"],
        ["Houses Destroyed Estimate", "houses destroyed estimate"]
    ];
    console.log("tsunami object keys:", Object.keys(tsunami));
    console.log("tsunami object:", tsunami);
    fields.forEach(([label, key]) => {
        let value = tsunami[key];
        if (value === undefined || value === null) value = "—";
        const tr = document.createElement("tr");
        tr.innerHTML = `<td>${label}</td><td>${value}</td>`;
        table.appendChild(tr);
    });
}


function getAPIBaseURL() {
  return (
    window.location.protocol +
    "//" +
    window.location.hostname +
    ":" +
    window.location.port +
    "/api/"
  );
}

