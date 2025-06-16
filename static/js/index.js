

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

document.addEventListener('DOMContentLoaded', function() {
    // Функция для показа/скрытия пароля
    const togglePassword = document.getElementById('togglePassword');
    if (togglePassword) {
        togglePassword.addEventListener('click', function() {
            const passwordInput = document.getElementById('id_password');
            if (passwordInput) {
                const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordInput.setAttribute('type', type);
                this.classList.toggle('bi-eye');
                this.classList.toggle('bi-eye-slash');
            }
        });
    }

    // Обработчик для кнопки входа
    const loginBtn = document.getElementById('login-btn');
    if (loginBtn) {
        loginBtn.addEventListener('click', function(e) {
            const loginText = document.getElementById('login-text');
            const loginSpinner = document.getElementById('login-spinner');

            if (loginText && loginSpinner) {
                loginText.classList.add('d-none');
                loginSpinner.classList.remove('d-none');
                this.disabled = true;
            }
        });
    }

    // Обработчик для форм с классом .needs-validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Инициализация tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});