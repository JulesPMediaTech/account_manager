const dialogWindow = document.getElementById("js-dialog-main");
const dialogCancelButton = document.querySelector(".js-dialog-cancel-button");
const triggerDialog = document.getElementById("js-trigger-dialog");
const openDialogButton = document.querySelector(".js-open-dialog-button");



if (dialogCancelButton) {
  dialogCancelButton.addEventListener("click", () => {
    dialogWindow.close();
  });
}

if (openDialogButton) {
  openDialogButton.addEventListener("click", () => {
    openDialog(openDialogButton);
  });
}

if (triggerDialog) {
  openDialog(triggerDialog);
}

function openDialog(trigger) {
  const dialogMessagePane = document.querySelector(".js-dialog-message-pane");
  console.log(dialogMessagePane);
  const dialogMessage = trigger.dataset.dialogMessage;
  if (dialogMessage) {
    dialogMessagePane.innerHTML = `
      <p>${dialogMessage}</p>
      `;
  }
  dialogWindow.showModal();
}

// DIALOG WARNING PANE

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
