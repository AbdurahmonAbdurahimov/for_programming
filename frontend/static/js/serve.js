
document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("access_token");
    const mealSelect = document.getElementById("meal-select");
    const form = document.getElementById("serve-form");
    const alertBox = document.getElementById("alert-box");
    const servedTable = document.querySelector("#served-meals-table tbody");

    function loadMeals() {
        fetch("/api/v1/meals/", {
            headers: { Authorization: token }
        })
        .then(res => res.json())
        .then(data => {
            mealSelect.innerHTML = data.map(meal =>
                `<option value="\${meal.id}">\${meal.name}</option>`
            ).join("");
        });
    }

    function loadServedMeals() {
        fetch("/api/v1/meals/served/", {
            headers: { Authorization: token }
        })
        .then(res => res.json())
        .then(data => {
            servedTable.innerHTML = data.map(log =>
                `<tr>
                    <td>\${log.meal.name}</td>
                    <td>\${log.served_by.full_name}</td>
                    <td>\${new Date(log.served_at).toLocaleString()}</td>
                </tr>`
            ).join("");
        });
    }

    form.addEventListener("submit", e => {
        e.preventDefault();
        const meal_id = mealSelect.value;
        fetch("/api/v1/meals/serve/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: token
            },
            body: JSON.stringify({ meal_id })
        })
        .then(res => res.json().then(data => ({ status: res.status, body: data })))
        .then(result => {
            if (result.status === 200) {
                alertBox.classList.add("d-none");
                loadServedMeals();
            } else {
                alertBox.textContent = result.body.detail || "Error";
                alertBox.classList.remove("d-none");
            }
        });
    });

    loadMeals();
    loadServedMeals();
});
