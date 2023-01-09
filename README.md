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
> pip install -r requirements.txt
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
> Descargar el archivo .json de credenciale en el NOC de Conext
>
> 
> Seguidamente en la consola correr el siguiente comando
>
> ```terminal
> python main.py
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
    > (RL)  :   Reactivar con lista
    > (RU)  :   Reactivar uno
    > (SL)  :   Suspender con lista
    > (SU)  :   Suspender uno
    > (IN)  :   Instalar nuevo
    > (IP)  :   Instalar previo
    > (BC)  :   Buscar cliente en OLT
    > (EC)  :   Eliminar Cliente
    > (MC)  :   Modificar Cliente
    > (VC)  :   Verificar consumo
    > (VP)  :   Verificacion de puerto
    > (CA)  :   Clientes con averias (corte de fibra)
    > (DT)  :   Desactivados Totales
$
```

### Modulos de Reactivacion (RX) Y Suspencion de servicio (SX)

Estos modulos son los encargados de reactivar o suspender el servicio de 1 o mas clientes a la vez, los modulos que inicien con R son modulos de reactivacion / activacion del servicio, los moulo que inicien con S son modulos de suspencion del servicio, entre estos se encuentran 3 principales funciones

> OPCION "L"
>
> En estos modulos se requiere de una lista de clientes en un archivo ".csv" o excel ".xlsx", la primera fila de esta lista tiene que tener la siguente forma para poder funcionar con normalidad, ademas de tener en cuenta la OLT a emplear la lista
>
> | name | olt  | sn   | frame | slot | port | id  |
> | :--: | :--: | :--: | :---: | :--: | :--: | :-: |
>
> Una vez establecida la lista, y seleccionada la opcion correspondiente este imprimira los datos y el cliente en consola por cada cliente que se este ejecutando la accion, al finalizar se requerira que se abra una carperta donde guardar los resultados de las operaciones

> OPCION "U"
>
> En este modulo no se requiere de una lista en concreto solo los datos pertienentes FRAME,SLOT, PORT, ID o SN para luego imprimir el cliente en pantalla al cual se le a realizado la operacion.

### Modulos de Confirmacion de ont (Agregar ont) (IX)

En este modulo se tienen 2 principales opciones "N" para una instalacion nueva desde 0, y "P" para una instalacion previa que por alguna razon haya sido rechazada, [IN, IP]

> MODULO "IN":
>
> Para este tipo de modulo se requeria saber el serial ont, tener los datos de ficha de instalacion pertinentes, en el prompt del programa se iran requiriendo los datos como lo son, nombre y plan, etc...
>
> ```terminal
> Ingrese el Serial del Cliente a buscar : : INGRESAR VALORES PERTINENTES
> ```

###############################################################

>
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

> MODULO "IP":
>
> Para este tipo de modulo se requeria saber en que puerto esta el ont, tener los datos de ficha de instalacion pertinentes, en el prompt del programa se iran requiriendo los datos como lo son, nombre, plan, slot,port, serial, proveedor, etc...
>
> ```
> Buscar cliente por serial o por Datos de OLT [S | D] : 
> ```
>
> si se buscan por sn ingrese SN del equipo y se le asignara un propt como el siguente...
> en caso de que sea por datos, ingresar frame,slor,port,id segun sea requerido
>
> ```
> |FRAME               :   VAL
> |SLOT                :   VAL
> |PORT                :   VAL
> |ID                  :   VAL
> |NAME                :   VAL
> |SN                  :   VAL
> |STATE               :   VAL
> |STATUS              :   VAL
> |LAST DOWN CAUSE     :   VAL
> |ONT TYPE            :   VAL
> |IP                  :   VAL
> |TEMPERATURA         :   VAL
> |POTENCIA            :   VAL
>
> |VLAN_{idx}              :   VAL FOR N SP CREATED
> |PLAN_{idx}              :   VAL FOR N SP CREATED
> |SPID_{idx}              :   VAL FOR N SP CREATED
> ```
>
> como en el anterior se volvera a mostrar los datos operacionales para poder validar el estatus de potencia y temperatura...

### Modulo de eliminacion de cliente

En este modulo como su titulo lo indica se podra eliminar de las OLT un cliente, se deben de proporcionar datos como lo son NOMBRE,SLOT,PORT,ID

### Modulo de Modificacion de equipo

En este modulo se podra modificar el titular del equipo [CT] o un cambio de ont [CO]
en ambos se debera de seguir el prompt en los datos que se requieran

#### Modulo de cambio de Vlan/Proveedor

En este Modulo se requeriran los datos: SLOT,PORT,ID,NAME para poder proceder con el cambio de proveedor al cliente

#### Modulos de Busqueda de ONT

En estos modulos se tienen principalmente 2 opciones un cliente ya agregado [BE] o uno nuevo [BN]

> MODULO BE:
>
> se podra localizar un cliente mediante algun nombre [N] o el serial [S] que este tiene
> cabe destacar que cuando se busca el nombre se muestran todos los resultados de los clientes que tengan ese nombre ingresado

> MODULO BN:
>
> en este modulo se buscaran todos los ONT disponibles para agregar que estan en la OLT

#### Modulo de cambio de plan

En este modulo como su titulo lo indica se podra cambiar de plan a un cliente, se deben de proporcionar datos como lo son NOMBRE,SLOT,PORT,ID

### Modulos de verificacion de valores

En estos modulos se podran verificar varios valores, desde el estatus del SPID [VS], wan interface para un posible reset del ont [VR], valores operacionales [VV], cosumo [VC], verificacion de puerto [VP] y verificacion de averias para el correo de averias [VA]

En cada uno se debe de seguir los datos que se piden en el prompt para poder validar el estatus del o los clinetes

### Modulo de busqueda de equipos (BX)

En este modulo se tienen 2 principales opciones "N" para buscar todos los ONT sin agregar en la OLT y "E" para buscar los datos de un ont en especifico que este agregado y exista en la OLT

> MODULO "BN":
>
> Este modulo muestra todos los ONT disponibles en la OLT.

> MODULO "BE":
>
> Para este tipo de modulo se requeria saber en que puerto esta el ont, tener los datos de ficha de instalacion pertinentes, en el prompt del programa se iran requiriendo los datos como lo son, nombre, plan, slot,port, serial, proveedor, etc...
>
> ```terminal
> Buscar cliente por serial o por Datos de OLT [S | D] : 
> ```
> si se buscan por sn ingrese SN del equipo y se le asignara un propt como el siguente...
> en caso de que sea por datos, ingresar frame,slor,port,id segun sea requerido
>
> ```terminal
> |FRAME               :   VAL
> |SLOT                :   VAL
> |PORT                :   VAL
> |ID                  :   VAL
> |NAME                :   VAL
> |SN                  :   VAL
> |STATE               :   VAL
> |STATUS              :   VAL
> |LAST DOWN CAUSE     :   VAL
> |ONT TYPE            :   VAL
> |IP                  :   VAL
> |TEMPERATURA         :   VAL
> |POTENCIA            :   VAL
>
> |VLAN_{idx}              :   VAL FOR N SP CREATED
> |PLAN_{idx}              :   VAL FOR N SP CREATED
> |SPID_{idx}              :   VAL FOR N SP CREATED
> ```
