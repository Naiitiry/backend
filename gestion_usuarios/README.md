<h1 align="center">Gestión de login de usuarios</h1>
> <p>
  En el siguiente Markdown les mostraré las pruebas realizadas a la API de registro y login de usuarios. La misma posee tanto la creación
  de usuarios nuevos, la modificación de datos de los mismos y la eliminación que en sí consta de pasar de "activo" a "inactivo", así la ID
  de los ya registrados como los nuevos no se ven alteradas por la eliminación de un registro.
</p>
<h2>Test</h2>
<p>
  <b>Aclaración</b>: las pruebas serán hechas en ThunderClient, desde VSCode, también lo hice con Postman pero por comodidad continuaré con el primero
  y la ejecución de la API lo realizo en el CMD de Windows directamente en vez de la consola del IDE.
</p>
<ol>
  <li>Ejecución del servicio.</li>
  <li>Primer GET para saber si conecta correctamente a la API.</li>
  <li>Completamos los datos para el registro del usuario.</li>
  <li>Luego ingresamos al endpoint de login</li>
  <li>Una vez dentro, podemos ver tanto nuestros datos como la de los demás usuarios.</li>
  <li>Unicamente podemos modificar nuestros datos y en caso de que seamos "admin" podemos modificar otros usuarios con el método PUT.</li>
  <li>Luego utilizamos otro GET para ver si efectivamente se realizó la actualización.</li>
</ol>
