async function toggleMonitor() {
    const btn = document.getElementById('monitorBtn');
    const isStarting = btn.innerText.includes("Start");
    const route = isStarting ? '/start' : '/stop';

    try {
        const response = await fetch(route);
        if (response.ok) {
            if (isStarting) {
                btn.innerText = "Stop Monitoring";
                btn.classList.replace('bg-green-600', 'bg-red-600');
                document.getElementById('statusLabel').innerText = "Running";
            } else {
                btn.innerText = "Start Monitoring";
                btn.classList.replace('bg-red-600', 'bg-green-600');
                document.getElementById('statusLabel').innerText = "Stopped";
            }
        }
    } catch (err) {
        console.error("Connection failed:", err);
    }
}

function runBackend() {
     console.log("Button clicked");
     
    fetch("/run")
        .then(res => res.json())
        .then(data => {
            alert(data.status);
            console.log(data);
        })
        .catch(err => console.error(err));
}

