# oltOperations

### ESTRUCTURA DE ARCHIVO CSV DE LISTA DIARIA DE REACTIVACIONES

```
"Client,frame,slot,port,id"

siendo ese la estructura de las columnas de los datos a tomar en cuenta [cabe destacar que no se distingue entre OLT, se tiene que esta consciente de que olt se estan agregando los datos]

estos archivos se tienen que llamar respectivamente OLT1.csv para datos de clientes en OLTx15 y OLT2.csv para datos de clientes en la OLTx2
```

### ESTRUCTURA DE ARCHIVOS CSV PARA CARGA MASIVA CON DATOS DE ODOO

```
"nombre,frame,slot,port,id,ID externo,Cliente/NIF"

siendo ese la estructura de las columnas de los datos a tomar en cuenta [cave destacar que no se distingue entre OLT, se tiene que esta consciente de que olt se estan agregando los datos]

para este tipo de operacion se tendran en cuenta 2 listas 1 lista de datos en odoo [nota: esto es temporal hasta que en odoo se tengan dichos datos de olt] la primera es una lista de datos de odoo en la cual se tomara en cuenta datos como "NIF", "NOMBRE" e "ID EXTERNO" estos datos normalmente no vienen asii por tanto se tienen que adecuar a esa estructura : "Cliente/NIF,Cliente,ID externo" a su vez la segunda lista es la lista de datos operacionales del google drive en la cual se tomaran datos como "CI", "NOMBRE", "FRAME","SLOT","PORT","ID" de igual forma esos datos por defecto no estan asi, por lo cual se deben de adecuar a "Cliente/NIF,Cliente,f,s,p,id" para poder realizar de manera exitosa la comparacion de dichos datos
```
