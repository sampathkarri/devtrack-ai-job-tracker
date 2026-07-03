let accessToken = null;

// ==================== LOGIN ====================

async function login() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    const response = await fetch("http://127.0.0.1:8001/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: formData
    });

    const data = await response.json();

    if (response.ok) {

        accessToken = data.access_token;

        localStorage.setItem("token", accessToken);

        document.getElementById("loginPage").style.display = "none";
        document.getElementById("dashboardPage").style.display = "block";

        loadDashboard();

    } else {

        alert(data.detail);

    }

}

// ==================== DASHBOARD ====================

async function loadDashboard() {

    const response = await fetch("http://127.0.0.1:8001/dashboard/stats", {
        headers: {
            "Authorization": "Bearer " + accessToken
        }
    });

    const data = await response.json();

    document.getElementById("total").innerText = data.total_applications;
    document.getElementById("applied").innerText = data.applied;
    document.getElementById("interview").innerText = data.interview;
    document.getElementById("offer").innerText = data.offer;
    document.getElementById("rejected").innerText = data.rejected;

    loadApplications();

}

// ==================== LOAD APPLICATIONS ====================

async function loadApplications() {

    const response = await fetch("http://127.0.0.1:8001/applications/", {
        headers: {
            "Authorization": "Bearer " + accessToken
        }
    });

    const applications = await response.json();

    const table = document.getElementById("applicationBody");

    table.innerHTML = "";

    applications.forEach(app => {

        table.innerHTML += `
        <tr>
            <td>${app.company}</td>
            <td>${app.role}</td>
            <td>${app.status}</td>

            <td>
                <button onclick="editApplication(
                    ${app.id},
                    '${app.company}',
                    '${app.role}',
                    '${app.location}',
                    '${app.jd_text}'
                )">
                    Edit
                </button>

                <button onclick="deleteApplication(${app.id})">
                    Delete
                </button>
            </td>
        </tr>
        `;

    });

}

// ==================== ADD APPLICATION ====================

async function addApplication() {

    const company = document.getElementById("company").value;
    const role = document.getElementById("role").value;
    const location = document.getElementById("location").value;
    const jd = document.getElementById("jd").value;

    const response = await fetch("http://127.0.0.1:8001/applications/", {

        method: "POST",

        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + accessToken
        },

        body: JSON.stringify({
            company: company,
            role: role,
            location: location,
            jd_text: jd
        })

    });

    const data = await response.json();

    if (response.ok) {

        alert("Application Added Successfully!");

        document.getElementById("company").value = "";
        document.getElementById("role").value = "";
        document.getElementById("location").value = "";
        document.getElementById("jd").value = "";

        loadDashboard();

    } else {

        alert(JSON.stringify(data));

    }

}

// ==================== DELETE APPLICATION ====================

async function deleteApplication(id) {

    const confirmDelete = confirm("Are you sure you want to delete this application?");

    if (!confirmDelete) {
        return;
    }

    const response = await fetch(
        `http://127.0.0.1:8001/applications/${id}`,
        {
            method: "DELETE",
            headers: {
                "Authorization": "Bearer " + accessToken
            }
        }
    );

    const data = await response.json();

    if (response.ok) {

        alert("Application Deleted Successfully!");

        loadDashboard();

    } else {

        alert(data.detail);

    }

}
// ==================== EDIT APPLICATION ====================

let editingApplicationId = null;

function editApplication(id, company, role, location, jd_text) {

    editingApplicationId = id;

    document.getElementById("company").value = company;
    document.getElementById("role").value = role;
    document.getElementById("location").value = location;
    document.getElementById("jd").value = jd_text;

    document.getElementById("saveButton").innerText = "Update Application";

    document.getElementById("saveButton").setAttribute(
        "onclick",
        "updateApplication()"
    );

}
// ==================== UPDATE APPLICATION ====================

async function updateApplication() {

    const company = document.getElementById("company").value;
    const role = document.getElementById("role").value;
    const location = document.getElementById("location").value;
    const jd = document.getElementById("jd").value;

    const response = await fetch(
        `http://127.0.0.1:8001/applications/${editingApplicationId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + accessToken
            },
            body: JSON.stringify({
                company: company,
                role: role,
                location: location,
                jd_text: jd
            })
        }
    );

    const data = await response.json();

    if (response.ok) {

        alert("Application Updated Successfully!");

        editingApplicationId = null;

        document.getElementById("company").value = "";
        document.getElementById("role").value = "";
        document.getElementById("location").value = "";
        document.getElementById("jd").value = "";

        document.getElementById("saveButton").innerText = "Add Application";
        document.getElementById("saveButton").setAttribute(
            "onclick",
            "addApplication()"
        );

        loadDashboard();

    } else {

        alert(JSON.stringify(data));

    }

}

// ==================== LOGOUT ====================

function logout() {

    localStorage.removeItem("token");

    accessToken = null;

    document.getElementById("dashboardPage").style.display = "none";
    document.getElementById("loginPage").style.display = "block";

}

// ==================== AUTO LOGIN ====================

window.onload = function () {

    const token = localStorage.getItem("token");

    if (token) {

        accessToken = token;

        document.getElementById("loginPage").style.display = "none";
        document.getElementById("dashboardPage").style.display = "block";

        loadDashboard();

    }

}