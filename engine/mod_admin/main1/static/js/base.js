(function($){ 
    $(document).ready(function(){
        console.log("Estoy en ready")       
        //------------------------------
        sincronizar_g5($);
  });

    function sincronizar_g5(){
        // alert("Estoy en sincronizar_g5")    
        $.ajax({
            type: 'GET',
            url: '/mk1cogesa/ajax/',
            data: {funcion:"mk1cogesa.carga_ini.actions.ajax_sincronizar_g5"},
            success: function(response){
                console.log(response);
            },
            error: function(xhr, status){alert("Ha ocurrido un error");},
            // complete: function(xhr, status){alert("Petición realizada");},

        });

    }
})(django.jQuery);
