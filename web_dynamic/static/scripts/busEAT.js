/**
 * Initializes the busEAT functionality.
 * Populates the dropdown menus with routes and stops.
 * Listens for click events on dropdown items and search button.
 * Retrieves schedule and calculates estimated arrival time.
 */
$(document).ready(function() {
  // Retrieve the routes from the API
  $.get('http://127.0.0.1:5001/api/v1/routes')
    .then(function(routes) {
      // Categorize the routes into urban and suburban lines
      const { urbanList, suburbanList } = categorizeRoutes(routes);


      // Pad the route numbers with leading zeros
      urbanList.forEach((element, index) => {
        urbanList[index] = element.toString().padStart(2, '0');
      });

      suburbanList.forEach((element, index) => {
        suburbanList[index] = element.toString().padStart(2, '0');
      });
      
      // Append the routes to the dropdown menu
      const dropdownMenu = $('div#dropdownMenu_lines');
      appendDropdownHeader(dropdownMenu, 'Urban', urbanList.length);
      appendDropdownItems(dropdownMenu, urbanList);
      appendDropdownHeader(dropdownMenu, 'Suburban', suburbanList.length, true);
      appendDropdownItems(dropdownMenu, suburbanList);
      
      // Store the routes in the button
      $('button#search').data('routes', routes);
      
      
    })
    .catch(function(error) {
      console.log('Error fetching routes:', error);
    });
  


  






























  // Listen for the click event on the dropdown items
  $(document).on('click', "#dropdownMenu_lines .dropdown-item", function(event) {
    const clickedItemText = $(this).text();

    console.log('The clicked item is: ', clickedItemText);
    const routes = $('button#search').data('routes');
    const route = getRoute(routes, clickedItemText);

    // Store the selected route in the button
    $('#search').data('route', route);


    $.get(`http://127.0.0.1:5001/api/v1/routes/${route.id}/stops`)
      .then(function(stops) {
        const stopsList = getStopsList(stops);

        const dropdownMenu = $('div#dropdownMenu_stops');
        dropdownMenu.empty();
        appendDropdownHeader(dropdownMenu, 'Stops', stopsList.length);
        appendDropdownItems(dropdownMenu, stopsList);
      
        // Store the stops in the button
        $('#search').data('stops', stops);
      })

      .catch(function(error) {
        console.log('Error fetching stops:', error);
      });
    
  });

  // Listen for the click event on the dropdown items 
  $(document).on('click', '#dropdownMenu_stops .dropdown-item', function(event) {
    // Store the stop name in the button
    const clickedItem_stop = $(this).text();
    $('#search').data('stopName', clickedItem_stop);
    console.log('The stop name is: ', clickedItem_stop);
  });

  // Listen for the click event on the search button
  $(document).on('click', 'button#search', function(event) {
  
    event.preventDefault();
    const stops = $(this).data('stops');
    const route = $(this).data('route');
    const stopName = $(this).data('stopName');
    const stopNumber = getStopNumber(stops, stopName);

    console.log('The stop number is: ', stopNumber);
    console.log('The schedule id is: ', route.schedule_id);
    $.get(`http://127.0.0.1:5001/api/v1/schedules/${route.schedule_id}`)
      .then(function(schedule) {
        console.log('stops length:', stops.length);
        estimated_time_between_stops = calculate_ETBS(schedule.duration, stops.length);
        console.log('Estimated time between stops:', estimated_time_between_stops);
        let estimated_arrival_time_list = bus_EAT(schedule.first_departure, schedule.last_departure, schedule.bus_frequency, estimated_time_between_stops, stopNumber);
        console.log('Estimated arrival time list:', estimated_arrival_time_list);

        
        
        const tableBody_1 = $('tbody#info_1');
        tableBody_1.empty();
        appendTableBody_1(tableBody_1, route, schedule);

        const tableBody_2 = $('tbody#info_2');
        tableBody_2.empty();
        appendTableBody_2(tableBody_2, route, schedule);
        
        
        const list_group = $('div#estimatedArrivalTimes');
        list_group.empty();
        list_header = `Estimated arrival times for ${stopName}`;
        appendList(list_group, list_header, estimated_arrival_time_list.map(estimated_arrival_time => estimated_arrival_time.toLocaleTimeString()));
      })
      
      .catch(function(error) {
        console.log('Error fetching stops:', error);
      });


  });



  // Show or hide the scroll-to-top button based on scroll position
  $(window).scroll(function () {
    if ($(this).scrollTop() > 100) {
        $('.scroll-to-top').fadeIn();
    } else {
        $('.scroll-to-top').fadeOut();
    }
  });

  // Scroll to top when the button is clicked
  $('.scroll-to-top a').click(function () {
      $('html, body').animate({ scrollTop: 0 }, 800);
      return false;
  });
});

