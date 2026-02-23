const signInIcon = document.querySelector(".js-sign-in");
const authEl = document.getElementById("js-auth");

const loginUrl = authEl?.dataset.loginUrl;
const logoutUrl = authEl?.dataset.logoutUrl;
const isAuthenticated = authEl?.dataset.isAuthenticated === "True"; // convert to boolean
const userManagerMenu = document.getElementById("user-manager-menu-container");

let openOrClosed;
if (signInIcon) {
  signInIcon.addEventListener("click", () => {
    if (loginUrl && !isAuthenticated) {
      signInIcon.classList.add("logged-in");
      window.location.href = loginUrl;
    } else if (loginUrl && isAuthenticated) {
      openOrClosed = toggleManagerMenu();
    }
  });
}

window.addEventListener("click", (event) => {
  if (!userManagerMenu || !signInIcon) return;

  // Keep menu state when clicking the sign-in icon (or its child nodes)
  if (signInIcon.contains(event.target)) return;
  // If you also want clicks inside the menu to keep it open, add this before remove:
  // if (userManagerMenu.contains(event.target)) return;
  userManagerMenu.classList.remove("open");
});


function getOpenHeightPx(el) {
  const cs = getComputedStyle(el);
  const borderTop = parseFloat(cs.borderTopWidth) || 0;
  const borderBottom = parseFloat(cs.borderBottomWidth) || 0;
  return Math.ceil(el.scrollHeight + borderTop + borderBottom);
}

function toggleManagerMenu() {
  if (!userManagerMenu) {
    console.warn(
      "managerMenu not found: check .user-manager-menu-container exists on this page",
    );
    return;
  }
  userManagerMenu.classList.toggle("open");
  const isOpen = userManagerMenu.classList.contains("open");
  if (isOpen) {
    const openHeightPx = getOpenHeightPx(userManagerMenu);
    document.documentElement.style.setProperty(
      "--open-height",
      `${openHeightPx}px`,
    );
  }
  return isOpen ? "open" : "closed";
}

function logOut() {
  console.log("LOGGING OUT");
  signInIcon.classList.remove("logged-in"); // reverts to sign-in icon
  // log out link now handled directly from HTML <a> href link
  //   window.location.href = logoutUrl;
}
