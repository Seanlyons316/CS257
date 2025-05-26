function SendtoPage(page) {
    let url = window.location.protocol
                + '//' + window.location.hostname
                + ':' + window.location.port
                + '/'
                + page;
        window.location.href = url;
}
