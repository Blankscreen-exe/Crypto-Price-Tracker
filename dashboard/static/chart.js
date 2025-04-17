const ctx = document.getElementById("priceChart").getContext("2d");

const chart = new Chart(ctx, {
    type: "line",
    data: {
        labels: PRICE_DATA.timestamps, // Populated by Jinja2 from backend
        datasets: [
            {
                label: "Price (USD)",
                data: PRICE_DATA.prices,
                borderColor: "#007bff",
                fill: false,
                tension: 0.1,
            },
            {
                label: "7d Moving Avg",
                data: PRICE_DATA.moving_avg,
                borderColor: "#28a745",
                fill: false,
                borderDash: [5, 5],
                tension: 0.1,
            },
        ],
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: "top",
            },
            title: {
                display: true,
                text: "Bitcoin Price Tracker",
            },
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: "Timestamp",
                },
                ticks: {
                    autoSkip: true,
                    maxTicksLimit: 10,
                },
            },
            y: {
                title: {
                    display: true,
                    text: "Price (USD)",
                },
                beginAtZero: false,
            },
        },
    },
});