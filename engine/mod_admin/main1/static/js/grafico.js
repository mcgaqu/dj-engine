(function($){ $(document).ready(function(){
    // saludo();
    // grafico1();
    // grafico2();
    grafico3($);
    //------------------------------
    console.log("Estoy en ready")
    // $(xxx).addEventListener(evento, funcion, true/false);
    // $(xxx).removeEventListener(evento, funcion, true/false);
    // $("#id_cliente").on("change", ponerProyectos);
    /*----------------x------------

    ----------------------------------*/
  });
})(django.jQuery);


function crearVentana(){
    var url = "http://127.0.0.1:8022/prexCogesa/infodoc/graficoanexo/1/change/VERGRAFICO/grafo/"
   //  miVentana = window.open(url);
   // miVentana = window.open("", "", "width=500,height=200,top=500,left=500");
    miVentana = window.open(url, "_blank", "toolbar=yes,scrollbars=yes,resizable=yes,top=500,left=500,width=400,height=400");
    // miVentana.document.write("<h1>Mi ventana</h1>")
}

function cerrarVentana(){
    miVentana.close();
}


function saludo(){

    window.name = "Mi ventana";
    console.log(window.name);
    var texto = "";
    texto += "<br/>Nombre:" + window.name;    
    texto += "<br/>Ancho Externo:" + window.outerWidth;
    texto += "<br/>Alto Externo:" + window.outerHeight;
    texto += "<br/>Ancho Interno:" + window.innerWidth;
    texto += "<br/>Alto Interno:" + window.innerHeight;
    // alert(texto);
    console.log(texto);
    document.getElementById("ventana").innerHTML = texto;
    console.log(window.location)
}

function grafico1(){
    var datos1 = {
        type: "pie",
        data: {
            datasets: [{
                data: [10,20,30,15],
                backgroundColor: ["#F77", "#465", "#BF1","#F7A"]
            }],
            labels : ["Datos1", "Datos2", "Datos3", "Datos4"]
        },
        options: {
            responsive: true,
        }
    };
    
    var canvas1 = document.getElementById('chart1').getContext('2d');
    window.pie = new Chart(canvas1, datos1);    
}

function grafico2(){
    var datos2 = {
        labels: ["Enero", "Febrero","Marzo", "Abril"],
        datasets: [
            {label:"Datos1", data:[10, 20, 30, 40], backgroundColor:"rgb(0,255,0)"},
            {label:"Datos2", data:[40, 30, -20, 10], backgroundColor:"rgb(255,0,0)", hidden:true},
            {label:"Datos3", data:[45, 35, 25, 15], backgroundColor:"rgb(0,0,255)"}, 
        ]
    };
    var canvas2 = document.getElementById('chart2').getContext('2d');
    window.bar = new Chart(canvas2,{
        type: "bar",
        data: datos2,
        options: {
            elements: {
                rectangule: {
                    borderWidth: 1,
                    borderColor: "rgb(0, 255,0)",
                    borderSkipped: "button"
                }
            },
            responsive: true,
            title: {
                display: true,
                text: "Prueba de grafico de garras"
            } 
        }
    });
   
}

function grafico3($){
    var id = window.location.href.split('/')[6];
    $.ajax({
        type: 'get',
        url: '/prexCogesa/ajax/',
        // data: {funcion:"mod_admin1.infodoc.actions.ajax_grafico_ver", params:{grafico_id:id}},
        data: {funcion:"mod_admin1.infodoc.actions.ajax_grafico_ver", grafico_id:id},
        success: function(response){
            console.log(response);
            console.log(response.dev);
            var datos3 = {
                labels: ["Enero", "Febrero", "Marzo", "Abril"],
                datasets: [
                    {label:"Datos1", data: response.dev},
                    {label:"Datos2", data:[40, 30, 20, 10]},                    
                ]
            };
            // datos3 = dev
            //---------------------------------
            var canvas3 = document.getElementById('chart2').getContext('2d');
            window.bar = new Chart(canvas3, {
                type: "bar",
                data: datos3,
                options: {
                    elements: {
                        rectangule: {
                            borderWidth: 1,
                            borderColor: "rgb(0, 255,0)",
                            borderSkipped: "button"
                        }
                    },
                    responsive: true,
                    title: {
                        display: true,
                        text: "Prueba de grafico de garras"
                    } 
                }
            });
        },
        error: function(xhr, status){alert("Ha ocurrido un error");},
        complete: function(xhr, status){alert("Petición realizada");},
    });   
}
