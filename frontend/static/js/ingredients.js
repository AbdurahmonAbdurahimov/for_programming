
document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("access_token");
    const tableBody = document.querySelector("#ingredients-table tbody");

    function fetchIngredients() {
        fetch("/api/v1/ingredients/", {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
        .then(res => res.json())
        .then(data => {
            tableBody.innerHTML = "";
            data.forEach(item => {
                tableBody.innerHTML += `
                    <tr>
                        <td>${item.name}</td>
                        <td>${item.quantity}</td>
                        <td>${item.delivery_date || ''}</td>
                        <td>
                            <button class="btn btn-danger btn-sm">Delete</button>
                        </td>
                    </tr>
                `;
            });
        });
    }

    document.querySelector("#ingredient-form").addEventListener("submit", e => {
        e.preventDefault();
        const name = document.querySelector("#name").value;
        const quantity = parseFloat(document.querySelector("#quantity").value);
        const delivery_date = document.querySelector("#delivery_date").value;

        fetch("/api/v1/ingredients/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({ name, quantity, delivery_date })
        })
        .then(res => {
            if (res.ok) {
                fetchIngredients();
                e.target.reset();
            } else {
                alert("Failed to add ingredient.");
            }
        });
    });

    fetchIngredients();
});
