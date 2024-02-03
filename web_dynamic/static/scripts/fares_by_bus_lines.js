$(document).ready(function() {
  $.get('http://127.0.0.1:5001/api/v1/routes', function(routes, status) {
    if (status === 'success') {
      count_urban_lines = 0;
      count_suburban_lines = 0;

      // Create tbody for urban and suburban tables
      let urbanTbody = $('<tbody></tbody>');
      let suburbanTbody = $('<tbody></tbody>');

      for (const route of routes) {
        
        // Create row for urban and suburban tables
        let row = $('<tr></tr>');
        // Set the innerHTML of the row
        row.html(`
          <th scope="row">${route.line_number}</th>
          <td>${route.departure_terminus}</td>
          <td>${route.arrival_terminus}</td>
          <td>${route.price}</td>
        `);
      
        // Append the row to the appropriate tbody
        if (route.urban === true) {
          urbanTbody.append(row);
          count_urban_lines++;
        } else {
          suburbanTbody.append(row);
          count_suburban_lines++;
        }
        
        
      }

      // Append the tbody to the tables
      $('table#urban').append(urbanTbody);
      $('table#suburban').append(suburbanTbody);
      
      // Update the number of lines
      $('div#number_of_urban_lines').text(`${count_urban_lines} line(s)`);
      $('div#number_of_suburban_lines').text(`${count_suburban_lines} line(s)`);

      // After populating tables
      $('table#urban').bootstrapTable();
      $('table#suburban').bootstrapTable();


      console.log(routes);
      
    } else {
      console.log(status);
    }
  });
});







$(document).ready(function() {
  $('a#urban_item').click(function(){
    
    $('div#row_2').attr('hidden', false);
    $('div#row_3').attr('hidden', true);
    $('button#dropdownMenuButton').text('Urban');
  });
  
  $('a#suburban_item').click(function(){
    
    $('div#row_2').attr('hidden', true);
    $('div#row_3').attr('hidden', false);
    $('button#dropdownMenuButton').text('Suburban');
  });
});









