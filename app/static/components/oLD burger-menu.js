const burgerMenuTemplate = document.createElement('template');

burgerMenuTemplate.innerHTML = `
  <style>
    :host {
      display: block;
      font-family: sans-serif;
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
    /* Add animation styles for the burger icon transformation */
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
      position: absolute; /* Take the panel out of the document flow */
      z-index: 10; /* Ensure it appears on top of other content */
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.3s ease-out;

      /* Use the variable for background, with a fallback */
      background-color: var(--menu-bg-color, #744949);
      color: var(--text-color, black);

      border-radius: 4px;
      width: fit-content;
      /* Remove the border completely when closed */
      border: none; 
      box-shadow: 0 2px 4px rgba(237, 230, 230, 0.1); /* Optional: add a subtle shadow */
    }

      /* When the menu is open, add the full border */
      .menu-panel.open {
        border: 1px solid #ccc;
      }


    /* Style for the content passed into the slot */
    ::slotted(a) {
      color: var(--text-color, white);
      padding: 14px 25px;
      text-decoration: none;
      display: block;
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
    this.handleDocumentClick = this.handleDocumentClick.bind(this); // bind here!
    
  }
  connectedCallback() {
    const burgerIcon = this.shadowRoot.querySelector('.burger-icon');
    const menuPanel = this.shadowRoot.querySelector('.menu-panel');

    burgerIcon.addEventListener('click', (event) => {
      burgerIcon.classList.toggle('change');
      const isOpen = menuPanel.classList.contains('open');

      if (isOpen) {
        // If closing, reset maxHeight to trigger transition
        menuPanel.style.maxHeight = null;
        // Remove document listener when closing via icon
        document.removeEventListener('mousedown', this.handleDocumentClick);
        menuPanel.classList.remove('open');
      } else {
        menuPanel.classList.add('open');
        menuPanel.style.maxHeight = menuPanel.scrollHeight + "px";
        // Add document listener when opening
        setTimeout(() => {
          document.addEventListener('mousedown', this.handleDocumentClick);
        }, 0);
      }
    });

    // Listen for the transition to finish
    menuPanel.addEventListener('transitionend', () => {
      if (!menuPanel.style.maxHeight) {
        menuPanel.classList.remove('open');
      }
    });
  }

  
  handleDocumentClick(event) {
    // Use composedPath for a more reliable check with Shadow DOM
    if (!event.composedPath().includes(this)) {
      const burgerIcon = this.shadowRoot.querySelector('.burger-icon');
      const menuPanel = this.shadowRoot.querySelector('.menu-panel');
      // Close the menu
      burgerIcon.classList.remove('change');
      menuPanel.style.maxHeight = null;
      document.removeEventListener('mousedown', this.handleDocumentClick);
    }
  }
}



window.customElements.define('burger-menu', BurgerMenu);