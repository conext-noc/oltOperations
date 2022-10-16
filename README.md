# oltOperations

Este Programa es para el uso interno de operaciones basicas/cotidianas en el area del NOC de CONEXT.

A continuacion se explicara a detalle el funcionamiento del mismo.

Principalmente hay 2 formas de utilizar el SCRIPT:

- Como script nativo en python
- Como aplicacion .exe [windows], .bin[linux], .app[macOS]

## INSTALACION

> COMO SCRIPT NATIVO:
>
> Para correr esta aplicacion es necesario correr el siguiente comando [teniendo python instalado en el sistema]
>
> ```terminal
> pip install paramiko pandas csv python-dotenv tkinter python-regex
> ```
>
> Luego crear un archivo ".env" con las variables de entorno
>
> ```.env
> user="USUARIO DEL EQUIPO"
> password="CONTRASEÑA DEL EQUIPO"
> port=22
> ```
>
> Seguidamente en la consola correr el siguiente comando
>
> ```terminal
> python index.py
> ```

> COMO EJECUTABLE:
>
> Instalar la aplicacion setup.exe | setup.bin | setup.app, en los documentos del dispositivo, y a su vez crear un acceso directo con permisos de administrador
>
> Ejecutar la aplicacion [acceso directo]

## USO

Una vez ejecutado bien sea de forma de SCRIPT o de EJECUTABLE, se tendra un mensaje como el siguiente (opciones pueden variar):

```
Que accion se realizara?
  > (RC)  :  Reactivar Clientes (lista)
  > (RO)  :  Reactivar con lista de Odoo
  > (RU)  :  Reactivar uno
  > (SC)  :  Suspender Clientes
  > (SO)  :  Suspender con lista de Odoo
  > (SU)  :  Suspender uno
  > (IN)  :  Instalar nuevo
  > (IP)  :  Instalar previo
  > (EC)  :  Eliminar Cliente
  > (BN)  :  Buscar cliente en OLT (no agregado)
  > (BE)  :  Buscar cliente en OLT (ya agregado)
  > (CP)  :  Cambio de plan
  > (MC)  :  Modificar Cliente
  > (VV)  :  Verificar valores de ont
  > (VC)  :  Verificar consumo
  > (VR)  :  Verificar reset
  > (VS)  :  Verificar Service-Port ID
  > (VP)  :  Verificacion de puerto
  > (CV)  :  Cambio Vlan (Proveedor)
  > (CA)  :  Clientes con averias (corte de fibra)
$
```

### Modulos de Reactivacion Y Suspencion de servicio

Estos modulos son los encargados de reactivar o suspender el servicio de 1 o mas clientes a la vez, los modulos que inicien con R son modulos de reactivacion / activacion del servicio, los moulo que inicien con S son modulos de suspencion del servicio, entre estos se encuentran 3 principales funciones

> OPCION "C"
>
> En estos modulos se requiere de una lista de clientes en un archivo ".csv", la primera fila de esta lista tiene que tener la siguente forma para poder funcionar con normalidad
> | NOMBRE | OLT | FRAME | SLOT | PORT | ID |
> |:------:|:---:|:-----:|:----:|:----:|:--:|
>
> Una vez establecida la lista, y seleccionada la opcion correspondiente este imprimira los datos y el cliente en consola por cada cliente que se este ejecutando la accion, al finalizar se requerira que se abra una carperta donde guardar los resultados de las operaciones

> OPCION "O"
>
> En estos modulos se requiere de una lista con los datos de odoo [lista1] de clientes en un archivo ".csv", la segunda lista es una lista que posea los datos pertinentes olt frame slot port onu-id [lista22], la primera fila de esta lista1 tiene que tener la siguente forma para poder funcionar con normalidad
> | Cliente | Cliente/NIF | ID externo | _columnas opcionales_ |
> |:-------:|:-----------:|:----------:|:---------------------:|
>
> la primera fila de esta lista2 tiene que tener la siguente forma para poder funcionar con normalidad
> | NOMBRE | OLT | FRAME | SLOT | PORT | ID | NIF |
> |:------:|:---:|:-----:|:----:|:----:|:--:|:---:|
>
> Una vez establecida la lista1 y lista2, y seleccionada la opcion correspondiente este imprimira los datos y el cliente en consola por cada cliente que se este ejecutando la accion, al finalizar se requerira que se abra una carperta donde guardar los resultados de las operaciones

