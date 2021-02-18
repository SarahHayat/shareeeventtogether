$(document).ready(function () {

    $('#rating').on('click', function (e) {
        let id = $('#rating').attr('data-id')
        let url = $(this).attr("href")
        if (id != null) {
            url = url + '&event=' + id
        }
        window.location = url
        event.preventDefault()
    })

})
