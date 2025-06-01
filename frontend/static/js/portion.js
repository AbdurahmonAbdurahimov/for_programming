
document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("access_token");
    const portionTable = document.querySelector("#portion-table tbody");

    function loadPortionEstimates() {
        fetch("/api/v1/meals/portion-estimates/", {
            headers: {
                Authorization: token
            }
        })
        .then(res => res.json())
        .then(data => {
            portionTable.innerHTML = data.map(entry => `
                <tr>
                    <td>${entry.meal_name}</td>
                    <td>${entry.estimated_portions}</td>
                </tr>
            `).join("");
        });
    }

    loadPortionEstimates();
});
