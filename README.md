# oltOperations

Existen Principalmente 2 modulos accion y confirmacion:

- ACCION:
  en este modulo se ejecutan acciones como reactivar a un cliente o desactivar a un cliente por pago.

- CONFIRMACION:
  en este modulo se ejecuta la accion de confirmar o agregar un cliente desde 0 o confirmar un cliente que se haya instalado y no se le haya dado servicio por potencia o cualquier tipo de inconveniente.

## USO DE ACCION

Para el uso de esta funcion es necesario tener una lista de tipo ".csv" para poder realizar las acciones (para formulacion de dichos archivos lea "ESTRUCTURA DE ARCHIVO CSV DE LISTA DIARIA DE REACTIVACIONES" o "ESTRUCTURA DE ARCHIVOS CSV PARA CARGA MASIVA CON DATOS DE ODOO").

para acceder a esta funcion, al iniciar el archivo se selecciona la opcion "activar/desactivar cliente (o)", procede a ingresar "o" en la terminal.

seguidamente se le requerira especificar el tipo de accion a realizar (activate | deactivate) para reconectar [activar] o desactivar.

luego se requerira de especificar si se requieren datos de odoo (como lo es el uso de "ID externo") para ello presionar "y" y seguidamente continuar con la seleccion de los archivos correspondientes, como lo son la seleccion de la localizacion del archivo de resultados, la lista de clientes de los datos operacionales de operaciones y la lista de corte descargaada enviada por facturacion.

si no se requieren de los datos de odoo presionar "n" y continuar con la seleccion del archivo de resultados de la operacion y la seleccion de la lista de core anteriormente adecuada (para la formulacion de este archivo vease "ESTRUCTURA DE LOS ARCHIVO CSV DE LISTA DIARIA DE REACTIVACIONES").

### ESTRUCTURA DE ARCHIVO CSV DE LISTA DIARIA DE REACTIVACIONES

```
"Client,frame,slot,port,id"
```

siendo ese la estructura de las columnas de los datos a tomar en cuenta [cabe destacar que no se distingue entre OLT, se tiene que esta consciente de que olt se estan agregando los datos]

estos archivos se tienen que llamar respectivamente OLT1.csv para datos de clientes en OLTx15 y OLT2.csv para datos de clientes en la OLTx2

### ESTRUCTURA DE ARCHIVOS CSV PARA CARGA MASIVA CON DATOS DE ODOO


> "ODOO.csv"
```
"nombre,ID externo,Cliente/NIF"
```

> "CLIENTES.csv"
```
"nombre,nif,f,s,p,id"
```


siendo ese la estructura de las columnas de los datos a tomar en cuenta [cave destacar que no se distingue entre OLT, se tiene que esta consciente de que olt se estan agregando los datos]

para este tipo de operacion se tendran en cuenta 2 listas 1 lista de datos en odoo [nota: esto es temporal hasta que en odoo se tengan dichos datos de olt] la primera es una lista de datos de odoo en la cual se tomara en cuenta datos como "NIF", "NOMBRE" e "ID EXTERNO" estos datos normalmente no vienen asii por tanto se tienen que adecuar a esa estructura : "Cliente/NIF,Cliente,ID externo" a su vez la segunda lista es la lista de datos operacionales del google drive en la cual se tomaran datos como "CI", "NOMBRE", "FRAME","SLOT","PORT","ID" de igual forma esos datos por defecto no estan asi, por lo cual se deben de adecuar a "Cliente/NIF,Cliente,f,s,p,id" para poder realizar de manera exitosa la comparacion de dichos datos
