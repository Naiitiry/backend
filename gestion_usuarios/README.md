<h1 align="center">Gestión de login de usuarios</h1>
<p>
  En el siguiente Markdown les mostraré las pruebas realizadas a la API de registro y login de usuarios. La misma posee tanto la creación
  de usuarios nuevos, la modificación de datos de los mismos y la eliminación que en sí consta de pasar de "activo" a "inactivo", así la ID
  de los ya registrados como los nuevos no se ven alteradas por la eliminación de un registro.
</p>

## Test

> Aclaración: las pruebas serán hechas en ThunderClient, desde VSCode, también lo hice con Postman pero por comodidad continuaré con el primero y la ejecución de la API lo realizo en el CMD de Windows directamente en vez de la consola del IDE.
<ol>
  <li>Ejecución del servicio.</li>
  <li>Primer GET para saber si conecta correctamente a la API.</li>
  <li>Completamos los datos para el registro del usuario.</li>
  <li>Luego ingresamos al endpoint de login</li>
  <li>Una vez dentro, podemos ver tanto nuestros datos como la de los demás usuarios.</li>
  <li>Unicamente podemos modificar nuestros datos y en caso de que seamos "admin" podemos modificar otros usuarios con el método PUT.</li>
  <li>Luego utilizamos otro GET para ver si efectivamente se realizó la actualización.</li>
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
      <td>/session/register</td>
      <td>Permite registrar a un usuario nuevo a través del método POST.</td>
    </tr>
    <tr>
      <td>/session/login</td>
      <td>que es lo que hace</td>
    </tr>
    <tr>
      <td>
        /session/profile/&lt;int:id_user&gt
      </td>
      <td>Una vez logeado permite ver a cualquier usuario indicando el número de ID</td>
    </tr>
        </tr>
        <tr>
      <td>/session/profile/edit/&lt;int:id_user&gt;</td>
      <td>Permite editar al usuarios, siempre y cuando quien edite sea el propio usuario o tenga el rol de "admin"</td>
    </tr>
        </tr>
    <tr>
      <td>/session/profile/status/&lt;int:id_user&gt;</td>
      <td>Permite cambiar el status al usuario seleccionado, hay 3 opciones, "activo", "inactivo" y "bloqueado".</td>
    </tr>
  </tbody>
</table>
