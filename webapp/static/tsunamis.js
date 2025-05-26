window.addEventListener("load", initialize);

function initialize() {
    let element = document.getElementById('tsunami_search_button');
    let resetElement = document.getElementById('tsunami_reset_button');
    if (element) {
        element.onclick = onTsunamisSearchChanged;
    }
    if (resetElement) {
        resetElement.onclick = onResetSearch;
    }
}

function getAPIBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/api';
    return baseURL;
}

function onTsunamisSearchChanged() {
    let input = document.getElementById('tsunami_search_input');
    if (!input) {
        return;
    }

    let yearString = input.value.trim();
    if (yearString === '') {
        return;
    }

    let year = parseInt(yearString);
    if (isNaN(year)) {
        return;
    }

    let nextYearString = (year + 1).toString();

    let url = getAPIBaseURL() + '/tsunamis/years?start_year=' + yearString + '&end_year=' + nextYearString;
    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(tsunamis) {
        let tableBody = '';
        for (let k = 0; k < tsunamis.length; k++) {
            let tsunami = tsunamis[k];
            tableBody += '<tr>'
                            + '<td>' + tsunami['source id'] + '</td>'
                            + '<td>' + tsunami['wave id'] + '</td>'
                            + '<td>' + tsunami['distance from source'] + '</td>'
                            + '<td>' + tsunami['travel time hours'] + '</td>'
                            + '<td>' + tsunami['validity'] + '</td>'
                            + '<td>' + tsunami['measurement type'] + '</td>'
                            + '<td>' + tsunami['wave period'] + '</td>'
                            + '<td>' + tsunami['first motion'] + '</td>'
                            + '<td>' + tsunami['max_height'] + '</td>'
                            + '<td>' + tsunami['horizonrtal innundation'] + '</td>'
                            + '<td>' + tsunami['injuries'] + '</td>'
                            + '<td>' + tsunami['injuries estimate'] + '</td>'
                            + '<td>' + tsunami['fatalities'] + '</td>'
                            + '<td>' + tsunami['fatalities estimate'] + '</td>'
                            + '<td>' + tsunami['houses damaged'] + '</td>'
                            + '<td>' + tsunami['houses damaged estimate'] + '</td>'
                            + '<td>' + tsunami['houses destroyed'] + '</td>'
                            + '<td>' + tsunami['houses destroyed estimate'] + '</td>'
                            + '<td>' + tsunami['region code'] + '</td>'
                            + '<td>' + tsunami['country'] + '</td>'
                            + '<td>' + tsunami['wave year'] + '</td>'
                            + '<td>' + tsunami['wave month'] + '</td>'
                            + '<td>' + tsunami['wave day'] + '</td>'
                            + '<td>' + tsunami['state'] + '</td>'
                            + '<td>' + tsunami['location'] + '</td>'
                            + '<td>' + tsunami['latitude'] + '</td>'
                            + '<td>' + tsunami['longitude'] + '</td>'
                            + '</tr>';
        }

        let tsunamisTable = document.querySelector('#tsunamis_table tbody');
        if (tsunamisTable) {
            tsunamisTable.innerHTML = tableBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function onResetSearch() {
    let input = document.getElementById('tsunami_search_input');
    if (input) {
        input.value = '';
    }
    let tsunamisTable = document.querySelector('#tsunamis_table tbody');
    if (tsunamisTable) {
        tsunamisTable.innerHTML = '';
    }
}
