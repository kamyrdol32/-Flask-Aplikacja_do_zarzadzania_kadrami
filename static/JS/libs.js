function coll($type, $event){
  $event.preventDefault();

  $collapse = $("div.collapse[collapse='"+$type+"']").collapse('toggle');
}

function resizeMessageBox(){
  $orig = $(".contact-list").height();
  $(".messages").height(($orig-100)+"px");
}

function sendMessage(){
  $.ajax({
    url: "/messages",
    data: {'message': $("#message").val()},
    type: "POST",
  }).done(function(data){
    if(data['message']){
      notify(data);
      console.log(data);
    } else {
      console.log(data);
    }
  }).fail(function($r){
    console.log($r.responseText);
  });
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

  $("#current_company.details").on("change", function(e){
    $val = $("#current_company").val();
    window.location = "/company/list/"+$val;
  })

  $("#current_company.workers").on("change", function(e){
    $val = $("#current_company").val();
    window.location = "/company/workers/"+$val;
  })

  $(".contact-tile").on("click", function(e){
    $e = $(e.target);
    $id = $e.attr("user-id");
    window.location = "/messages/"+$id;
  });

  resizeMessageBox();
})


$(window).on("resize", function(){
  resizeMessageBox();
});
