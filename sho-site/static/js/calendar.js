// My calendar ajax function
function to_calendar_ajax(action_string) {
  $('#cal').html('<center><img src="/static/loading.gif"></center>');
  $.get("ajax/",
    {action: action_string},
    function(response) {
      window.setTimeout(function() {
      $('#cal').html(response);
      },1000);
    },
    "html"
  );
};

// DOM event handlers

$(document).ready(function() {

  $('#back').click(function() {
    to_calendar_ajax('back');
  });

  $('#current').click(function() {
    to_calendar_ajax('current');
  });

  $('#next').click(function() {
    to_calendar_ajax('forward');
  });

  $('#cal').on('click', '.clickable', function() {
  $.post("/shobiz/calendar/",
    {date: this.id},
    function(response) {
      var json = JSON.parse(response);
      if (json.result = 'success') {
      window.location.href = "/shobiz/schedule/";
      } else {
      window.location.href = "/shobiz/calendar/";
      };
    },
    "html"
  );
  });


});








