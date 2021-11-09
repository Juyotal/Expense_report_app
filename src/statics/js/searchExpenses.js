const searchField = document.querySelector('#searchField')
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table")
const paginationContainer = document.querySelector(".pagination-container");
const noResults = document.querySelector(".no-results")
const tbody = document.querySelector('.table-body')
const editbtn = document.querySelector('.edit')

console.log('yeah baby')

searchField.addEventListener('change', (e) => {
    const searchValue = e.target.value;
    tbody.innerHTML = ''
    if (searchValue.trim().length > 0){
        paginationContainer.style.display = "none"

        fetch("/search-expenses/", {
        body: JSON.stringify({ searchText: searchValue }),
        method: "POST",
        })
        .then((res) => res.json())
        // console.log(res)
        .then((data) => {
            console.log("data", data);
            appTable.style.display = "none";
            tableOutput.style.display = "block";

            console.log("data.length", data.length);

            if (data.length === 0) {
            noResults.style.display = "block";
            tableOutput.style.display = "none";
            } else {
            noResults.style.display = "none";
                data.forEach((item) => {
                    tbody.innerHTML += `
                        <tr>
                        <td>${item.amount}</td>
                        <td>${item.category}</td>
                        <td>${item.description}</td>
                        <td>${item.date}</td>
                        
                        </tr>`;
                });
            }
        })
    }else {
        appTable.style.display = "block";
        paginationContainer.style.display = "block";
    }    
})