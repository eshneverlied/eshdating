console.log("main.js загружен");

document.addEventListener("DOMContentLoaded", () => {
    const authModal = document.getElementById('auth-modal');
    const loginBtn = document.getElementById('login-btn');
    const registerBtn = document.getElementById('register-btn');
    const authCloseBtn = authModal ? authModal.querySelector('.close-btn') : null;
    const authForm = document.getElementById('auth-form');
    const submitBtn = document.getElementById('submit-auth');
    const formTitle = document.getElementById('form-title');
    const switchAuth = document.getElementById('switch-auth');
    const togglePassword = document.getElementById('toggle-password');
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");

    const tgModal = document.getElementById('telegram-modal');
    const addTgBtn = document.getElementById('add-telegram-btn');
    const tgCloseBtn = tgModal ? tgModal.querySelector('.close-btn') : null;
    const tgForm = document.getElementById('telegram-form');

    let isLogin = true;

    function showModal(element) {
        if (element) {
            element.classList.remove("hidden");
            element.classList.add("show");
        }
    }

    function hideModal(element) {
        if (element) {
            element.classList.remove("show");
            element.classList.add("hidden");
        }
    }

    function bindSwitch() {
        const switchToRegister = document.getElementById("switch-to-register");
        const switchToLogin = document.getElementById("switch-to-login");

        if (switchToRegister) {
            switchToRegister.onclick = (e) => {
                e.preventDefault();
                isLogin = false;
                formTitle.textContent = "Регистрация";
                submitBtn.textContent = "Зарегистрироваться";
                switchAuth.innerHTML = `Уже есть аккаунт? <a href="#" id="switch-to-login">Войти</a>`;
                bindSwitch();
            };
        }

        if (switchToLogin) {
            switchToLogin.onclick = (e) => {
                e.preventDefault();
                isLogin = true;
                formTitle.textContent = "Вход";
                submitBtn.textContent = "Войти";
                switchAuth.innerHTML = `Еще нет аккаунта? <a href="#" id="switch-to-register">Зарегистрироваться</a>`;
                bindSwitch();
            };
        }
    }

    if (loginBtn) {
        loginBtn.onclick = () => {
            isLogin = true;
            formTitle.textContent = "Вход";
            submitBtn.textContent = "Войти";
            switchAuth.innerHTML = `Еще нет аккаунта? <a href="#" id="switch-to-register">Зарегистрироваться</a>`;
            showModal(authModal);
            bindSwitch();
        };
    }

    if (registerBtn) {
        registerBtn.onclick = () => {
            isLogin = false;
            formTitle.textContent = "Регистрация";
            submitBtn.textContent = "Зарегистрироваться";
            switchAuth.innerHTML = `Уже есть аккаунт? <a href="#" id="switch-to-login">Войти</a>`;
            showModal(authModal);
            bindSwitch();
        };
    }

    if (authCloseBtn) {
        authCloseBtn.onclick = () => hideModal(authModal);
    }

    if (togglePassword) {
        togglePassword.onclick = () => {
            const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
            passwordInput.setAttribute("type", type);
        };
    }

    if (authForm) {
        authForm.onsubmit = async (e) => {
            e.preventDefault();

            const email = emailInput.value.trim();
            const password = passwordInput.value.trim();
            const url = isLogin ? "/api/v1/auth/login" : "/api/v1/auth/register";

            const response = await fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify({ email, password }),
            });

            if (response.ok) {
                window.location.href = "/dashboard";
            } else {
                const err = await response.json();
                alert(err.detail || "Ошибка");
            }
        };
    }

    if (addTgBtn) {
        addTgBtn.onclick = () => showModal(tgModal);
    }

    if (tgCloseBtn) {
        tgCloseBtn.onclick = () => hideModal(tgModal);
    }

    if (tgForm) {
        tgForm.onsubmit = async (e) => {
            e.preventDefault();

            const payload = {
                session_name: document.getElementById('session-name').value.trim(),
                api_id: parseInt(document.getElementById('api-id').value.trim(), 10),
                api_hash: document.getElementById('api-hash').value.trim(),
                phone: document.getElementById('phone').value.trim(),
                otp: document.getElementById('otp').value.trim(),
                password: document.getElementById('session-password').value.trim() || null,
            };

            try {
                const response = await fetch('/api/v1/telegram/sessions', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include',
                    body: JSON.stringify(payload),
                });

                if (response.ok) {
                    alert('Сессия создана');
                    tgForm.reset();
                    hideModal(tgModal);
                } else {
                    const err = await response.json();
                    alert(err.detail || 'Ошибка');
                }
            } catch (err) {
                alert(err.message || 'Ошибка');
            }
        };
    }
});
