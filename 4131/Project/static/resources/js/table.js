function updateTable() {
    var table = document.getElementById("projectTable");
    var now = new Date();

    for (var i = 1; i < table.rows.length; i++) {
        var deadlineText = table.rows[i].cells[3].innerText;
        if (deadlineText === "Overdue") {
            continue;
        }
        var deadline = new Date(table.rows[i].cells[3].innerText);
        var timeDifference = deadline.getTime() - now.getTime();

        if (timeDifference < 0) {
            table.rows[i].cells[3].innerHTML = "Overdue";
            
        } else {
            var seconds = Math.floor(timeDifference / 1000);
            var minutes = Math.floor(seconds / 60);
            var hours = Math.floor(minutes / 60);
            var days = Math.floor(hours / 24);

            table.rows[i].cells[3].innerHTML = days + " days " + hours % 24 + " hours " + minutes % 60 + " minutes " + seconds % 60 + " seconds";
            
        }
    }
}
setInterval(updateTable, 1000);



function statusColor() {
    const statusChanger = document.querySelectorAll(".statusChanger");
    
    statusChanger.forEach(button => {
        button.addEventListener("click", function () {
            const projectId = button.getAttribute("dataProjectId");
            const currentStatus = button.getAttribute("dataStatus");
            const newStatus = currentStatus === "Done" ? "Not Done" : "Done"; 
            const statusData = { project_id: projectId, status: newStatus };

            fetch("/api/update_status", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(statusData)
            })
            .then(response => {
                if (response.status === 204) {
                    button.innerText = newStatus;
                    button.setAttribute("dataStatus", newStatus);
                    updateStatusColor(button, newStatus);
                } else if (response.status === 400) {
                    alert("Listing not found.");
                } else {
                    alert("An error occurred. Status wasn't updated.");
                }
            })
            .catch(error => {
                console.error("Error updating status:", error);
                alert("Network error. Please try again later.");
            });
        });
    });

    statusChanger.forEach(button => {
        const status = button.getAttribute("dataStatus");
        updateStatusColor(button, status);
    });
}

function updateStatusColor(button, status) {
    if (status === "Done") {
        button.style.backgroundColor = "green";
    } else if (status === "Not Done") {
        button.style.backgroundColor = "red";
    } else {
        button.style.backgroundColor = "";
    }
}
statusColor();




const deleteButtons = document.querySelectorAll(".deleteBtn");
deleteButtons.forEach(button => {
    
    button.addEventListener("click", function() {
        var projectId = button.getAttribute("dataProjectId");
        var deleteData = { project_id: projectId };
        fetch("/api/delete_project", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(deleteData)
        })
        .then(response => {
            if (response.status === 204) {
                var row = button.closest('tr');
                row.remove();
                updateTable();  
            } else if (response.status === 400) {
                alert("Listing not found.");
            } else {
                alert("An error occurred. Listing wasn't deleted.");
            }
        })
        .catch(error => {
            console.error("Error deleting listing:", error);
            alert("Network error. Please try again later.");
        });
    });
});

document.querySelector('.search-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from reloading the page
    searchFilter();
});

function searchFilter() {
    const searchBar = document.getElementById('searchBar').value.toLowerCase();
    const categoryFilter = document.getElementById('dropDown').value;
    const overDue = document.getElementById('overDue').value;
    const tableRows = document.querySelectorAll('#tableData tr');

    tableRows.forEach(row => {
        const titleCell = row.querySelector('td:first-child a');
        const categoryCell = row.querySelector('td:nth-child(3)');
        if (titleCell && categoryCell) {
            const title = titleCell.textContent.toLowerCase();
            const category = categoryCell.textContent.toLowerCase();
            const matchesSearch = searchBar === "" || title.includes(searchBar);
            const pastProject = row.querySelector('td:nth-child(4)').textContent === "Overdue";
            const matchesCategory = categoryFilter === "All" || category === categoryFilter.toLowerCase();

            if (matchesSearch && matchesCategory) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
            
            if (overDue === "true" && !pastProject) {
                row.style.display = 'none';
            }
        }
    });
}


document.getElementById('dropDownStatus').addEventListener('change', statusfilter);
function statusfilter() { 
    const statusFilter = document.getElementById('dropDownStatus').value;
    const tableRows = document.querySelectorAll('#tableData tr');
    
    tableRows.forEach(row => {
        const statusCell = row.querySelector('td:nth-child(2)');
        if (statusCell) {
            const status = statusCell.textContent;
            const matchesStatus = statusFilter === "All" || status === statusFilter;
            
            if (matchesStatus) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        }
    });
}


document.getElementById('dropDownOverDue').addEventListener('change', deadlinefilter);
function deadlinefilter() { 
    const statusFilter = document.getElementById('dropDownOverDue').value;
    const tableRows = document.querySelectorAll('#tableData tr');
    
    tableRows.forEach(row => {
        const statusCell = row.querySelector('td:nth-child(4)');
        if (statusCell) {
            const status = statusCell.textContent;
            const matchesStatus = statusFilter === "All" || status === statusFilter;
            
            if (matchesStatus) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        }
    });
}
