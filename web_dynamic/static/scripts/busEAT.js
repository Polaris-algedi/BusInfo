$(document).ready(function() {
  populateDropdownMenu();

  $(document).on('click', '#dropdownMenu_stops .dropdown-item', function(event) {
    const clickedItem_stop = $(this).text();
    $('#search').data('stopName', clickedItem_stop);
    console.log('The stop name is: ', clickedItem_stop);
  });

  $(document).on('click', 'button#search', function(event) {
  
    event.preventDefault();
    const stops = $(this).data('stops');
    const stopName = $(this).data('stopName');
    const stopNumber = getStopNumber(stops, stopName);

    console.log('The stop number is: ', stopNumber);

  });
});

function populateDropdownMenu() {
  $.get('http://127.0.0.1:5001/api/v1/routes')
    .then(function(routes) {
      const { urbanList, suburbanList } = categorizeRoutes(routes);

      const dropdownMenu = $('div#dropdownMenu_lines');
      appendDropdownHeader(dropdownMenu, 'Urban', urbanList.length);
      appendDropdownItems(dropdownMenu, urbanList);
      appendDropdownHeader(dropdownMenu, 'Suburban', suburbanList.length);
      appendDropdownItems(dropdownMenu, suburbanList);

      
      $("#dropdownMenu_lines .dropdown-item").click(function(event) {
        const clickedItemText = $(this).text();

        console.log('The clicked item is: ', clickedItemText);
        const routeId = getRouteId(routes, clickedItemText);


        $.get(`http://127.0.0.1:5001/api/v1/routes/${routeId}/stops`)
          .then(function(stops) {
            const stopsList = getStopsList(stops);

            const dropdownMenu = $('div#dropdownMenu_stops');
            appendDropdownHeader(dropdownMenu, 'Stops', stopsList.length);
            appendDropdownItems(dropdownMenu, stopsList);
         
            // Store the stops in the button
            $('#search').data('stops', stops);
          })

          .catch(function(error) {
            console.log('Error fetching stops:', error);
          });
        
      });

    })
    .catch(function(error) {
      console.log('Error fetching routes:', error);
    });
}

function categorizeRoutes(routes) {
  let countUrbanLines = 0;
  let countSuburbanLines = 0;
  let urbanList = [];
  let suburbanList = [];

  for (const route of routes) {
    if (route.urban === true) {
      urbanList.push(route.line_number);
      countUrbanLines++;
    } else {
      suburbanList.push(route.line_number);
      countSuburbanLines++;
    }
  }

  urbanList.sort((a, b) => a - b);
  suburbanList.sort((a, b) => a - b);

  return { urbanList, suburbanList };
}

function appendDropdownHeader(dropdownMenu, category, count) {
  dropdownMenu.append(`<h6 class="dropdown-header">${category} ${count} line(s)</h6>`);
}

function appendDropdownItems(dropdownMenu, itemList) {
  itemList.forEach(element => {
    dropdownMenu.append(`<a class="dropdown-item" href="#">${element}</a>`);
  });
}

function getRouteId(routes, line_number) {
  for (const route of routes) {
    if (route.line_number === Number(line_number)) {
      return route.id;
    }
  }
}

function getStopsList(stops) {
  let stopsList = [];

  for (const stop of stops) {
    stopsList.push(stop.stop_name);
  }

  stopsList.sort();

  return stopsList;
}


function getStopNumber(stops, stop_name) {
  for (const stop of stops) {
    if (stop.stop_name === stop_name) {
      return stop.stop_number_in_route;
    }
  }
}
  
  

  
  
  
  
  
  
  
  