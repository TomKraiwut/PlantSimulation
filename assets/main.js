// Plant Simulation Tutorial — off-canvas sidebar behaviour (generic, no page-specific logic)
(function () {
    var wrapper = document.getElementById('wrapper');
    var toggle = document.querySelector('.menu-toggle');
    var overlay = document.getElementById('sidebar-overlay');
    var closeBtn = document.querySelector('.sidebar-close');

    function setOpen(open) {
        wrapper.classList.toggle('sidebar-active', open);
        if (toggle) toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        if (open) {
            // bring the current chapter into view in a long menu
            var sidebar = document.getElementById('sidebar');
            var active = document.querySelector('#menu li.active');
            if (sidebar && active) {
                sidebar.scrollTop = active.offsetTop - sidebar.clientHeight / 2;
            }
        }
    }

    function closeSidebar() {
        setOpen(false);
    }

    function toggleSidebar() {
        setOpen(!wrapper.classList.contains('sidebar-active'));
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

    if (closeBtn) {
        closeBtn.addEventListener('click', closeSidebar);
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
