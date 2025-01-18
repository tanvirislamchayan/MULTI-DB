window.addEventListener("load", function() {
    const loaderSection = document.getElementById("loaderBody");
    loaderSection.style.display = "none";
});

document.addEventListener('DOMContentLoaded', () => {
    const errMsg = document.getElementById('error-message');
    const scsMsg = document.getElementById('success-message');
    errMsg.classList.add('d-none');
    scsMsg.classList.add('d-none');
    const subdomainInput = document.getElementById('subdomain');
    subdomainInput.addEventListener('input', () => {
        
    });
});