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


    const step1Form = document.getElementById('tg-step1-form');
    const step2Form = document.getElementById('tg-step2-form');
    const step3Form = document.getElementById('tg-step3-form');
    const statusMessage = document.getElementById('status-message');

    const updateStatus = (msg) => {
        if (statusMessage) statusMessage.textContent = msg;
        console.log(msg);
    };

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


    let sessionName = '';
    let apiId = 0;
    let apiHash = '';

    if (step1Form) {
        step1Form.onsubmit = async (e) => {
            e.preventDefault();

            sessionName = document.getElementById('session-name').value.trim();
            apiId = parseInt(document.getElementById('api-id').value.trim(), 10);
            apiHash = document.getElementById('api-hash').value.trim();

            try {
                updateStatus('Отправляем данные...');
                const resp = await fetch('/api/v1/telegram/sessions/start', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include',
                    body: JSON.stringify({ session_name: sessionName, api_id: apiId, api_hash: apiHash })

                });
                if (!resp.ok) {
                    const err = await resp.json();
                    throw new Error(err.detail || 'Ошибка');
                }

                step1Form.classList.add('hidden');
                step2Form.classList.remove('hidden');
                updateStatus('Введите номер телефона');

            } catch (err) {
                alert(err.message || 'Ошибка');
            }
        };
    }


    if (step2Form) {
        step2Form.onsubmit = async (e) => {
            e.preventDefault();

            const phone = document.getElementById('phone').value.trim();

            try {
                updateStatus('Отправляем номер...');
                const resp = await fetch('/api/v1/telegram/sessions/phone', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include',
                    body: JSON.stringify({ session_name: sessionName, phone })

                });
                if (!resp.ok) {
                    const err = await resp.json();
                    throw new Error(err.detail || 'Ошибка');

                }
                step2Form.classList.add('hidden');
                step3Form.classList.remove('hidden');
                updateStatus('Введите код из SMS');
            } catch (err) {
                alert(err.message || 'Ошибка');
            }
        };
    }

    if (step3Form) {
        step3Form.onsubmit = async (e) => {
            e.preventDefault();

            const otp = document.getElementById('otp').value.trim();
            const password = document.getElementById('session-password').value.trim() || null;

            try {
                updateStatus('Подтверждаем код...');
                const resp = await fetch('/api/v1/telegram/sessions/confirm', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include',
                    body: JSON.stringify({ session_name: sessionName, otp, password })
                });
                if (!resp.ok) {
                    const err = await resp.json();
                    throw new Error(err.detail || 'Ошибка');

                }
                alert('Сессия создана');
                updateStatus('Сессия успешно создана');
                step3Form.reset();
                step3Form.classList.add('hidden');
                step1Form.classList.remove('hidden');
            } catch (err) {
                alert(err.message || 'Ошибка');
            }
        };
    }
});