/*function populateDropdownMenu() {
  
    const routes = $('button#search').data('routes');
  const route = getRoute(routes, 1);

  // Store the selected route in the button
  $('#search').data('route', route);


  $.get(`http://127.0.0.1:5001/api/v1/routes/${route.id}/stops`)
    .then(function(stops) {
      const stopsList = getStopsList(stops);

      $('#search').data('stopName', stopsList[0]);

      const dropdownMenu = $('div#dropdownMenu_stops');
      dropdownMenu.empty();
      appendDropdownHeader(dropdownMenu, 'Stops', stopsList.length);
      appendDropdownItems(dropdownMenu, stopsList);
    
      // Store the stops in the button
      $('#search').data('stops', stops);
    })

    .catch(function(error) {
      console.log('Error fetching stops:', error);
    });
  



  
  $.get(`http://127.0.0.1:5001/api/v1/schedules/${route.schedule_id}`)
  .then(function(schedule) {
    const stops = $('#search').data('stops');
    const stopName = $('#search').data('stopName');

    console.log('stops length:', stops.length);
    estimated_time_between_stops = calculate_ETBS(schedule.duration, stops.length);
    console.log('Estimated time between stops:', estimated_time_between_stops);
    let estimated_arrival_time_list = bus_EAT(schedule.first_departure, schedule.last_departure, schedule.bus_frequency, estimated_time_between_stops, 1);
    console.log('Estimated arrival time list:', estimated_arrival_time_list);

    
    
    const tableBody_1 = $('tbody#info_1');
    tableBody_1.empty();
    appendTableBody_1(tableBody_1, route, schedule);

    const tableBody_2 = $('tbody#info_2');
    tableBody_2.empty();
    appendTableBody_2(tableBody_2, route, schedule);
    
    
    const list_group = $('div#estimatedArrivalTimes');
    list_group.empty();
    list_header = `Estimated arrival times for ${stopName}`;
    appendList(list_group, list_header, estimated_arrival_time_list.map(estimated_arrival_time => estimated_arrival_time.toLocaleTimeString()));
  })
  
  .catch(function(error) {
    console.log('Error fetching stops:', error);
  });


}*/

/**
 * Categorizes the given routes into urban and suburban lines.
 * 
 * @param {Array<Object>} routes - The array of routes to categorize.
 * @returns {Object} - An object containing the urbanList and suburbanList arrays.
 */
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

/**
 * Appends a dropdown header to the given dropdown menu.
 * @param {jQuery} dropdownMenu - The dropdown menu to append the header to.
 * @param {string} category - The category of the header.
 * @param {number} count - The number of lines in the category.
 */
function appendDropdownHeader(dropdownMenu, category, count, dropdownMenu_divider = false) {
  if (dropdownMenu_divider) {
    dropdownMenu.append('<div class="dropdown-divider"></div>');
  }
  dropdownMenu.append(`<h6 class="dropdown-header">${category} ${count} line(s)</h6>`);
}

/**
 * Appends dropdown items to a dropdown menu.
 * 
 * @param {HTMLElement} dropdownMenu - The dropdown menu element.
 * @param {Array<string>} itemList - The list of items to append.
 */
function appendDropdownItems(dropdownMenu, itemList) {
  itemList.forEach(element => {
    dropdownMenu.append(`<a class="dropdown-item" href="#">${element}</a>`);
  });
}

function appendList(list_group, listHeader, itemList) {
  list_group.append(`<a href="#" class="list-group-item list-group-item-action active">${listHeader}</a>`);

  itemList.forEach(element => {
    list_group.append(`<a href="#" class="list-group-item list-group-item-action">${element}</a>`);
  });
  
}
/**
 * Retrieves a route object from an array of routes based on the line number.
 * @param {Array} routes - An array of route objects.
 * @param {number} line_number - The line number of the route to retrieve.
 * @returns {Object|undefined} - The route object matching the line number, or undefined if not found.
 */
function getRoute(routes, line_number) {
  for (const route of routes) {
    if (route.line_number === Number(line_number)) {
      return route;
    }
  }
}

/**
 * Returns a sorted list of stop names from the given stops array.
 * @param {Array} stops - The array of stops.
 * @returns {Array} - The sorted list of stop names.
 */
