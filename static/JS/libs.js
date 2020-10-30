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

})
