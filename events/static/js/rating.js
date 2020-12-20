$(".rating a").on('click', function (e) {
    let value = $(this).data('value');
    console.log("value");
    console.log(value);
    $.ajax({
        url: "{% url 'profil-finished-events' %}",
        type: 'POST',
        data: {'rating': value},
        success: function (d) {
            // some processing
        }
    })
});

$("#send").on('click', function (e) {
    console.log("test confirm");
});
