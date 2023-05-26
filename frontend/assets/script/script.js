//HTML ELEMENTS
//Header
var proceure_text = document.getElementById('procedure_text')
//Search
var searchBox = document.getElementById('search-box')
var searchButton = document.getElementById('search-button')
//Select
var selectedMainTitle = document.getElementById('selected_main_title')
var selectedTitle = document.getElementById('selected-title')
var suggestionshButton = document.getElementById('suggestions-button')
var imdbButton = document.getElementById('imdb-button')
//Suggestion elements
var suggestionWindow = document.getElementById('suggestions_table_container_border')
//Table
var tableMainTitle = document.getElementById('suggestions_title')
var tableBody = document.querySelector('#suggestions_table tbody')
var table = document.getElementById('suggestions_table')
//VARIABLES
var faze = 0
var title_id = ''
//MODAL
var imdbButton = document.getElementById('imdb-button')
var modal = document.getElementById('imdb_info')
var span = document.getElementsByClassName('imdb_info-close')[0]
var watchTrailer = document.getElementById('watch_trailer')

modal.style.display = 'none'

window.onload = function () {
  faze = 0
  clearFields()
  suggestionWindow.hidden = true
}

function clearFields() {
  tableMainTitle.textContent = ''
}

//SEARCH ELEMENT
searchButton.addEventListener('click', function () {
  var searchText = searchBox.value

  if (searchText) {
    suggestionWindow.hidden = false
    proceure_text.innerHTML = 'Double click to select title from the list'
    faze = 1
    searchBox.value = ''
    selectedTitle.innerHTML = ''
    searchTitles(searchText)
    title_id = ''
    tableMainTitle.textContent = 'SELECT TITLE'
  }
})

//Search data - populate table
function searchTitles(data) {
  let json = JSON.stringify(data)

  if (!json) {
  } else {
    fetch('http://127.0.0.1:5000/search_title', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: json,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Request failed')
        }
        return response.json()
      })
      .then((data) => {
        let show_edit_data = JSON.parse(JSON.stringify(data)).slice(0, 14)
        populateTableWithSearch(table, show_edit_data)
      })
      .catch((error) => {
        console.error(error)
      })
  }
}

function populateTableWithSearch(table, data) {
  // Clears table
  for (var i = 0; i < table.rows.length; i++) {
    var row = table.rows[i]
    for (var j = 0; j < row.cells.length; j++) {
      row.cells[j].innerHTML = ''
      row.cells[j].classList.remove('has-value')
    }
  }

  // Adds data to the table
  for (var i = 0; i < data.length; i++) {
    var row = table.rows[i]
    var col1 = row.cells[0]
    var col2 = row.cells[1]
    var col3 = row.cells[2]
    col1.innerHTML = data[i][1] + ' (' + data[i][2] + ')'
    col2.innerHTML = '[' + data[i][3].toFixed(1) + ']'
    col3.innerHTML = data[i][0]

    if (data[i][0] || data[i][1]) {
      row.cells[0].classList.add('has-value')
      row.cells[1].classList.add('has-value')
    }
  }
}

//SUGGESTIONS
suggestionshButton.addEventListener('click', function () {
  if (selectedTitle && faze == 1) {
    proceure_text.innerHTML =
      'Double click a title from the table for more suggestions or IMDB info.'
    tableMainTitle.textContent = 'TITLE SUGGESTIONS'
    titleSuggestions(title_id)
  }
})

function titleSuggestions(data) {
  let json = JSON.stringify(data)

  if (!json) {
  } else {
    fetch('http://127.0.0.1:5000/title_suggestions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: json,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Request failed')
        }
        return response.json()
      })
      .then((data) => {
        let show_edit_data = JSON.parse(JSON.stringify(data)).slice(0, 14)
        populateTableWithSuggestions(table, show_edit_data)
      })
      .catch((error) => {
        console.error(error)
      })
  }
}