function getStopsList(stops) {
  let stopsList = [];

  for (const stop of stops) {
    stopsList.push(stop.stop_name);
  }

  stopsList.sort();

  return stopsList;
}


/**
 * Returns the stop number in route for a given stop name.
 * @param {Array} stops - The array of stops.
 * @param {string} stop_name - The name of the stop.
 * @returns {number|undefined} - The stop number in route, or undefined if not found.
 */
function getStopNumber(stops, stop_name) {
  for (const stop of stops) {
    if (stop.stop_name === stop_name) {
      return stop.stop_number_in_route;
    }
  }
}
  

/**
 * Calculates the estimated arrival times for a bus based on the given parameters.
 * 
 * @param {string} first_departure_time - The time of the first departure in the format 'HH:MM:SS'.
 * @param {string} last_departure_time - The time of the last departure in the format 'HH:MM:SS'.
 * @param {string} frequency_time - The frequency of the bus in the format 'HH:MM:SS'.
 * @param {number} estimated_time_between_stops - The estimated time in minutes between each bus stop.
 * @param {number} stop_number - The number of the bus stop.
 * @returns {Date[]} - An array of Date objects representing the estimated arrival times.
 */
function bus_EAT(first_departure_time, last_departure_time, frequency_time, estimated_time_between_stops, stop_number) {
  // Convert the first and last departure times to Date objects
  
  let first_departure = new Date(`1970-01-01T${first_departure_time}`);
  let last_departure = new Date(`1970-01-01T${last_departure_time}`);
  let frequency = new Date(`1970-01-01T${frequency_time}`);
  //console.log(frequency);
  frequency = frequency.getTime();
  let estimated_arrival_time = new Date(0);
/*   
  console.log('first departure', first_departure);
  console.log('last deparure', last_departure);
  console.log('frequency', frequency);
  console.log('estimated_arrival_time', estimated_arrival_time);
   */


  let estimated_time_between_stops_in_milliseconds = estimated_time_between_stops * 60000;
  estimated_arrival_time.setTime(first_departure.getTime() + (estimated_time_between_stops_in_milliseconds * (stop_number - 1)));
  
  

  let estimated_arrival_time_list = [];
  while (estimated_arrival_time.getTime() <= last_departure.getTime() + frequency) {
    //console.log('estimated_arrival_time', estimated_arrival_time);
    estimated_arrival_time_list.push(new Date(estimated_arrival_time));

    // Calculate the estimated_arrival_time
    estimated_arrival_time.setTime(estimated_arrival_time.getTime() + frequency);

  }
  return estimated_arrival_time_list;
}

/**
 * Calculates the average duration of a bus trip per stop.
 *
 * @param {string} duration - The total duration of the bus trip in the format 'HH:mm:ss'.
 * @param {number} stops - The number of stops in the bus trip.
 * @returns {number} - The average duration of the bus trip per stop in minutes.
 */
function calculate_ETBS(duration, stops) {
  
  let duration_in_minutes = new Date(`1970-01-01T${duration}`);
  duration_in_minutes = duration_in_minutes.getMinutes() + duration_in_minutes.getHours() * 60;
  /*
  Why stops - 1?
  The bus stops at the first stop and the last stop, so the average duration per stop is the total
  duration divided by the number of stops minus 1.
  Example:
  If the total duration is 60 minutes and there are 5 stops, the average duration per stop is:
  60 / (5 - 1) = 60 / 4 = 15 minutes.
  S5 - S4 - S3 - S2 - S1      S for stop
  60 - 45 - 30 - 15 - 00      time in minutes 
  */
  return duration_in_minutes / (stops - 1);
  
}

  
function appendTableBody_1(tableBody, route, schedule) {
  
  // Create row for table body
  let row = $('<tr></tr>');
  // Set the innerHTML of the row
  row.html(`
    <td scope="row">${route.departure_terminus}</td>
    <td scope="row">${schedule.duration}</td>
    <td scope="row">${route.arrival_terminus}</td>
    <td scope="row">${schedule.bus_frequency}</td>
  `);

  // Append the row to the appropriate tbody
  tableBody.append(row);

}

function appendTableBody_2(tableBody, route, schedule) {
  
  // Create row for table body
  let row = $('<tr></tr>');
  // Set the innerHTML of the row
  row.html(`
    <td scope="row">Line ${route.line_number}</td>
    <td scope="row">${schedule.first_departure}</td>
    <td scope="row">${schedule.last_departure}</td>
  `);

  // Append the row to the appropriate tbody
  tableBody.append(row);

}
  