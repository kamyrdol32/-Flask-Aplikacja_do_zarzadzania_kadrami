function coll($type, $event){
  $event.preventDefault();

  $collapse = $("div.collapse[collapse='"+$type+"']").collapse('toggle');
}

function resizeMessageBox(){
  $orig = $(".contact-list").height();
  $(".messages").height(($orig-100)+"px");
}

function sendMessage(){
  $id = window.location.href.split("/");
  $id = $id[$id.length-1];

  $.ajax({
    url: "/messages/"+$id,
    data: {'message': $("#message").val()},
    type: "POST",
  }).done(function(data){
    $d = new Date();
    $d = $d.getHours()+":"+$d.getMinutes()+":"+$d.getSeconds();
    if(data.sendMessage) addMessage($("#message").val(), "right", $d);
  }).fail(function($r){
    console.log($r.responseText);
  });
}

function addMessage($text = "", $side = "left", $date, $seen = 0){

  $html = "<div class='message "+($side == "left" ? "from" : "to")+"'>"+
                          "<div class='message-tile'>"+
                              "<span class='message'>"+$text+"</span>"+
                              "<span class='date'>Teraz</span>"+
                              "<p class='arrow'></p>"+
                          "</div>"+
                      "</div>";

  $(".messages").append($html);
  $height = 0;
  $(".messages > div").each(function(){$height += $(this).outerHeight();});
  $(".messages").stop().animate({scrollTop: $height+200}, 500, 'swing', function() {
  });

  if($side == "right") $("#message").val("");
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

  $height = 0;
  $(".messages > div").each(function(){$height += $(this).outerHeight();});
  $(".messages").scrollTop($height);

  $('.type-date').mask("0000-00-00");

  resizeMessageBox();
})


$(window).on("resize", function(){
  resizeMessageBox();
});
