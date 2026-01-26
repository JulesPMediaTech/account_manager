const accordionMenuTemplate = document.createElement('template');

accordionMenuTemplate.innerHTML = `
  <style> 
    :host {
      display: block;
      border: 1px solid #ccc;
      border-radius: 4px;
      overflow: hidden; /* Important for rounded corners */
    }
    .label {
      cursor: pointer;
      padding: 10px 15px;
      background-color: rgb(50, 49, 49);
      user-select: none; /* Prevents text selection on click */
    }
    .label:hover {
        background-color: var(--menu-hover-color, #ddd);
    }
    .content {
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.4s cubic-bezier(0.4, 0, 0.2, 1), padding 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      padding: 0 15px;
      background-color: var(--page-bg-color, #fff);
      will-change: max-height, padding;
    }
    .content.open {
      padding: 15px 15px;
      max-height: 500px;
    }
      </style>
  <div class="accordion-menu">
    <div class="label"><slot name="label">Menu</slot></div>
    <div class="content"><slot name="content"></slot></div>
  </div>

`;



class AccordionMenu extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.appendChild(accordionMenuTemplate.content.cloneNode(true));
  }

  connectedCallback() {
    const label = this.shadowRoot.querySelector('.label');
    const content = this.shadowRoot.querySelector('.content');

    // Only enable transitions after first frame
    requestAnimationFrame(() => {
      content.setAttribute('data-initialized', 'true');
    });

    label.addEventListener('click', () => {
      content.classList.toggle('open');
    });
  }
}

window.customElements.define('accordion-menu', AccordionMenu);