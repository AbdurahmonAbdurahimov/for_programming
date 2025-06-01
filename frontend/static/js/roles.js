
document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("access_token");

    fetch("/api/v1/users/me", {
        headers: { Authorization: token }
    })
    .then(res => res.json())
    .then(user => {
        const role = user.role;
        if (role === "cook") {
            document.querySelectorAll(".admin-only, .manager-only").forEach(e => e.remove());
        } else if (role === "manager") {
            document.querySelectorAll(".admin-only").forEach(e => e.remove());
        }
        document.getElementById("welcome-role").textContent = `Welcome, ${user.full_name} (${role})`;
    });
});
