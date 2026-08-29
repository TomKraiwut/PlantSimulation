// Plant Simulation Tutorial — off-canvas sidebar behaviour (generic, no page-specific logic)
(function () {
    var wrapper = document.getElementById('wrapper');
    var toggle = document.querySelector('.menu-toggle');
    var overlay = document.getElementById('sidebar-overlay');

    function closeSidebar() {
        wrapper.classList.remove('sidebar-active');
    }

    function toggleSidebar() {
        wrapper.classList.toggle('sidebar-active');
    }

    if (toggle) {
        toggle.addEventListener('click', function (e) {
            e.stopPropagation();
            toggleSidebar();
        });
    }

    if (overlay) {
        overlay.addEventListener('click', closeSidebar);
    }

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeSidebar();
    });

    document.querySelectorAll('.submenu-toggle').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            var li = btn.closest('li.has-children');
            if (li) li.classList.toggle('expanded');
        });
    });
})();
