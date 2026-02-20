const signInIcon = document.querySelector(".js-sign-in");
// const logoutBurgerItem = document.getElementById("a-logout");
const authEl = document.getElementById("js-auth");

const loginUrl = authEl?.dataset.loginUrl;
const logoutUrl = authEl?.dataset.logoutUrl;
const isAuthenticated = authEl?.dataset.isAuthenticated === "True"; // convert to boolean
const userManagerMenu = document.getElementById("user-manager-menu-container");
const openHeightPx = userManagerMenu?.scrollHeight ?? 0;
console.log(openHeightPx);

// logoutBurgerItem.addEventListener("click", () => {
//   logOut();
// });

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
    document.documentElement.style.setProperty(
      "--open-height",
      `${openHeightPx}px`,
    );
  }
  return isOpen ? "open" : "closed";
}

function logOut() {
  console.log("LOGGING OUT");
  signInIcon.classList.remove("logged-in");
  // log out link now handled directly from HTML <a> href link
  //   window.location.href = logoutUrl;
}
