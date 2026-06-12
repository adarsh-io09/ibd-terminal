// Live time in sidebar
setInterval(() => {
    const now = new Date();
    document.getElementById('live-time').innerText = now.toLocaleTimeString('en-US', { hour12: false });
}, 1000);

// Humor quotes rotation
const quotes = [
    "Associate hasn’t slept in 48 hours.",
    "Model broke before MD review.",
    "Client wants upside with zero dilution.",
    "This comp set looks trash.",
    "Mgmt adjusted EBITDA kaafi aggressive lag raha hai.",
    "Sponsor pushing tighter exclusivity.",
    "Legal ne phir markup bhej diya.",
    "Data room abhi incomplete hai."
];
let i = 0;
setInterval(() => {
    document.getElementById('humor-quote').innerText = quotes[i % quotes.length];
    i++;
}, 8000);
