	function toggleUserMenu() {
		const menu = document.getElementById("user-menu");
		menu.classList.toggle("hidden");
	}

	function toggleMobileMenu() {
		const menu = document.getElementById("mobile-menu");
		const menuIcon = document.getElementById("menu-icon");
		const closeIcon = document.getElementById("close-icon");

		menu.classList.toggle("hidden");
		menuIcon.classList.toggle("hidden");
		closeIcon.classList.toggle("hidden");
	}

	// Close dropdown when clicking outside
	document.addEventListener("click", function (event) {
		const userMenu = document.getElementById("user-menu");
		const userButton = event.target.closest('[onclick="toggleUserMenu()"]');

		if (!userButton && !event.target.closest("#user-menu")) {
			userMenu.classList.add("hidden");
		}
	});