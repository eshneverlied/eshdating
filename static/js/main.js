const modal = document.getElementById('auth-modal');
const loginBtn = document.getElementById('login-btn');
const registerBtn = document.getElementById('register-btn');
const closeBtn = document.querySelector('.close-btn');
const authForm = document.getElementById('auth-form');
const submitBtn = document.getElementById('submit-auth');

let isLogin = true;

loginBtn.onclick = () => {
    isLogin = true;
    submitBtn.textContent = "Войти";
    modal.classList.remove('hidden');
};

registerBtn.onclick = () => {
    isLogin = false;
    submitBtn.textContent = "Зарегистрироваться";
    modal.classList.remove('hidden');
};

closeBtn.onclick = () => modal.classList.add('hidden');

authForm.onsubmit = async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const url = isLogin ? "/api/v1/auth/login" : "/api/v1/auth/register";

    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
        alert("Успешно!");
        window.location.href = "/dashboard";
    } else {
        alert("Ошибка авторизации или регистрации");
    }
};
