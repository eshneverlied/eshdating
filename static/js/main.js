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


    if (tgForm) {
        tgForm.onsubmit = async (e) => {
            e.preventDefault();

            const sessionName = document.getElementById('session-name').value.trim();
            const apiId = parseInt(document.getElementById('api-id').value.trim(), 10);
            const apiHash = document.getElementById('api-hash').value.trim();
            const phone = document.getElementById('phone').value.trim();
            const otp = document.getElementById('otp').value.trim();
            const password = document.getElementById('session-password').value.trim() || null;

            const base = '/api/v1/telegram/sessions';

            try {
                let response = await fetch(`${base}/start`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include',
                    body: JSON.stringify({ session_name: sessionName, api_id: apiId, api_hash: apiHash })
                });
                if (!response.ok) {
                    const err = await response.json();
                    throw new Error(err.detail || 'Ошибка инициализации');
                }

                response = await fetch(`${base}/phone`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include',
                    body: JSON.stringify({ session_name: sessionName, phone })
                });
                if (!response.ok) {
                    const err = await response.json();
                    throw new Error(err.detail || 'Ошибка отправки телефона');
                }

                response = await fetch(`${base}/confirm`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include',
                    body: JSON.stringify({ session_name: sessionName, otp, password })
                });

                if (response.ok) {
                    alert('Сессия создана');
                    tgForm.reset();
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
