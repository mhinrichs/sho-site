$(document).ready(function() {

  $('#timetable').on('click', '.clickable', function() {
  $.get("/shobiz/schedule/appointment/",
    {time: this.id},
    function(response) {
      window.location.href = "/shobiz/schedule/appointment/";
    },
    "html"
  );
  });

});
