# Left side navigation drawer 

Build a collapsible side navigation drawer that opens and closes. 

This drawer will replace the current burger menu.
The drawer contains a column of link names and corresponding column of svg images.

When the drawer is open, it reveals both columns: the link names and the svg images.
When the drawer is closed, it shows a narrow column of svgs only.

### UI Appearence
Give an 'ease' animation to both open / close actions
The drawer background colour should match header and footer - currently black

The user can open and close the drawer by toggling the burger icon.
When closed, the icon dislays 3 horizontal bars.
When open, it displays 2 crossed bars.
USE THE CURRENT CSS ANIMATION FOR THIS FOUND IN: static/components/burger-menu.js

### Code structure
I don't want to create a shadowRoot element as burger-menu currently is.
Instead, create:
     html for the drawer in templates/partials
     css in static/css
     js in static/js

HOWEVER IT SHOULD BE EASY TO ADD LINKS (& corresponding svgs) TO THE DRAWER IN THE HTML FILE AT LATER STAGES OF DEVELOPMENT

### Tasks
1. Create the drawer container element and style as instructed.
2. Get the burger icon and its animation
3. Include the links
4. Create svg images. Put them in the static/images folder for now. HOWEVER Make it easy for me to add them to sprite_sheet.svg later.
5. The partial should be accessed by using {% include.. %} in the base.html file. Its css should be linked in base.html
6. Ask me anything you need clarity on.

### Answers to your Questions
1. correct, use left_sidenav_drawer.md
2. Create links: 'Home', 'Add User', 'Show Users', 'Test Admin Access', 'Change Password',  'User Preferences', 'Admin Settings'. The last 2 (prefs and settings) can be placeholders for now but include appropriate svgs.
3. Just add to base.html as I've already explained. I can exclude templates later.
4. Copy the animation from burger-menu.js. into new files. DON'T ALTER THE ORIGINAL FILE!.  If this can be done entirely using css without unneccessary js, then that is preferable.
5. create individual svg files now.
6. Yes, good question. The drawer should push content to the right when it opens.
7. for drawer width, choose sensible defaults. You can make CSS variables for tweaking if you think this will be clearer and cleaner.

### Report section
Use this section to tick off tasks and add comments.

- [x] 1. Created drawer container partial at `templates/partials/left_sidenav_drawer.html` and styled it in `static/css/left_sidenav_drawer.css`.
- [x] 2. Copied the burger bar animation behavior into the new drawer styles (3 bars closed, crossed bars open) without changing `static/components/burger-menu.js`.
- [x] 3. Added links in requested order: Home, Add User, Show Users, Test Admin Access, Change Password, User Preferences (placeholder), Admin Settings (placeholder).
- [x] 4. Added individual SVG files in `static/images` with `nav-*` naming to simplify migration into `sprite_sheet.svg` later.
- [x] 5. Wired partial include and CSS/JS links through `base.html`; drawer now replaces the old header burger menu and pushes content right when opened.
- [x] 6. Clarifications resolved before implementation; no additional blockers identified.

### First pass comments
- [x] I have altered left_sidenav_drawer so that headers and footers are NOT affected. 
- [x] Burger Icon needs to be back in its original position inside <div header-left> in header.html. 
- [x] svgs: AVOID using <img src>. Instead, use <svg use>
- [x] svgs are not visible on the page. Maybe they are black and not showing against the black background?
- [x] svg apply default colour var(--text-color)
- [x] Open / close state NEEDS TO BE PERSISTENT across page re-loads.
