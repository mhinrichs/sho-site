$(document).ready(function() {
  $('#back').click(function() {
    $('#cal').html("");
    $.get("ajax/",
          {action: 1},
          function(response) {
            $('#cal').html(response);
          },
          "html"
         );
  });
});
