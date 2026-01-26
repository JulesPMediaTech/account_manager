const burgerMenuTemplate = document.createElement('template');

burgerMenuTemplate.innerHTML = `
  <style>
    :host {
      display: block;
      font-family: sans-serif;
      position: relative;
    }
    .burger-icon {
      display: inline-block;
      cursor: pointer;
      padding: 10px;
    }
    .bar1, .bar2, .bar3 {
      width: 35px;
      height: 5px;
      background-color: var(--text-color, white);
      margin: 6px 0;
      transition: 0.4s;
    }
    .change .bar1 {
      transform: translate(0, 11px) rotate(-45deg);
    }
    .change .bar2 {
      opacity: 0;
    }
    .change .bar3 {
      transform: translate(0, -11px) rotate(45deg);
    }
    .menu-panel {
      position: absolute;
      z-index: 10;
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.3s ease-out;
      background-color: var(--menu-bg-color, #744949);
      color: var(--text-color, black);
      border-radius: 4px;
      width: fit-content;
      border: none; 
      box-shadow: 0 2px 4px rgba(237, 230, 230, 0.1);
    }
    .menu-panel.open {
      border: 1px solid #ccc;
    }
    ::slotted(a) {
      color: var(--text-color, white);
      padding: 14px 25px;
      text-decoration: none;
      display: block;
      /* Add a line below each menu item */
      border-bottom: 2px solid rgba(204, 204, 204, 0.47);
    }
    /* Remove the line from the last menu item */
    ::slotted(a:last-child) {
      border-bottom: none;
    }
    
    ::slotted(a:hover) {
      background-color: var(--menu-hover-color, #ddd);
    }
  </style>
  <div class="burger-icon">
    <div class="bar1"></div>
    <div class="bar2"></div>
    <div class="bar3"></div>
  </div>
  <div class="menu-panel">
    <slot></slot>
  </div>
`;

class BurgerMenu extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.appendChild(burgerMenuTemplate.content.cloneNode(true));
    this.handleDocumentClick = this.handleDocumentClick.bind(this);
  }

  connectedCallback() {
    const burgerIcon = this.shadowRoot.querySelector('.burger-icon');
    const menuPanel = this.shadowRoot.querySelector('.menu-panel');

    burgerIcon.addEventListener('click', () => this.toggleMenu());

    // Listen for clicks on the component itself to handle slotted links
    this.addEventListener('click', (e) => {
      const anchor = e.target.closest('a');
      if (anchor && this.shadowRoot.querySelector('.menu-panel.open')) {
        e.preventDefault();
        this.closeMenu();

        if (anchor.href !== window.location.href) {
          menuPanel.addEventListener('transitionend', () => {
            window.location.href = anchor.href;
          }, { once: true });
        }
      }
    });

    // Add a single, permanent listener to remove the 'open' class after closing
    menuPanel.addEventListener('transitionend', () => {
      if (!menuPanel.style.maxHeight) {
        menuPanel.classList.remove('open');
      }
    });
  }

  toggleMenu() {
    const menuPanel = this.shadowRoot.querySelector('.menu-panel');
    if (menuPanel.classList.contains('open')) {
      this.closeMenu();
    } else {
      this.openMenu();
    }
  }

  openMenu() {
    const burgerIcon = this.shadowRoot.querySelector('.burger-icon');
    const menuPanel = this.shadowRoot.querySelector('.menu-panel');
    burgerIcon.classList.add('change');
    menuPanel.classList.add('open');
    menuPanel.style.maxHeight = menuPanel.scrollHeight + "px";
    setTimeout(() => document.addEventListener('mousedown', this.handleDocumentClick), 0);
  }

  closeMenu() {
    const burgerIcon = this.shadowRoot.querySelector('.burger-icon');
    const menuPanel = this.shadowRoot.querySelector('.menu-panel');
    burgerIcon.classList.remove('change');
    menuPanel.style.maxHeight = null; // This triggers the closing animation
    document.removeEventListener('mousedown', this.handleDocumentClick);
  }

  handleDocumentClick(event) {
    if (!event.composedPath().includes(this)) {
      this.closeMenu();
    }
  }
}

window.customElements.define('burger-menu', BurgerMenu);