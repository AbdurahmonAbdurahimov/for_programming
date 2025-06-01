
const ws = new WebSocket("ws://localhost:8000/ws/inventory/");
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === "low_stock") {
        alert("⚠️ LOW STOCK: " + data.ingredient);
    }
};
