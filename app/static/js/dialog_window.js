const dialogWindow = document.getElementById("js-dialog-main");
const dialogCancelButton = document.querySelector(".js-dialog-cancel-button");
const triggerDialog = document.getElementById("js-trigger-dialog");

if (dialogCancelButton) {
  dialogCancelButton.addEventListener("click", () => {
    dialogWindow.close();
  });
}

if (triggerDialog) {
  const dialogMessagePane = document.querySelector(".js-dialog-message-pane");
  const dialogMessage = triggerDialog.dataset.dialogMessage;
  if (dialogMessage) {
    dialogMessagePane.innerHTML = `
      <p>${dialogMessage}</p>
      `;
  }
  dialogWindow.showModal();
}

const dlgWarning = document.getElementById("js-dlg-warning-main");
const testWarningButton = document.getElementById("test-warning-button");
if (testWarningButton) {
  testWarningButton.addEventListener("click", () => {
    dlgWarning.showModal();
  });
}

const okButton = document.querySelector(".js-dlg-warning-ok-btn");
okButton.addEventListener("click", () => {
  dlgWarning.close();
});
