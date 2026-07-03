let accessToken = null;

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

    console.log(data);

    if (response.ok) {

    accessToken = data.access_token;

    document.getElementById("loginPage").style.display = "none";

    document.getElementById("dashboardPage").style.display = "block";

    loadDashboard();

    } else {

        alert(data.detail);

    }
}
async function loadDashboard() {

    const response = await fetch("http://127.0.0.1:8001/dashboard/stats", {

        headers: {
            "Authorization": "Bearer " + accessToken
        }

    });

    const data = await response.json();

    console.log(data);

    document.getElementById("total").innerText = data.total_applications;
    document.getElementById("applied").innerText = data.applied;
    document.getElementById("interview").innerText = data.interview;
    document.getElementById("offer").innerText = data.offer;
    document.getElementById("rejected").innerText = data.rejected;
    loadApplications();
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
            </tr>
        `;

    });

}

}