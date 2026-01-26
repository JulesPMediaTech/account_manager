const opaqueDialogTemplate = document.createElement('template');

opaqueDialogTemplate.innerHTML = `
  <style>
    @import url('/static/components/opaque-dialog.css');
  </style>
  <dialog>
    <slot></slot>
  </dialog>
`;


class OpaqueDialog extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.appendChild(opaqueDialogTemplate.content.cloneNode(true));
    this._dialog = this.shadowRoot.querySelector('dialog');
  }

  connectedCallback() {
    // Close the dialog if the form inside it is submitted
    this.shadowRoot.querySelector('slot').addEventListener('submit', (e) => {
      if (e.target.tagName === 'FORM' && e.target.method === 'dialog') {
        e.preventDefault();
        this.close();
      }
    });
  }

      // Modal display dialog
  showModal() {
    this._dialog.showModal();
  }

    // non-modal display dialog
  show() {
    this._dialog.show();
  }

  close() {
    this._dialog.classList.add('closing');
    this._dialog.addEventListener('animationend', () => {
      this._dialog.classList.remove('closing');
      this._dialog.close();
    }, { once: true });
  }
}

window.customElements.define('opaque-dialog', OpaqueDialog);