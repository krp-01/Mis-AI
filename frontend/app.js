let profile = null;

function showLogin() {
    document.getElementById("loginBox").style.display = "block";
    document.getElementById("signupBox").style.display = "none";
    document.getElementById("showLoginBtn").classList.add("active");
    document.getElementById("showSignupBtn").classList.remove("active");
}

function showSignup() {
    document.getElementById("loginBox").style.display = "none";
    document.getElementById("signupBox").style.display = "block";
    document.getElementById("showSignupBtn").classList.add("active");
    document.getElementById("showLoginBtn").classList.remove("active");
}

function valueToTrait(value, highTrait, lowTrait) {
    return value >= 4 ? highTrait : lowTrait;
}

function validScore(value) {
    return !isNaN(value) && value >= 1 && value <= 5;
}

async function signup() {
    const username = document.getElementById("signupUser").value.trim().toLowerCase();
    const display_name = document.getElementById("signupName").value.trim();
    const password = document.getElementById("signupPass").value.trim();

    const risc = parseInt(document.getElementById("q_risc").value);
    const social = parseInt(document.getElementById("q_social").value);
    const organizare = parseInt(document.getElementById("q_organizare").value);
    const emotie = parseInt(document.getElementById("q_emotie").value);
    const rabdare = parseInt(document.getElementById("q_rabdare").value);
    const adaptare = parseInt(document.getElementById("q_adaptare").value);
    const disciplina = parseInt(document.getElementById("q_disciplina").value);
    const incredere = parseInt(document.getElementById("q_incredere").value);

    if (!username || !display_name || !password) {
        alert("Completeaza username, nume afisat si parola.");
        return;
    }

    const scores = [risc, social, organizare, emotie, rabdare, adaptare, disciplina, incredere];
    if (!scores.every(validScore)) {
        alert("Toate raspunsurile din test trebuie sa fie numere intre 1 si 5.");
        return;
    }

    const body = {
        username,
        display_name,
        password,
        risc: valueToTrait(risc, "curajos", "prudent"),
        social: valueToTrait(social, "extrovertit", "rezervat"),
        organizare: valueToTrait(organizare, "organizat", "spontan"),
        emotie: valueToTrait(emotie, "emotional", "rational"),
        rabdare: valueToTrait(rabdare, "rabdator", "nerabdator"),
        adaptare: valueToTrait(adaptare, "flexibil", "constant"),
        disciplina: valueToTrait(disciplina, "disciplinat", "relaxat"),
        incredere: valueToTrait(incredere, "increzator", "retinut")
    };

    const res = await fetch("https://mis-ai.onrender.com/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });

    const data = await res.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    alert("Cont creat cu succes. Acum te poti loga.");
    showLogin();
}

async function login() {
    const username = document.getElementById("loginUser").value.trim().toLowerCase();
    const password = document.getElementById("loginPass").value.trim();

    if (!username || !password) {
        alert("Completeaza username si parola.");
        return;
    }

    const res = await fetch("https://mis-ai.onrender.com/signin", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    profile = data.profile;

    document.getElementById("authScreen").style.display = "none";
    document.getElementById("chatScreen").style.display = "flex";

    document.getElementById("profileName").textContent = profile.display_name || "Utilizator";
    document.getElementById("profileUser").textContent = "@" + (profile.username || "username");

    const chat = document.getElementById("chat");
    chat.innerHTML = "";

    if (data.history && data.history.length > 0) {
        for (const item of data.history) {
            const type = item.speaker === "Tu" ? "user" : "ai";
            addMessage(item.message, type);
        }
    } else {
        addMessage("Salut! Bine ai venit in MIS.", "ai");
    }
}

function logout() {
    profile = null;
    document.getElementById("chatScreen").style.display = "none";
    document.getElementById("authScreen").style.display = "flex";
}

function getMode() {
    const checked = document.querySelector('input[name="mode"]:checked');
    return checked ? checked.value : "local";
}

function addMessage(text, type) {
    const chat = document.getElementById("chat");
    const div = document.createElement("div");
    div.className = "bubble " + type;
    div.textContent = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

async function send() {
    const input = document.getElementById("msg");
    const message = input.value.trim();

    if (!message || !profile) {
        return;
    }

    addMessage(message, "user");
    input.value = "";

    const res = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            message: message,
            profile: profile,
            mode: getMode()
        })
    });

    const data = await res.json();

    if (data.error) {
        addMessage("Eroare: " + data.error, "ai");
        return;
    }

    addMessage(data.response, "ai");
}

function handleEnter(event) {
    if (event.key === "Enter") {
        send();
    }
}