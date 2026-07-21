const API_BASE = "http://127.0.0.1:8001";

let accessToken = localStorage.getItem("token") || null;
let currentPage = 1;
const limit = 5;
let editingApplicationId = null;

/* ==================== HELPERS ==================== */

function getAuthHeaders(isJson = true) {
    const headers = {};
    if (isJson) headers["Content-Type"] = "application/json";
    if (accessToken) headers["Authorization"] = "Bearer " + accessToken;
    return headers;
}

async function handleResponse(response) {
    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(data.detail || "Something went wrong");
    }

    return data;
}

function resetApplicationForm() {
    document.getElementById("company").value = "";
    document.getElementById("role").value = "";
    document.getElementById("location").value = "";
    document.getElementById("jd").value = "";
    editingApplicationId = null;

    const saveButton = document.getElementById("saveButton");
    saveButton.innerText = "Add Application";
    saveButton.setAttribute("onclick", "addApplication()");
}

function showDashboard() {
    document.getElementById("loginPage").style.display = "none";
    document.getElementById("dashboardPage").style.display = "block";
}

function showLogin() {
    document.getElementById("dashboardPage").style.display = "none";
    document.getElementById("loginPage").style.display = "block";
}

/* ==================== LOGIN ==================== */

async function login() {
    try {
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();

        const formData = new URLSearchParams();
        formData.append("username", email);
        formData.append("password", password);

        const response = await fetch(`${API_BASE}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: formData
        });

        const data = await handleResponse(response);

        accessToken = data.access_token;
        localStorage.setItem("token", accessToken);

        showDashboard();
        loadDashboard();
    } catch (error) {
        alert(error.message);
    }
}

/* ==================== DASHBOARD ==================== */

async function loadDashboard() {
    try {
        const response = await fetch(`${API_BASE}/dashboard/stats`, {
            headers: getAuthHeaders(false)
        });

        const data = await handleResponse(response);

        document.getElementById("total").innerText = data.total_applications || 0;
        document.getElementById("applied").innerText = data.applied || 0;
        document.getElementById("interview").innerText = data.interview || 0;
        document.getElementById("offer").innerText = data.offer || 0;
        document.getElementById("rejected").innerText = data.rejected || 0;

        loadApplications();
    } catch (error) {
        alert(error.message);
    }
}

/* ==================== LOAD APPLICATIONS ==================== */

async function loadApplications() {
    try {
        const search = document.getElementById("search").value.trim();

        const response = await fetch(
            `${API_BASE}/applications/?search=${encodeURIComponent(search)}&page=${currentPage}&limit=${limit}`,
            {
                headers: getAuthHeaders(false)
            }
        );

        const applications = await handleResponse(response);
        const table = document.getElementById("applicationBody");
        table.innerHTML = "";

        applications.forEach(app => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${app.company || ""}</td>
                <td>${app.role || ""}</td>
                <td><span class="status ${String(app.status || "").toLowerCase()}">${app.status || "Saved"}</span></td>
                <td>
                    <button onclick="editApplication(${app.id})">Edit</button>
                    <button onclick="deleteApplication(${app.id})">Delete</button>
                </td>
            `;

            row.dataset.company = app.company || "";
            row.dataset.role = app.role || "";
            row.dataset.location = app.location || "";
            row.dataset.jd = app.jd_text || "";

            table.appendChild(row);
        });
    } catch (error) {
        alert(error.message);
    }
}

/* ==================== ADD APPLICATION ==================== */

async function addApplication() {
    try {
        const company = document.getElementById("company").value.trim();
        const role = document.getElementById("role").value.trim();
        const location = document.getElementById("location").value.trim();
        const jd = document.getElementById("jd").value.trim();

        const response = await fetch(`${API_BASE}/applications/`, {
            method: "POST",
            headers: getAuthHeaders(true),
            body: JSON.stringify({
                company,
                role,
                location,
                jd_text: jd
            })
        });

        await handleResponse(response);

        alert("Application added successfully!");
        resetApplicationForm();
        loadDashboard();
    } catch (error) {
        alert(error.message);
    }
}

/* ==================== DELETE APPLICATION ==================== */

async function deleteApplication(id) {
    try {
        const confirmDelete = confirm("Are you sure you want to delete this application?");
        if (!confirmDelete) return;

        const response = await fetch(`${API_BASE}/applications/${id}`, {
            method: "DELETE",
            headers: getAuthHeaders(false)
        });

        if (response.status === 204) {
            alert("Application deleted successfully!");
            loadDashboard();
            return;
        }

        await handleResponse(response);
        alert("Application deleted successfully!");
        loadDashboard();
    } catch (error) {
        alert(error.message);
    }
}

/* ==================== EDIT APPLICATION ==================== */

function editApplication(id) {
    const rows = document.querySelectorAll("#applicationBody tr");

    for (const row of rows) {
        const editButton = row.querySelector("button");
        if (editButton && editButton.getAttribute("onclick") === `editApplication(${id})`) {
            editingApplicationId = id;
            document.getElementById("company").value = row.dataset.company || "";
            document.getElementById("role").value = row.dataset.role || "";
            document.getElementById("location").value = row.dataset.location || "";
            document.getElementById("jd").value = row.dataset.jd || "";

            const saveButton = document.getElementById("saveButton");
            saveButton.innerText = "Update Application";
            saveButton.setAttribute("onclick", "updateApplication()");
            break;
        }
    }
}

/* ==================== UPDATE APPLICATION ==================== */

async function updateApplication() {
    try {
        const company = document.getElementById("company").value.trim();
        const role = document.getElementById("role").value.trim();
        const location = document.getElementById("location").value.trim();
        const jd = document.getElementById("jd").value.trim();

        const response = await fetch(`${API_BASE}/applications/${editingApplicationId}`, {
            method: "PUT",
            headers: getAuthHeaders(true),
            body: JSON.stringify({
                company,
                role,
                location,
                jd_text: jd
            })
        });

        await handleResponse(response);

        alert("Application updated successfully!");
        resetApplicationForm();
        loadDashboard();
    } catch (error) {
        alert(error.message);
    }
}

/* ==================== LOGOUT ==================== */

function logout() {
    localStorage.removeItem("token");
    accessToken = null;
    resetApplicationForm();
    showLogin();
}

/* ==================== PAGINATION ==================== */

function nextPage() {
    currentPage++;
    document.getElementById("pageNumber").innerText = `Page ${currentPage}`;
    loadApplications();
}

function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        document.getElementById("pageNumber").innerText = `Page ${currentPage}`;
        loadApplications();
    }
}

/* ==================== AI STATUS PREDICTION ==================== */

async function predictStatus() {
    try {
        const note = document.getElementById("note").value.trim();

        const response = await fetch(`${API_BASE}/ai/tag-suggestion`, {
            method: "POST",
            headers: getAuthHeaders(true),
            body: JSON.stringify({ note })
        });

        const data = await handleResponse(response);

        document.getElementById("predictionResult").innerHTML = `
            <div class="card">
                <h3>AI Prediction</h3>
                <h1>${data.suggested_status}</h1>
            </div>
        `;
    } catch (error) {
        alert(error.message);
    }
}

/* ==================== AUTO LOGIN ==================== */

window.onload = function () {
    const token = localStorage.getItem("token");

    if (token) {
        accessToken = token;
        showDashboard();
        loadDashboard();
    } else {
        showLogin();
    }
};