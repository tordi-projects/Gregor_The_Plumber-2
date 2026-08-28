// Collapse the mobile navbar automatically after a link is clicked.
document.addEventListener('DOMContentLoaded', function () {
    var navLinks = document.querySelectorAll('#mainNav .nav-link');
    var navCollapse = document.getElementById('mainNav');

    navLinks.forEach(function (link) {
        link.addEventListener('click', function () {
            if (navCollapse.classList.contains('show')) {
                var bsCollapse = bootstrap.Collapse.getOrCreateInstance(navCollapse);
                bsCollapse.hide();
            }
        });
    });

    // Auto-dismiss alerts after 6 seconds
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alertEl) {
        setTimeout(function () {
            var bsAlert = bootstrap.Alert.getOrCreateInstance(alertEl);
            if (bsAlert) bsAlert.close();
        }, 6000);
    });
});
