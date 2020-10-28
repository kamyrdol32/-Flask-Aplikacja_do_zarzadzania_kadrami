function findParentForm($element){
    if($element.tagName != "FORM"){
        $element =  findParentForm($element.parentElement);
    }

    return $element;
  }

  $(document).ready(function(){
    $forms = $("form");

    $($forms).each(function($i, $form){
      $($form).find('input[type="submit"], button[type="submit"]').on("click", function($e){
        $e.preventDefault();
        $form = findParentForm($e.target);
        console.log($form);

        $url = $($form).attr("action");
        $method = $($form).attr("method");
        $data = {};

        $($form).find("input, select").each(function($i, $input){
          $name = $($input).attr("id");
          $data[$name] = $($input).val();
        });


        $.ajax({
          url: $url,
          data: $data,
          type: $method,
        }).done(function(data){
          if(data['message']){
            // notify(data);
            console.log(data);
          } else if (data['redirect']) {
            window.location = data['redirect'];
          } else {
            console.log(data);
          }
        })

      })
    });

  });
