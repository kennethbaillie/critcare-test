// Read the CSV file
function readCSV() {
    Papa.parse("reviewdates.csv", {
        download: true,
        header: true,
        complete: function(results) {
            createTable(results.data);
        }
    });
}

// Create the table with data
function createTable(data) {
    const tableBody = document.getElementById("table-body");
    
    data.forEach(row => {
        const tr = document.createElement("tr");
        
        Object.values(row).forEach(value => {
            const td = document.createElement("td");
            td.textContent = value;
            tr.appendChild(td);
        });
        
        tableBody.appendChild(tr);
    });
}

// Sort the table by column index
function sortTable(columnIndex) {
    const table = document.getElementById("review-dates-table");
    let switching = true;
    let shouldSwitch;
    
    while (switching) {
        switching = false;
        const rows = table.rows;
        
        for (let i = 1; i < rows.length - 1; i++) {
            shouldSwitch = false;
            const firstCell = rows[i].getElementsByTagName("TD")[columnIndex];
            const secondCell = rows[i + 1].getElementsByTagName("TD")[columnIndex];
            
            if (firstCell.innerHTML.toLowerCase() > secondCell.innerHTML.toLowerCase()) {
                shouldSwitch = true;
                break;
            }
        }
        
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }
}

// Initialize the table
readCSV();
