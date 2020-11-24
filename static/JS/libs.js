//
// function coll($type, $event){
//   $event.preventDefault();
//
//   $collapse = $("div.collapse[collapse='"+$type+"']").collapse('toggle');
// }

// Wysłąnie wiadomości prywatnej
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

// Dodanie wiadomości bez odświezania strony (AJAX)
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

  // Wyłączenie wyszukiwarki w Select'ach
  $("select").select2({
    minimumResultsForSearch: -1,
  });

  // Przekierowanie na odpowiedni adres po wybraniu firmy
  $("#current_company.details").on("change", function(e){
    $val = $("#current_company").val();
    window.location = "/company/list/"+$val;
  })

  // Przekierowanie na odpowiedni adres po wybraniu firmy
  $("#current_company.workers").on("change", function(e){
    $val = $("#current_company").val();
    window.location = "/company/workers/"+$val;
  })

  // Przekierowanie na odpowiedni adres po wybraniu firmy
  $("#current_company.vacations").on("change", function(e){
    $val = $("#current_company").val();
    window.location = "/company/vacation/"+$val;
  })

  // Przekierowanie na odpowiedni adres po nadawcy/adresata
  $(".contact-tile").on("click", function(Message){
    $e = $(Message.target);
    $id = $Message.attr("user-id");
    window.location = "/messages/"+$id;
  });

  // Maska dotycząca daty
  $('.type-date').mask("0000-00-00");

  // Maska dotycząca NR Telefonu
  $('.type-phone-number').mask("000000000");

  // Maska dotycząca kodu pocztowego
  $('.type-zip').mask("00-000");

  // Scrollowanie do aktualnej wiadomośći PW
  $height = 0;
  $(".messages > div").each(function(){$height += $(this).outerHeight();});
  $(".messages").scrollTop($height);


  // Zmiana wysokości MessageBox'a po załądowaniu strony
  resizeMessageBox();
})




  // Zmiana wysokości MessageBox'a
function resizeMessageBox(){
  $orig = $(".contact-list").height();
  $(".messages").height(($orig-100)+"px");
}

  // Zmiana wysokości MessageBox'a kiedy rozmiar okna ulegnie zmianie
$(window).on("resize", function(){
  resizeMessageBox();
});


function editModal($id, $firma){
  $($("#modal-edit input[type='hidden']")[1]).val($id);
  $($("#modal-edit input[type='hidden']")[2]).val($firma);
  $("#modal-edit").modal();
}
