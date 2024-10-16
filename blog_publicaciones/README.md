<h1 align="center">Blog</h1>
<p>Este proyecto es una continuación de los 2 anteriores, una integración de todolist y gestion de usuarios.<br>

El objetivo de esta API es poder registrar usuarios, tanto administradores (con sus permisos excepcionales) como usuarios regulares, los cuales tendran restricciones en algunos sectores de la API. Se podrá crear publicaciones, comentar las mismas, crear categorías (unicamente con los admins)
</p>

## Test

> Aclaración: las pruebas serán hechas en ThunderClient, desde VSCode, también lo hice con Postman pero por comodidad continuaré con el primero y la ejecución de la API lo realizo en el CMD de Windows directamente en vez de la consola del IDE.<br> Las capturas de la misma serán almacenadas en el propio repositorio.
<ol>
  <li>Ejecución del servicio.</li>
  <img src="./img/Captura00.PNG"><br><br>
  <li>Primer GET para saber si conecta correctamente a la API.</li><br>
  <li>Completamos los datos para el registro del usuario.</li><br>
  <img src="./img/Captura1.PNG">
  <li>Luego ingresamos al endpoint de login</li><br>
  <img src="./img/Captura2.PNG"><br><br>
  <li>Una vez dentro, podemos ver tanto nuestros datos como la de los demás usuarios.</li><br>
  <img src="./img/Captura3.PNG"><br><br>
  <li>Unicamente podemos modificar nuestros datos y en caso de que seamos "admin" podemos modificar otros usuarios con el método PUT. En este caso pusimos el nombre y apellido con la primer letra en mayúsculas.</li><br>
  <img src="./img/Captura4.PNG"><br><br>
  <li>Luego utilizamos otro GET para ver si efectivamente se realizó la actualización.</li><br>
  <img src="./img/Captura5.PNG">
  
</ol>

## Glosario

<table>
  <thead>
    <th>Endpoint</th>
    <th>¿Qué hace?</th>
  </thead>
  <tbody>
    <tr>
      <td>127.0.0.1:5000/</td>
      <td>Muetra un texto simple para saber que se conecta correctamente con un GET.
      </td>
    </tr>
    <tr>
      <td>/api/register</td>
      <td>Permite registrar a un usuario nuevo a través del método POST.</td>
    </tr>
    <tr>
      <td>/api/login</td>
      <td>Poder hacer login con el método POST</td>
    </tr>
    <tr>
      <td>
        /api/fetch/&lt;int:id_user&gt
      </td>
      <td>Una vez logeado permite ver a cualquier usuario indicando el número de ID</td>
    </tr>
        </tr>
        <tr>
      <td>/api/fetch/edit/&lt;int:id_user&gt;</td>
      <td>Permite editar al usuarios, siempre y cuando quien edite sea el propio usuario o tenga el rol de "admin", a traves del método 'PUT'</td>
    </tr>
        </tr>
    <tr>
      <td>/api/fetch/edit_status/&lt;int:id_user&gt;</td>
      <td>Permite cambiar el status al usuario seleccionado, hay 3 opciones, "activo", "inactivo" y "bloqueado".</td>
    </tr>
  </tbody>
</table>