// const modal = document.getElementById('auth-modal');
// const loginBtn = document.getElementById('login-btn');
// const registerBtn = document.getElementById('register-btn');
// const closeBtn = document.querySelector('.close-btn');
// const authForm = document.getElementById('auth-form');
// const submitBtn = document.getElementById('submit-auth');

// let isLogin = true;

// loginBtn.onclick = () => {
//     isLogin = true;
//     submitBtn.textContent = "Войти";
//     modal.classList.remove('hidden');
// };

// registerBtn.onclick = () => {
//     isLogin = false;
//     submitBtn.textContent = "Зарегистрироваться";
//     modal.classList.remove('hidden');
// };

// closeBtn.onclick = () => modal.classList.add('hidden');

// authForm.onsubmit = async (e) => {
//     e.preventDefault();

//     const email = document.getElementById("email").value;
//     const password = document.getElementById("password").value;

//     const url = isLogin ? "/api/v1/auth/login" : "/api/v1/auth/register";
//     const method = "POST";

//     const response = await fetch(url, {
//         method,
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ email, password }),
//     });

//     if (response.ok) {
//         const data = await response.json();
//         alert("Успешно!");
//         localStorage.setItem("access_token", data.access_token || "");
//         window.location.href = "/dashboard";
//     } else {
//         alert("Ошибка авторизации или регистрации");
//     }
// };
const modal = document.getElementById('auth-modal');
const loginBtn = document.getElementById('login-btn');
const registerBtn = document.getElementById('register-btn');
const closeBtn = document.querySelector('.close-btn');
const authForm = document.getElementById('auth-form');
const submitBtn = document.getElementById('submit-auth');
const formTitle = document.getElementById('form-title');
const switchAuth = document.getElementById('switch-auth');
const togglePassword = document.getElementById('toggle-password');
const passwordInput = document.getElementById('password');
let isLogin = true;

async function getCsrfToken() {
    const response = await fetch('http://localhost:8000/', {
        method: 'GET',
        credentials: 'include',
    });
    if (!response.ok) throw new Error('Failed to fetch CSRF token');
    const data = await response.json();
    return data.csrf_token;
}

function showModal(mode) {
    isLogin = mode === 'login';
    modal.classList.remove('hidden');
    modal.classList.add('show');
    formTitle.textContent = isLogin ? 'Вход' : 'Регистрация';
    submitBtn.textContent = isLogin ? 'Войти' : 'Зарегистрироваться';
    switchAuth.innerHTML = isLogin
        ? 'Еще нет аккаунта? <a href="#" id="switch-to-register">Зарегистрироваться</a>'
        : 'Уже есть аккаунт? <a href="#" id="switch-to-register">Войти</a>';
}

function hideModal() {
    modal.classList.remove('show');
    setTimeout(() => modal.classList.add('hidden'), 300);
}

loginBtn.onclick = () => showModal('login');
registerBtn.onclick = () => showModal('register');

document.body.addEventListener('click', (e) => {
    if (e.target.id === 'switch-to-register') {
        showModal(isLogin ? 'register' : 'login');
        e.preventDefault();
    }
});

togglePassword.onclick = () => {
    passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
    togglePassword.style.color = passwordInput.type === 'text' ? '#00bfff' : 'rgba(255, 255, 255, 0.7)';
};

authForm.onsubmit = async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = passwordInput.value;

    if (!email.includes("@") || !email.includes(".")) {
        alert("Введите корректный email");
        return;
    }

    const url = isLogin ? 'http://localhost:8000/api/v1/auth/login' : 'http://localhost:8000/api/v1/auth/register';

    try {
        const csrfToken = await getCsrfToken();
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRF-Token": csrfToken,
            },
            body: JSON.stringify({ email, password }),
            credentials: 'include',
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem("access_token", data.access_token);
            alert("Успешно!");
            window.location.href = "/dashboard";
        } else {
            const error = await response.json();
            alert(`Ошибка: ${error.detail || "Неизвестная ошибка"}`);
        }
    } catch (error) {
        alert(`Ошибка: ${error.message}`);
    }
};
