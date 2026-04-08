const logArea = document.getElementById("logArea");
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");

// Rafraîchir les logs toutes les 2 secondes
function refreshLogs() {
    fetch("/logs")
        .then(response => response.json())
        .then(data => {
            logArea.textContent = data.logs.join("");
        })
        .catch(err => {
            logArea.textContent = "Erreur lors du chargement des logs";
        });
}

// Bouton Start
startBtn.addEventListener("click", () => {
    fetch("/start", {method: "POST"})
        .then(res => res.json())
        .then(data => alert(data.message))
        .catch(err => alert("Erreur: " + err));
});

// Bouton Stop
stopBtn.addEventListener("click", () => {
    fetch("/stop", {method: "POST"})
        .then(res => res.json())
        .then(data => alert(data.message))
        .catch(err => alert("Erreur: " + err));
});

// Rafraîchir les logs automatiquement
setInterval(refreshLogs, 2000);
refreshLogs(); // Premier affichage


