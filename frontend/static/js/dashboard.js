
document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("access_token");

    function loadDashboardData() {
        fetch("/api/v1/reports/dashboard/", {
            headers: {
                Authorization: token
            }
        })
        .then(res => res.json())
        .then(data => {
            const usageCtx = document.getElementById("usageChart").getContext("2d");
            const summaryCtx = document.getElementById("summaryChart").getContext("2d");

            new Chart(usageCtx, {
                type: "line",
                data: {
                    labels: data.usage.labels,
                    datasets: [
                        {
                            label: "Delivered",
                            data: data.usage.delivered,
                            borderColor: "green"
                        },
                        {
                            label: "Consumed",
                            data: data.usage.consumed,
                            borderColor: "red"
                        }
                    ]
                }
            });

            new Chart(summaryCtx, {
                type: "bar",
                data: {
                    labels: data.summary.labels,
                    datasets: [
                        {
                            label: "Served Portions",
                            data: data.summary.served,
                            backgroundColor: "blue"
                        },
                        {
                            label: "Could Have Served",
                            data: data.summary.possible,
                            backgroundColor: "gray"
                        }
                    ]
                }
            });

            if (data.summary.flagged) {
                const warning = document.getElementById("flag-warning");
                warning.classList.remove("d-none");
                warning.textContent = "⚠️ Warning: Misuse detected (discrepancy > 15%)";
            }
        });
    }

    loadDashboardData();
});
