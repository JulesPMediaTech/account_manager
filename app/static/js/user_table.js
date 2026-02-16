const userTable = document.querySelector('.js-user-table');
const tbody = userTable.querySelector('tbody');
const editUrl = userTable.dataset.userEditUrl;

/* 
      Up: &#9650; &#x25B2; &nbsp;
      Down: &#9660; &#x25BC; &nbsp;
      Left: &#9664; &#x25C0; &nbsp;
      Right: &#9654; &#x25B6;
*/

const headers = userTable.querySelectorAll('thead th');
// let activeHeader = headers[0];  // first run - active header defaults to first column
// activeHeader.classList.add('sorted-by-column');
let activeHeader;
headers.forEach(header => {
    header.addEventListener('click', () => {
        const colIndex = header.cellIndex;
        const ascending = header.dataset.order !== 'asc'; //toggle
        header.dataset.order = ascending ? 'asc' : 'desc';

        const rows = Array.from(tbody.querySelectorAll('tr'));

        rows.sort((a,b) => {
            const aText = a.children[colIndex]?.textContent.trim() ?? '';
            const bText = b.children[colIndex]?.textContent.trim() ?? '';
            return ascending
                ? aText.localeCompare(bText, undefined, { numeric: true })
                : bText.localeCompare(aText, undefined, { numeric: true });
        });

        rows.forEach((r) => tbody.appendChild(r));
        console.log(`Sorted by header "${header.textContent.trim()}" (col ${colIndex})`);
        if (activeHeader) {
            activeHeader.classList.remove('sorted-by-column');
        };
        activeHeader = header;
        console.log(headers[0])
        activeHeader.classList.add('sorted-by-column');
        console.log(`Header ${activeHeader.textContent} has the class ${activeHeader.classList.value}`);
    });
});

const tableRows = tbody.querySelectorAll('tr');
tableRows.forEach(row => {
    row.addEventListener('click', () => {
        const userId = row.dataset.userId;
        if (userId) {
            document.getElementById('edit-user-id').value = userId;
            document.getElementById('edit-user-form').submit();
        }
    });
});


