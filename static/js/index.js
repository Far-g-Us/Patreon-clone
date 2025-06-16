

// $("#search_input_box").hide();
// $("#search").on("click", function () {
//     $("#search_input_box").slideToggle();
//     $("#search_input").focus();
// });
// $("#close_search").on("click", function () {
//     $('#search_input_box').slideUp(500);
// });


document.getElementById('logout-btn').addEventListener('click', function(e) {
    e.preventDefault();
    if (confirm('Вы уверены, что хотите выйти?')) {
        fetch("{% url 'logout' %}", {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json'
            }
        }).then(response => {
            if (response.ok) {
                window.location.href = "{% url 'home' %}";
            }
        });
    }
});