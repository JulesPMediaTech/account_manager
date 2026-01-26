const accordionMenuTemplate = document.createElement('template');

accordionMenuTemplate.innerHTML = `
  <style>
    @import url('/static/components/accordion-menu.css');
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