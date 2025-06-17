

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
    // 1. Функция переключения видимости пароля (только на странице входа)
    const togglePassword = document.getElementById('togglePassword');
    if (togglePassword) {
        togglePassword.addEventListener('click', function() {
            const passwordInput = document.getElementById('id_password');
            if (passwordInput) {
                const type = passwordInput.type === 'password' ? 'text' : 'password';
                passwordInput.type = type;

                // Переключение иконки
                const icon = this.querySelector('i');
                if (icon) {
                    icon.classList.toggle('bi-eye');
                    icon.classList.toggle('bi-eye-slash');
                }
            }
        });
    }

    // 2. Обработчик для кнопки входа (только на странице входа)
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        const loginBtn = loginForm.querySelector('#login-btn');
        if (loginBtn) {
            loginBtn.addEventListener('click', function() {
                const loginText = document.getElementById('login-text');
                const loginSpinner = document.getElementById('login-spinner');

                if (loginText && loginSpinner) {
                    loginText.classList.add('d-none');
                    loginSpinner.classList.remove('d-none');
                    this.disabled = true;

                    // Автоматическая отправка формы
                    loginForm.submit();
                }
            });
        }
    }

    // 3. Валидация форм (для всех форм с классом needs-validation)
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

    // 4. Инициализация tooltips (если Bootstrap доступен)
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.forEach(tooltipTriggerEl => {
            new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // 5. Обработчик для кнопки "Показать больше"
//    const showMoreBtn = document.getElementById('show-more');
//    if (showMoreBtn) {
//        showMoreBtn.addEventListener('click', function() {
//            const hiddenContent = document.querySelectorAll('.content-hidden');
//            hiddenContent.forEach(item => {
//                item.classList.remove('d-none');
//            });
//            this.classList.add('d-none');
//        });
//    }
});