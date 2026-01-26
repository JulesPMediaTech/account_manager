
class AccordionMenu extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  async connectedCallback() {
    // Fetch external CSS and inject it before rendering content
    const cssUrl = '/static/components/accordion-menu.css';
    let cssText = '';
    try {
      const response = await fetch(cssUrl);
      cssText = await response.text();
    } catch (e) {
      console.warn('AccordionMenu: Failed to load CSS:', e);
    }

    const style = document.createElement('style');
    style.textContent = cssText;

    // Create the accordion menu structure
    const wrapper = document.createElement('div');
    wrapper.className = 'accordion-menu';
    wrapper.setAttribute('part', 'container'); 
    wrapper.innerHTML = `
      <div class="label"><slot name="label">Menu</slot></div>
      <div class="content"><slot name="content"></slot></div>
    `;

    this.shadowRoot.appendChild(style);
    this.shadowRoot.appendChild(wrapper);

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