> OPCION "U"
>
> En este modulo no se requiere de una lista en concreto solo los datos pertienentes, NOMBRE, FRAME,SLOT, PORT, ID, para luego imprimir el cliente en pantalla al cual se le a realizado la operacion, sin necesidad de agregar los resultados a un archivo ".csv"

### Modulos de Confirmacion de ont (Agregar ont)

En este modulo se tienen 2 principales opciones "N" para una instalacion nueva desde 0, y "P" para una instalacion previa que por alguna razon haya sido rechazada, [IN, IP]

> MODULO N:
>
> Para este tipo de modulo se requeria saber en que puerto esta el ont, tener los datos de ficha de instalacion pertinentes, en el prompt del programa se iran requiriendo los datos como lo son, nombre, plan, slot,port, serial, vlan, service profile, line profile, etc...
> una vez agregados los valores este cpomenzara con la instalacion, se ha hagregado una opcion que permite verificar que vlan se le ha agregado manualmente al ont para poder ver esto en el prompt
>
> ```
> Desea verificar si el cliente ya tiene la wan interface configurada? [Y | N] :
> ```
>
> una vez verificados o no estos valores se procedera con el siguiente prompt
>
> ```
> Se agregara vlan al puerto? (es bridge) [Y/N] :
> ```
>
> para poder agregar la proveedor al puerto es decir se trata de un bridge
>
> seguidamente se mostraran los datos operacionales (potencia y temperatura) para poder proceder con la instalacion de lo contrario se agregara al cliente pero este no tendra servicio (vease MODULO P para poder terminar de asignar servicio al cliente)

> MODULO "P":
>
> Para este tipo de modulo se requeria saber en que puerto esta el ont, tener los datos de ficha de instalacion pertinentes, en el prompt del programa se iran requiriendo los datos como lo son, nombre, plan, slot,port, serial, proveedor, etc...
> como en el anterior se volvera a mostrar los datos operacionales para poder validar el estatus de potencia y temperatura...

### Modulo de eliminacion de cliente

En este modulo como su titulo lo indica se podra eliminar de las OLT un cliente, se deben de proporcionar datos como lo son NOMBRE,SLOT,PORT,ID

### Modulo de Modificacion de equipo

En este modulo se podra modificar el titular del equipo [CT] o un cambio de ont [CO]
en ambos se debera de seguir el prompt en los datos que se requieran

### Modulo de cambio de Vlan/Proveedor

En este Modulo se requeriran los datos: SLOT,PORT,ID,NAME para poder proceder con el cambio de proveedor al cliente

### Modulos de Busqueda de ONT

En estos modulos se tienen principalmente 2 opciones un cliente ya agregado [BE] o uno nuevo [BN]

> MODULO BE:
>
> se podra localizar un cliente mediante algun nombre [N] o el serial [S] que este tiene
> cabe destacar que cuando se busca el nombre se muestran todos los resultados de los clientes que tengan ese nombre ingresado

> MODULO BN:
>
> en este modulo se buscaran todos los ONT disponibles para agregar que estan en la OLT

### Modulo de cambio de plan

En este modulo como su titulo lo indica se podra cambiar de plan a un cliente, se deben de proporcionar datos como lo son NOMBRE,SLOT,PORT,ID

### Modulos de verificacion de valores

En estos modulos se podran verificar varios valores, desde el estatus del SPID [VS], wan interface para un posible reset del ont [VR], valores operacionales [VV], cosumo [VC], verificacion de puerto [VP] y verificacion de averias para el correo de averias [VA]

En cada uno se debe de seguir los datos que se piden en el prompt para poder validar el estatus del o los clinetes
