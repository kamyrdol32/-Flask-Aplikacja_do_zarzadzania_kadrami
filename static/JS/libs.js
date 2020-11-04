function coll($type, $event){
  $event.preventDefault();

  $collapse = $("div.collapse[collapse='"+$type+"']").collapse('toggle');
}



$(document).ready(function(){
  $(".content-container").mouseover(function(){
    $("body").addClass("content-hovered");
  })

  $(".content-container").mouseleave(function(){
    $("body").removeClass("content-hovered");
  })


  $("select").select2({
    minimumResultsForSearch: -1,
  });

  $("#current_company").on("change", function(e){
    $val = $("#current_company").val();

    window.location = window.location.pathname+"?id="+$val;
  })

})
