console.log("main.js загружен");

document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById('auth-modal');
    const loginBtn = document.getElementById('login-btn');
    const registerBtn = document.getElementById('register-btn');
    const closeBtn = document.querySelector('.close-btn');
    const authForm = document.getElementById('auth-form');
    const submitBtn = document.getElementById('submit-auth');
    const formTitle = document.getElementById('form-title');
    const switchAuth = document.getElementById('switch-auth');
    const togglePassword = document.getElementById('toggle-password');
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");

    let isLogin = true;

    function showModal() {
        modal.classList.remove("hidden");
        modal.classList.add("show");
    }

    function hideModal() {
        modal.classList.remove("show");
        modal.classList.add("hidden");
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

    loginBtn.onclick = () => {
        isLogin = true;
        formTitle.textContent = "Вход";
        submitBtn.textContent = "Войти";
        switchAuth.innerHTML = `Еще нет аккаунта? <a href="#" id="switch-to-register">Зарегистрироваться</a>`;
        showModal();
        bindSwitch();
    };

    registerBtn.onclick = () => {
        isLogin = false;
        formTitle.textContent = "Регистрация";
        submitBtn.textContent = "Зарегистрироваться";
        switchAuth.innerHTML = `Уже есть аккаунт? <a href="#" id="switch-to-login">Войти</a>`;
        showModal();
        bindSwitch();
    };

    closeBtn.onclick = () => hideModal();

    togglePassword.onclick = () => {
        const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
        passwordInput.setAttribute("type", type);
    };

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
});
