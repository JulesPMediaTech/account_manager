const drawerRoot = document.body;
const toggle = document.getElementById("sidenav-toggle");
const storageKey = "left-sidenav-state";

if (drawerRoot && toggle) {
  const readStoredState = () => {
    try {
      return localStorage.getItem(storageKey);
    } catch {
      return null;
    }
  };

  const writeStoredState = (isOpen) => {
    try {
      localStorage.setItem(storageKey, isOpen ? "open" : "closed");
    } catch {
      // Ignore storage write failures (private mode, disabled storage, etc.).
    }
  };

  const applyState = (isOpen) => {
    drawerRoot.classList.toggle("drawer-open", isOpen);
  };

  const setExpandedState = () => {
    const expanded = drawerRoot.classList.contains("drawer-open");
    toggle.setAttribute("aria-expanded", expanded ? "true" : "false");
    toggle.setAttribute(
      "aria-label",
      expanded ? "Close navigation menu" : "Open navigation menu",
    );
  };

  const storedState = readStoredState();
  applyState(storedState === "open");
  setExpandedState();

  toggle.addEventListener("click", () => {
    const isOpen = !drawerRoot.classList.contains("drawer-open");
    applyState(isOpen);
    writeStoredState(isOpen);
    setExpandedState();
  });
}
