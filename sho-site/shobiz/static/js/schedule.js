$(document).ready(function() {

  $('#timetable').on('click', '.clickable', function() {
  $.post("/shobiz/schedule/",
    {time: this.id},
    function(response) {
      var json = JSON.parse(response)
      if (json.result == 'success') {
        window.location.href = "/shobiz/appointment/";
      } else {
        window.location.href = "/shobiz/calendar/";
      };
    },
    "html"
  );
  });

});