function populateTableWithSuggestions(table, data) {
  // Clears table
  for (var i = 0; i < table.rows.length; i++) {
    var row = table.rows[i]
    for (var j = 0; j < row.cells.length; j++) {
      row.cells[j].innerHTML = ''
      row.cells[j].classList.remove('has-value')
    }
  }
  // Adds data to the table
  for (var i = 0; i < data.length; i++) {
    var row = table.rows[i]
    var col1 = row.cells[0]
    var col2 = row.cells[1]
    var col3 = row.cells[2]
    var arrayData = JSON.parse(data[i][4])
    col1.innerHTML = data[i][1] + ' (' + data[i][2] + ')'
    col2.innerHTML = '[' + arrayData[0].toFixed(1) + ']'
    col3.innerHTML = data[i][0]

    if (data[i][0] || data[i][1]) {
      row.cells[0].classList.add('has-value')
      row.cells[1].classList.add('has-value')
    }
  }
}
//

//TABLE DOUBLE CLICK
function handleRowDoubleClick(event) {
  var row = event.target.parentNode
  var rowData = []

  // Get the content of each cell in the row
  for (var i = 0; i < row.cells.length; i++) {
    rowData.push(row.cells[i].textContent)
    proceure_text.innerHTML =
      'Click on a suggestion button for title suggestions'
  }

  // Alert the row content
  selectedTitle.innerHTML = rowData[0]
  title_id = rowData[2]
}

// Attach event listener to table rows
var tableRows = document.querySelectorAll('#suggestions_table tbody tr')
tableRows.forEach(function (row) {
  row.addEventListener('dblclick', handleRowDoubleClick)
})

//MODAL
//Opening modal
let modalName
let modalfactor1
let modalfactor2
let modaltotal

//IMDB data modal
imdbButton.addEventListener('click', function () {
  if (selectedTitle.innerHTML) {
    IMDBdata(title_id)
  }
})

function IMDBdata(data) {
  let json = JSON.stringify(data)
  if (!json) {
  } else {
    fetch('http://127.0.0.1:5000/imdb_data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: json,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Request failed')
        }
        return response.json()
      })
      .then((data) => {
        let show_edit_data = JSON.parse(JSON.stringify(data))
        openModal(show_edit_data)
      })
      .catch((error) => {
        console.error(error)
      })
  }
}

//Two function that close modal, x and outside of modal click
span.onclick = function () {
  modal.style.display = 'none'
}

window.addEventListener('click', function (event) {
  if (event.target === modal) {
    modal.style.display = 'none'
  }
})

function openModal(data) {
  var modalTitlelement = document.getElementById('imdb_info-title')
  var modalPlotElement = document.getElementById('imdb_info-plot')
  var modalDirectorElement = document.getElementById('imdb_info-director')
  var modalActorsElement = document.getElementById('imdb_info-actors')
  var modalGenreElement = document.getElementById('imdb_info-genre')
  var modaRatingElement = document.getElementById('imdb_info-rating')
  var modalCoverElement = document.getElementById('imdb_info-cover')

  modalTitlelement.innerHTML =
    data['title'] + (data['year'] ? ' (' + data['year'] + ')' : '')
  modalPlotElement.innerHTML = data['synopsis']
  modalDirectorElement.innerHTML = data['director']
  modalActorsElement.innerHTML = data['actors']
  modalGenreElement.innerHTML = data['genre']
  modaRatingElement.innerHTML = data['ratings']
  trailer_url = data['trailer']
  modalCoverElement.innerHTML =
    '<img src="' + data['image'] + '" style="max-width: 50%; max-height: 50%;">'

  modal.style.display = 'block'
  if (trailer_url === null) {
    watchTrailer.disabled = true
  } else {
    watchTrailer.disabled = false
  }
}

var trailer_url = ''

watchTrailer.addEventListener('click', function () {
  window.open(trailer_url, 'Trailer Popup')
})
