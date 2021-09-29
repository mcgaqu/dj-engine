=======
EMPRESA
=======

En este menú están los procesos de introducción de datos necesarios para
realizar los posteriores cálculos y obtención de informes.
Tiene especial importancia la primera opción: Empresa, que detallamos a
continuación.

1. Empresa.

	Algunos campos ya vienen rellenos de la instalación.
	Los campos código y nif no se pueden modificar porque identifican a la instalación.
	Los demás se pueden modificar y ompletar manualmente: att, teléfono, etc..
	
	Tiene especial interés el campo Fichero, en caso de que se quieran importar
	datos para poner en marcha la aplicación.
	El proceso de importación no es imprescindible, ya que todos los datos se pueden
	introducir mediante la interfaz del programa, pero pueden facilitar la puesta en
	marcha.
	
	El campo Fichero contiene un Libro de Excel con hojas preestablecidas para importar.
	No se puede cambiar el nombre de las hojas y se debe respetar el formato
	de las columnas de las mismas. Se pueden introducir tantas filas de datos
	como se desee. Estos son los nombres y formatos de las hojas del libro excel.

		* TARIFAS: En esta hoja se introducen los productos y servicios con sus precios de venta
		
		* VENTAS: Los importes de venta por periodos (según el tipo de periodo que se
		  indicará en la pestala de ejercicios activos)
		
		* FACTORES: Factores de cálculo. Ver modelo
		
		* T2010 - T2020: Cada una de las cuales hace referencia a un ejercicio.
		  Son los cobros diarios por tarjeta.
	
	La aplicación viene con un fichero base que se puede utilizar.
		NOTA: No se puede modificar directamente, es necesario:
		1) Descargarse el fichero
		2) Modificarlo en local, incluyendo nuestros datos
		3) Insertarlo otra vez en el campo Fichero de la ficha de empresa
	
	Ejercicios:
		1) Año
		2) Tipo de periodo en el que se introducen las ventas: Por defecto trimestre
		3) Patrón de numeración de facturas


	
Cuando se opte por importar datos, previamente especificados,
en la hoja de cálculo indicada anteriormente, será necesario realizar la/s acciones
de importación, que se ofrecen en la lista desplegable Accion: de la ficha de la Empresa.
	
	Nota: La acción Importar Fichero de Datos: Realiza las 4 opciones que se muestran
	debajo, por lo que si se realiza, no es necesario realizar las demás.
	

Acciones:

	1) COPIAS de Seguridad

	2)  GENERAR Ejercicio Activos.
		Realiza el proceso de cálculo y generación de informes en bloque,
		que consta de los siguientes pasos:
			
			* CREAR Ejerccios activos
			
			* Importar Fichero de datos
			
			* Calcular Ventas Diarias
			
			* Generar facturas
			
			* Ajustar cobros
			
	
	2) CREAR Ejercicios Activos:
	
		* crea un registro diario para prevision ventas calculadas
	
		* crea un registro por periodo de introduccion de datos de previsión de ventas
	
		* crea un registro diario para previsión de cobros
	
	
	3) IMPORTAR Fichero de datos.
	
		2.1 Importar Tarifas de Productos y Servicios
		
		2.2 Importar Ventas y Gastos
		
		2.3 Importar Cobros Tarjeta
		
		2.4 Importar Factores de Cálculo
		

	4) ELIMINAR Ejercicios Inactivos


 POBLACIONES.
 
 PERSONAS/CLIENTES
 
 TIPOS DE IVA
 
 PRODUCTOS/SERVICIOS
 
 FACTORES DE CALCULO
  
=======
EMPRESA
=======

Procedimientos de Trabajo:

a) PROCEDIMIENTO SIMPLIFICADO AUTOMATICO COMPLETO:

	I. Empresa:
	
		a) Introducción de datos de empresa, incluyendo:
			
			* el fichero de datos
		
			* los ejercicios activos
			
					
		b) Accion de GENERAR Ejercicios activos
		
		c) Acción: OBTENER informes.
		
		d) Copia seguridad
		
		e) Desactivar y ELIMINAR Ejercicios procesados


b) PROCEDIMIENTO PASO A PASO

	I. Empresa: 
	
		a) Introducción de datos descritos en este capítulo
		
		b) Acción de Crear de ejercicio(s) activo en curso
		
		c) Acción(es) de importación que proceda
		

	II. Ingresos: Introducción de datos
	
		a) Introducción de datos de previsión de ventas por periodo
			(si no se han importado)
	
		b) Introducción de datos de previsión de Cobros diarios
			(si no se han importado)


	III. Ingresos: Cálculos de Periodos
		OJO!! Para realizar esta operación correctamente es necesario
		que estén introducidos los datos de previsión de ventas y
		previsión de cobros. Si no se han obtenido mediante los procesos
		de importación, será necesario introducirlos manualmente,
		según se indica en el apartado II.

		
			1.- CALCULAR ventas. Acción en la pantalla Previsión de Ventas.
				Filtrar por Año o Trimestre
				1.1.- Reasignar peso-dia
				
				1.2.- Recalcular importes
				
				1.3.- Recalcular acumulados
			
			2.- GENERAR documentos
			
			3.- AJUSTAR ventas y cobros
			
			4.- Renumerar Facturas
			
			4.- COMPROBACION de Datos
		

	IV. Informes
	
		1.- Carpeta de Informes periodo

			a) Documentos			

			b) listados

