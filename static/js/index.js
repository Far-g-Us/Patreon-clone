

// $("#search_input_box").hide();
// $("#search").on("click", function () {
//     $("#search_input_box").slideToggle();
//     $("#search_input").focus();
// });
// $("#close_search").on("click", function () {
//     $('#search_input_box').slideUp(500);
// });




document.addEventListener('DOMContentLoaded', function() {
    // 1. Обработчик для кнопки входа (только если элементы существуют)
    const loginForm = document.getElementById('login-form');
    const loginBtn = document.getElementById('login-btn');

    if (loginForm && loginBtn) {
        loginBtn.addEventListener('click', function() {
            const loginText = document.getElementById('login-text');
            const loginSpinner = document.getElementById('login-spinner');

            if (loginText && loginSpinner) {
                loginText.classList.add('d-none');
                loginSpinner.classList.remove('d-none');
                this.disabled = true;
                loginForm.submit();
            }
        });
    }

    // 2. Валидация форм
    const forms = document.querySelectorAll('.needs-validation');
    if (forms) {
        forms.forEach(form => {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });
    }

    // 3. Инициализация tooltips
    if (typeof bootstrap !== 'undefined') {
        const tooltipElements = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        if (tooltipElements) {
            tooltipElements.forEach(el => {
                new bootstrap.Tooltip(el);
            });
        }
    }

//    // 4. Обработчик для кнопки "Показать больше"
//    const showMoreBtn = document.getElementById('show-more');
//    if (showMoreBtn) {
//        showMoreBtn.addEventListener('click', function() {
//            const hiddenContent = document.querySelectorAll('.content-hidden');
//            if (hiddenContent) {
//                hiddenContent.forEach(item => {
//                    item.classList.remove('d-none');
//                });
//                this.classList.add('d-none');
//            }
//        });
//    }
});


// Кнопка "Наверх"
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    const btn = document.getElementById("scrollTopBtn");
    if (btn) {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            btn.style.display = "block";
        } else {
            btn.style.display = "none";
        }
    }
}

function topFunction() {
    window.scrollTo({top: 0, behavior: 'smooth'});
}
