document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.flash-msg').forEach(function (el) {
        setTimeout(function () {
            el.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            el.style.opacity = '0';
            el.style.transform = 'translateY(-8px)';
            setTimeout(function () { el.remove(); }, 300);
        }, 5000);
    });
});
