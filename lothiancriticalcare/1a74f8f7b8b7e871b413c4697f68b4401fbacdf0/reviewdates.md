---
title: guidelines access system
layout: page
---

### Guideline review dates

Download an excel version of this table: [reviewdates.xlsx](reviewdates.xlsx)

Click on column headers below to sort the table.

<div id="tableContainer"></div>


<style>
    table {
        border-collapse: collapse;
        width: 100%;
        max-width:1200px;
        margin:1em;
    }
    th, td {
        border: 1px solid black;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #f2f2f2;
        cursor: pointer;
    }
    .highlight {
        background-color: #fdd;
    }
</style>

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

<script>
    $(document).ready(function() {
        $.ajax({
            url: "reviewdates.csv",
            dataType: "text",
            success: function(data) {
                createTable(data);
            }
        });
    });

    function createTable(csv) {
        let lines = csv.split("\n");
        let table = $('<table></table>');
        let today = new Date();
        today.setHours(0, 0, 0, 0);

        lines.forEach((line, index) => {
            let row = $('<tr></tr>');
            let cells = line.split(",");
            cells.forEach((cell, cellIndex) => {
                let cellElement = (index === 0) ? $('<th></th>') : $('<td></td>');
                cellElement.text(cell);

                if (index !== 0 && cellIndex === 1) { 
                    let date = new Date(cell);
                    if (date < today) {
                        row.addClass('highlight');
                    }
                }

                row.append(cellElement);
            });
            table.append(row);
        });

        //$("body").append(table);
        $("#tableContainer").append(table);
        sortTableOnClick();
    }

    function sortTableOnClick() {
        $('th').click(function() {
            let table = $(this).parents('table');
            let rows = table.find('tr:gt(0)').toArray().sort(comparer($(this).index()));
            this.asc = !this.asc;
            if (!this.asc) {
                rows = rows.reverse();
            }
            table.append(rows);
        });
    }

    function comparer(index) {
        return function(a, b) {
            let valA = getCellValue(a, index);
            let valB = getCellValue(b, index);
            return $.isNumeric(valA) && $.isNumeric(valB) ? valA - valB : valA.toString().localeCompare(valB);
        }
    }

    function getCellValue(row, index) {
        return $(row).children('td').eq(index).text();
    }
</script>

