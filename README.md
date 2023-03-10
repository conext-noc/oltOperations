# oltOperations

# SCRIPT PRINIPAL DE OPERACIONES EN CONEXT

Este Programa es para el uso interno de operaciones basicas/cotidianas en el area del NOC de CONEXT.

A continuacion se explicara a detalle el funcionamiento del mismo.

Principalmente hay 2 formas de utilizar el SCRIPT:

- Como script nativo en python
- Como aplicacion .exe [windows], .bin[linux], .app[macOS]

# INSTALACION

## COMO SCRIPT NATIVO:
Para correr esta aplicacion es necesario correr el siguiente comando [teniendo python & git instalado en el sistema]

1. Clonar el ropositorio con los archivos
- SSH:
```terminal 
[bash]$ git clone git@github.com/conext-noc/oltOperations.git
```

- HTTP:
```terminal
[bash]$ git clone https://github.com/conext-noc/oltOperations.git
```
2. Crear una carpeta "logs" en la carpeta de documentos del sistema

3. instalar las dependencias
```terminal
[bash]$ pip install -r requirements.txt
```

4. Descargar los archivos .env y .json de credenciales en el NOC de Conext
Seguidamente en la consola correr el siguiente comando

5. iniciar el script
```terminal
[bash]$ python main.py
```

## COMO EJECUTABLE:
1. Instalar la aplicacion setup.exe | setup.bin | setup.app, en los documentos del dispositivo, y a su vez crear un acceso directo con permisos de administrador

2. Crear una carpeta "logs" en la carpeta de documentos del sistema

3. Ejecutar la aplicacion [acceso directo]

# USO
Una vez ejecutado bien sea de forma de SCRIPT o de EJECUTABLE, se tendra un mensaje como el siguiente (opciones pueden variar):

- PUNTO PRINCIPAL
```
Seleccione el equipo a utilizar [ROUTER | OLT] : 
```

una vez seleccionado el tipo de equipo a usar, en estos se agrego una funcion de Debug, para visualizar los comandos emitidos por la consola, y verificar que todo este fuincionando con normalidad, esto puede ser utilizado para uso de aprendizage en cli HUAWEI o para verificar en que paso de la operacion esta fallando, y consultar con el ING de redes o el coordinador de IT para validar que los comandos en la CLI esten funcionando sin problemas

## ROUTER
```
Selecciona el router a monitorear [E1 | E2 | A1 | A2] : 
```

### DEFINICION DE CADA UNO DE LOS MODULOS

#### ROUTERS DE BORDE (EDGE [E])

En estos routers solo se le verficara el consumo en vivo de las interfaces del router escogido

se mostrara de la siguiente forma 
```terminal
| Interface                 | PHY       | Protocol  | InUti         | OutUti        | inErrors     | outErrors      |
| GigabitEthernet0/3/X(10G) | up/down   | up/down   | IN_CONSUMO_%  | OUT_CONSUMO_% | #_IN_ERRORS  | #__OUT_ERRORS  |
| GigabitEthernet0/3/Y(10G) | up/down   | up/down   | IN_CONSUMO_%  | OUT_CONSUMO_% | #_IN_ERRORS  | #__OUT_ERRORS  |
| GigabitEthernet0/3/X(10G) | up/down   | up/down   | IN_CONSUMO_%  | OUT_CONSUMO_% | #_IN_ERRORS  | #__OUT_ERRORS  |
| GigabitEthernet0/3/Y(10G) | up/down   | up/down   | IN_CONSUMO_%  | OUT_CONSUMO_% | #_IN_ERRORS  | #__OUT_ERRORS  |
| GigabitEthernet0/3/X(10G) | up/down   | up/down   | IN_CONSUMO_%  | OUT_CONSUMO_% | #_IN_ERRORS  | #__OUT_ERRORS  |
| GigabitEthernet0/3/Y(10G) | up/down   | up/down   | IN_CONSUMO_%  | OUT_CONSUMO_% | #_IN_ERRORS  | #__OUT_ERRORS  |
| GigabitEthernet0/3/X(10G) | up/down   | up/down   | IN_CONSUMO_%  | OUT_CONSUMO_% | #_IN_ERRORS  | #__OUT_ERRORS  |
| GigabitEthernet0/3/Y(10G) | up/down   | up/down   | IN_CONSUMO_%  | OUT_CONSUMO_% | #_IN_ERRORS  | #__OUT_ERRORS  |
| GigabitEthernet0/3/X(10G) | up/down   | up/down   | IN_CONSUMO_%  | OUT_CONSUMO_% | #_IN_ERRORS  | #__OUT_ERRORS  |
| GigabitEthernet0/3/Y(10G) | up/down   | up/down   | IN_CONSUMO_%  | OUT_CONSUMO_% | #_IN_ERRORS  | #__OUT_ERRORS  |
```

Se mostraran el consumo de las interfaces en 5 instancias (las mas recientes para cada una de las interfaces configuradas)


#### ROUTERS DE AGREGACION (AGGREGATION [A])
En estos routers se resolveran los conflictos en los segmentos de las IP que esten presentando problemas

En este modulo simplemente se veran que segmentos tienen conflitos, en caso de tener, estos se resolveran, encaso de no tener conflictos se mostrara un mensaje de "0 conflictos en [segmento]"


## OLT

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
    > (MG)  :   Migracion OLT
    > (AD)  :   Actualizacion de datos en olt
    > (DC)  :   CPDC
$
```
### DEFINICION DE CADA UNO DE LOS MODULOS

#### Modulos de Reactivacion (RU & RL) Y Suspencion de servicio (SU & SL)

Estos modulos son los encargados de reactivar o suspender el servicio de 1 o mas clientes a la vez, los modulos que inicien con R son modulos de reactivacion / activacion del servicio, los moulo que inicien con S son modulos de suspencion del servicio, entre estos se encuentran 2 principales funciones

##### OPCION "L"
En estos modulos se requiere de una lista de clientes en un archivo ".csv" o excel ".xlsx", la lista tiene que tener la siguente forma para poder funcionar con normalidad, ademas de tener en cuenta la OLT a emplear la lista [NOTA: en caso de que la lista sea generada por odoo, cambiar el nombre de la OLT por su numero correspondinete]

>| name | olt  | sn   | frame | slot | port | onu_id  | Referencia | Identificación externa| ID  |
>| :--: | :--: | :--: | :---: | :--: | :--: | :-----: | :--------: | :-------------------: | :-: |

Una vez establecida la lista, y seleccionada la opcion correspondiente este imprimira los datos y el cliente en consola por cada cliente que se este ejecutando la accion, al finalizar se requerira que se abra una carperta donde guardar los resultados de las operaciones

##### OPCION "U"

En este modulo no se requiere de una lista en concreto solo los datos pertienentes FRAME,SLOT, PORT, ONU_ID o SN para luego imprimir el cliente en pantalla al cual se le a realizado la operacion.

#### Modulos de Confirmacion de ont (Agregar ont) (IN & IP)

En este modulo se tienen 2 principales opciones "N" para una instalacion nueva desde 0, y "P" para una instalacion previa que por alguna razon haya sido rechazada, (Potencia, Nomenclatura erronea, etc...)

##### MODULO "IN":
Para este tipo de modulo se requeria saber el serial ont, tener los datos de ficha de instalacion pertinentes, en el prompt del programa se iran requiriendo los datos como lo son, nombre y plan, etc...
```terminal
 Ingrese el Serial del Cliente a buscar : INGRESAR VALORES PERTINENTES
```

Seguidamente apareceran una lista de los ONT disponibles para instalar, en caso de que el serial inresado este en esa lista el serial aparecera con un color VERDE y este atumaticamente tendra los datos de FRAME, SLOT, y PORT

Luego Sera Prompteado para ingresar los otros valores:
```terminal
Ingrese plan del cliente : 
```
Se ingresa el plan a instalar al cliente OZ_<NOMBRE_DE_PLAN>_<IDX_DE_PROVEEDOR> EJ: OZ_MAX_1
IDX DE PROVEEDOR: 1 => PROVEEDOR 1, 2 => PROVEEDOR 2, IP => SERVICIO DE IP PUBLICA
NOMBRES POSIBLES DE PLANES:
0 => NO INSTALAR
PLUS
MAX
NEXT
MAGICAL
SKY

```terminal
Ingrese nombre del cliente : 
```
Para ingresar el nombre del cliete se sigue la siguente nomenclatura:
<1> <2> <#_CONTRATO>
1: "PRIMER_NOMBRE", "NOMBRE_DE_EMPRESA_SEPARADOS_POR_PISOS", "CONDOMINIO_RESIDENCIA"
2: "SEGUNDO_NOMBRE", "CA", "NOMBRE_DE_RESIDENCIA_O_CONDOMINIO_SEPARADO_POR_PISOS"

```terminal
Ingrese el NIF del cliente [V123 | J123]: 
```
Este valor no sera agregado a la olt, este valor es asignado en la hoja de calculo de datos CPDC en conext [NOC]

una vez agregados los valores este comenzara con la instalacion, mostrara los siguentes valores en la pantalla de la terminal
```
La potencia del ONT es : (PWR) y la temperatura es : (TEMP)
  quieres proceder con la instalacion? [Y | N] : 
```

- En caso de no proceeder con la instalacion saldra el siguente mensaje:
    ```
    Por que no se le asignara servicio? : 
    ```
    se le agrega la razon por la cual el cliente no tendra servicio e imprime los datos operacionales en los cuales se tendran los datos antes asignados ademas de la razon por la cual no tiene servicio


```
El tipo de ONT del cliente es (ONT_TYPE)

El SPID que se le agregara al cliente es : (SPID)
```

Una vez verificados o no estos valores se procedera con el siguiente prompt

```
Se agregara vlan al puerto? (es bridge) [Y/N] :
```
En caso de que el ONT sea unbridge se le agrega la VLAN al puerto, de caso contrario no

- EN CASO DE SER IP PUBLICA
    ```
    Ingrese la IPv4 Publica del cliente : 
    ```

Seguida mente se imprimen los datos operacionales

##### MODULO "IP":
Para este modulo se requere saber en que puerto esta el ont, tener los datos de ficha de instalacion pertinentes o saber el serial del ONT del cliente, en el prompt del programa se iran requiriendo los datos como lo son, nombre, plan, slot,port, serial, proveedor, etc...
```
Buscar cliente por serial o por Datos de OLT [S | D] : 
```
si se buscan por sn ingrese SN del equipo y se le asignara un propt como el siguente...
en caso de que sea por datos, ingresar frame,slor,port,id segun sea requerido
```
|FRAME               :   VAL
|SLOT                :   VAL
|PORT                :   VAL
|ONU_ID              :   VAL
|NAME                :   VAL
|SN                  :   VAL
|STATE               :   VAL
|STATUS              :   VAL
|LAST DOWN CAUSE     :   VAL
|ONT TYPE            :   VAL
|IP                  :   VAL
|TEMPERATURA         :   VAL
|POTENCIA            :   VAL
|VLAN_{idx}              :   VAL FOR N SP CREATED
|PLAN_{idx}              :   VAL FOR N SP CREATED
|SPID_{idx}              :   VAL FOR N SP CREATED
```
como en el anterior se volvera a mostrar los datos operacionales para poder validar el estatus de potencia y temperatura...

#### Modulo de eliminacion de cliente

En este modulo como su titulo lo indica se podra eliminar de las OLT un cliente, se deben de proporcionar datos como lo son los datos de olt (F/S/P/ONU_ID) o Serial, seguidamente se validan los datos con un prompt:
```
|FRAME               :   VAL
|SLOT                :   VAL
|PORT                :   VAL
|ONU_ID              :   VAL
|NAME                :   VAL
|SN                  :   VAL
|STATE               :   VAL
|STATUS              :   VAL
|LAST DOWN CAUSE     :   VAL
|ONT TYPE            :   VAL
|IP                  :   VAL
|TEMPERATURA         :   VAL
|POTENCIA            :   VAL
|VLAN_{idx}              :   VAL FOR N SP CREATED
|PLAN_{idx}              :   VAL FOR N SP CREATED
|SPID_{idx}              :   VAL FOR N SP CREATED
Desea continuar? [Y | N] : 
```
Dependiendo de la respuesta se realiza o no la accion

#### Modulo de Modificacion de equipo

En este modulo se podra modificar los datos del cliente, se mostrara el siguente prompt
```
Que cambio se realizara? 
  > (CT)    :   Cambiar Titular
  > (CO)    :   Cambiar ONT
  > (CP)    :   Cambiar Plan & Vlan
  > (CV)    :   Cambiar Proveedor
  > (ES)    :   Eliminar Service Port
  > (AS)    :   Agregar Service Port
  > (AV)    :   Agregar Voip [Solo OLT 1 (X15 nueva)]
$ 
```

##### Modulo de cambio de titular
En este modulo se requerira los datos del cliente (F/S/P/ONU_ID) o SN seguidamente se verificara que son los datos del cliente con un prompt como el siguinete:
```
|FRAME               :   VAL
|SLOT                :   VAL
|PORT                :   VAL
|ONU_ID              :   VAL
|NAME                :   VAL
|SN                  :   VAL
|STATE               :   VAL
|STATUS              :   VAL
|LAST DOWN CAUSE     :   VAL
|ONT TYPE            :   VAL
|IP                  :   VAL
|TEMPERATURA         :   VAL
|POTENCIA            :   VAL
|VLAN_{idx}              :   VAL FOR N SP CREATED
|PLAN_{idx}              :   VAL FOR N SP CREATED
|SPID_{idx}              :   VAL FOR N SP CREATED
Desea continuar? [Y | N] : 
```
luego se procede a preguntar el nuevo titular del cliente *SIGUIENDO LAS NORMAS DE NOMENCLATURA PREVIAMENTE ESTABLECIDAS*

##### Modulo de cambio de ONT
En este modulo se requerira los datos del cliente (F/S/P/ONU_ID) o SN seguidamente se verificara que son los datos del cliente con un prompt como el siguinete:
```
|FRAME               :   VAL
|SLOT                :   VAL
|PORT                :   VAL
|ONU_ID              :   VAL
|NAME                :   VAL
|SN                  :   VAL
|STATE               :   VAL
|STATUS              :   VAL
|LAST DOWN CAUSE     :   VAL
|ONT TYPE            :   VAL
|IP                  :   VAL
|TEMPERATURA         :   VAL
|POTENCIA            :   VAL
|VLAN_{idx}              :   VAL FOR N SP CREATED
|PLAN_{idx}              :   VAL FOR N SP CREATED
|SPID_{idx}              :   VAL FOR N SP CREATED
Desea continuar? [Y | N] : 
```
Luego se requerira ingresar el nuevo ONT del cliente y si ese ONT es un bridge o no

##### Modulo de cambio de Plan y Vlan/Proveedor
En este modulo se requerira los datos del cliente (F/S/P/ONU_ID) o SN seguidamente se verificara que son los datos del cliente con un prompt como el siguinete:
```
|FRAME               :   VAL
|SLOT                :   VAL
|PORT                :   VAL
|ONU_ID              :   VAL
|NAME                :   VAL
|SN                  :   VAL
|STATE               :   VAL
|STATUS              :   VAL
|LAST DOWN CAUSE     :   VAL
|ONT TYPE            :   VAL
|IP                  :   VAL
|TEMPERATURA         :   VAL
|POTENCIA            :   VAL
|VLAN_{idx}              :   VAL FOR N SP CREATED
|PLAN_{idx}              :   VAL FOR N SP CREATED
|SPID_{idx}              :   VAL FOR N SP CREATED
Desea continuar? [Y | N] : 
```
Luego se requeriran los datos del nuevo plan *RECORDAR QUE EL NOMBRE DE PLAN TIENE INTRINSECAMENTE EL INDICE DE PROVEEDOR*

##### Modulo de cambio de proveedor
En este modulo se requerira los datos del cliente (F/S/P/ONU_ID) o SN seguidamente se verificara que son los datos del cliente con un prompt como el siguinete:
```
|FRAME               :   VAL
|SLOT                :   VAL
|PORT                :   VAL
|ONU_ID              :   VAL
|NAME                :   VAL
|SN                  :   VAL
|STATE               :   VAL
|STATUS              :   VAL
|LAST DOWN CAUSE     :   VAL
|ONT TYPE            :   VAL
|IP                  :   VAL
|TEMPERATURA         :   VAL
|POTENCIA            :   VAL
|VLAN_{idx}              :   VAL FOR N SP CREATED
|PLAN_{idx}              :   VAL FOR N SP CREATED
|SPID_{idx}              :   VAL FOR N SP CREATED
Desea continuar? [Y | N] : 
```
Luego se requeriran los datos del nuevo plan *RECORDAR QUE EL NOMBRE DE PLAN TIENE INTRINSECAMENTE EL INDICE DE PROVEEDOR*
Este modulo difiere del anteror en que este no cambia los LINE_PROFILES y SRV_PROFILES, solo cambia la vlan, solo emplear este modulo en caso de agregar vlan


##### Modulo de Eliminar SPID
En este modulo se requerira los datos del cliente (F/S/P/ONU_ID) o SN seguidamente se verificara que son los datos del cliente con un prompt como el siguinete:
```
|FRAME               :   VAL
|SLOT                :   VAL
|PORT                :   VAL
|ONU_ID              :   VAL
|NAME                :   VAL
|SN                  :   VAL
|STATE               :   VAL
|STATUS              :   VAL
|LAST DOWN CAUSE     :   VAL
|ONT TYPE            :   VAL
|IP                  :   VAL
|TEMPERATURA         :   VAL
|POTENCIA            :   VAL
|VLAN_{idx}              :   VAL FOR N SP CREATED
|PLAN_{idx}              :   VAL FOR N SP CREATED
|SPID_{idx}              :   VAL FOR N SP CREATED
Desea continuar? [Y | N] : 
```
Seguidamente el SPID sera eliminado y el cliente quedara sin servicio

##### Modulo de Agregar SPID
En este modulo se requerira los datos del cliente (F/S/P/ONU_ID) o SN seguidamente se verificara que son los datos del cliente con un prompt como el siguinete:
```
|FRAME               :   VAL
|SLOT                :   VAL
|PORT                :   VAL
|ONU_ID              :   VAL
|NAME                :   VAL
|SN                  :   VAL
|STATE               :   VAL
|STATUS              :   VAL
|LAST DOWN CAUSE     :   VAL
|ONT TYPE            :   VAL
|IP                  :   VAL
|TEMPERATURA         :   VAL
|POTENCIA            :   VAL
|VLAN_{idx}              :   VAL FOR N SP CREATED
|PLAN_{idx}              :   VAL FOR N SP CREATED
|SPID_{idx}              :   VAL FOR N SP CREATED
Desea continuar? [Y | N] : 
```
Seguidamente el SPID sera agregado y se seguira el proceso como si se fuese a agregar un nuevo plan


##### Modulo de Agregar VOIP [DEVELOPMENT]
En este modulo se requerira los datos del cliente (F/S/P/ONU_ID) o SN seguidamente se verificara que son los datos del cliente con un prompt como el siguinete:
```
|FRAME               :   VAL
|SLOT                :   VAL
|PORT                :   VAL
|ONU_ID              :   VAL
|NAME                :   VAL
|SN                  :   VAL
|STATE               :   VAL
|STATUS              :   VAL
|LAST DOWN CAUSE     :   VAL
|ONT TYPE            :   VAL
|IP                  :   VAL
|TEMPERATURA         :   VAL
|POTENCIA            :   VAL
|VLAN_{idx}              :   VAL FOR N SP CREATED
|PLAN_{idx}              :   VAL FOR N SP CREATED
|SPID_{idx}              :   VAL FOR N SP CREATED
Desea continuar? [Y | N] : 
```
Seguidamente se requeriran los datos para agregar este tipo de servicio

NOTA: ESTE MODULO ESTA EN DESARROLLO

<!-- NOTA PARA EL DESARROLLADOR: QUITAR LAS NOTAS Y EL "[DEVELOPMENT]" UNA VEZ CONFIGURADO Y TESTADO CORRECTAMENTE ESTE MODULO -->


#### Modulo de busqueda de equipos (BC)

En este modulo se puede buscar un cliente,  ben sea por datos (F/S/P/ONU_ID), por serial, o por nombre

```terminal
Buscar cliente por serial, por Datos de OLT o por nombre [S | D | N] : 
```
- Si se buscan por sn o por datos ingrese aparecera un prompt como el siguente...
```terminal
|FRAME               :   VAL
|SLOT                :   VAL
|PORT                :   VAL
|ONU_ID              :   VAL
|NAME                :   VAL
|SN                  :   VAL
|STATE               :   VAL
|STATUS              :   VAL
|LAST DOWN CAUSE     :   VAL
|ONT TYPE            :   VAL
|IP                  :   VAL
|TEMPERATURA         :   VAL
|POTENCIA            :   VAL
|VLAN_{idx}              :   VAL FOR N SP CREATED
|PLAN_{idx}              :   VAL FOR N SP CREATED
|SPID_{idx}              :   VAL FOR N SP CREATED

en caso de que se requiera ficha de instalacion se pedira en la terminal

- Si se busca por nombre se ingresa el nombre y aparecera un prompt como el siguente
    | F/S/P | ONU_ID | NAME | STATUS | STATE | SN |

```

#### Modulo de verificacion de consumo
En este modulo se verificara el consumo del cliente y requeriran los datos del cliente (F/S/P/ONU_ID) o SN seguidamente se verificara que son los datos del cliente con un prompt como el siguinete:
```
|FRAME               :   VAL
|SLOT                :   VAL
|PORT                :   VAL
|ONU_ID              :   VAL
|NAME                :   VAL
|SN                  :   VAL
|STATE               :   VAL
|STATUS              :   VAL
|LAST DOWN CAUSE     :   VAL
|ONT TYPE            :   VAL
|IP                  :   VAL
|TEMPERATURA         :   VAL
|POTENCIA            :   VAL
|VLAN_{idx}              :   VAL FOR N SP CREATED
|PLAN_{idx}              :   VAL FOR N SP CREATED
|SPID_{idx}              :   VAL FOR N SP CREATED
Desea continuar? [Y | N] : 
```

seguidamente se verificara el consumo en tiempo real en 5 puntos, y se mostrara un promedio de los datos obtenidos

#### Modulo de verificacion de Puerto
En este modulo se requerira que se acceda a los F/S/P de los clientes que quiere validar
una vez ingresados se imprimira en el prompt lo siguiente con los datos de los clientes:
```
| f/s/p | onu_id | name | state | status | last_down_cause | pwr | last_down_time | last_down_date | device | sn |
```
seguidamente se imprimiran los datos del puerto
```
En el puerto [F/S/P]:
El total del clientes en el puerto es       :   #_VAL
El total del clientes activos es            :   #_VAL
El total del clientes desactivados es       :   #_VAL
El total del clientes activos en corte es   :   #_VAL
El total del clientes activos apagados es   :   #_VAL
```

y por ultimo se reuerira si continuar y agregar los datos del puerto a verificar, o cancelar

#### Modulo de Clientes con averia
En este modulo se accederan a todos lo puertos disponibles en la olt,seguidamente se imprimira en el prompt lo siguiente con los datos de los clientes:
```
| f/s/p | onu_id | name | state | status | last_down_cause | pwr | last_down_time | last_down_date | device | sn |
```
sigueindo la nomenclatura de colores realizar acciones acorde a lo requerido en el NOC

#### Modulo de Clientes desactivados totales
En este modulo se accederan a todos lo puertos disponibles en la olt,seguidamente se imprimira en el prompt lo siguiente con los datos de los clientes:
```
| f/s/p | onu_id | name | state | status | last_down_cause | pwr | last_down_time | last_down_date | device | sn |
```
sigueindo la nomenclatura de colores realizar acciones acorde a lo requerido en el NOC

#### Modulo de Migracion
En estos modulos se requiere de una lista de clientes en un archivo ".csv" o excel ".xlsx", la lista tiene que tener la siguente forma para poder funcionar con normalidad, ademas de tener en cuenta la OLT a emplear la lista [NOTA: en caso de que la lista sea generada por odoo, cambiar el nombre de la OLT por su numero correspondinete]

>| name | olt  | sn   | frame | slot | port | onu_id  | Referencia | Identificación externa| ID  |
>| :--: | :--: | :--: | :---: | :--: | :--: | :-----: | :--------: | :-------------------: | :-: |

Una vez establecida la lista, y seleccionada la opcion correspondiente este imprimira los datos y el cliente en consola por cada cliente que se este ejecutando la accion.

#### Modulo de Actualizacion masiva de datos
En estos modulos se requiere de una lista de clientes en un archivo ".csv" o excel ".xlsx", la lista tiene que tener la siguente forma para poder funcionar con normalidad, ademas de tener en cuenta la OLT a emplear la lista [NOTA: en caso de que la lista sea generada por odoo, cambiar el nombre de la OLT por su numero correspondinete]

>| name | olt  | sn   | frame | slot | port | onu_id  | Referencia | Identificación externa| ID  |
>| :--: | :--: | :--: | :---: | :--: | :--: | :-----: | :--------: | :-------------------: | :-: |

Una vez establecida la lista, y seleccionada la opcion correspondiente este imprimira los datos y el cliente en consola por cada cliente que se este ejecutando la accion.

#### Modulo de CPDC
En este modulo no se requiere ingresar ninun dato, al finalizar este modulo entregara un archivo excel con todos los datos pertinentes de todos los clientes instalados en la OLT

# NOTA:
## CODIGO DE COLORES DE SCRIPT
COLOR                       | SIGNIFICADO
- verde                     : mensajes de exito
- verde claro               : cliente activo y con servicio
- amarillo                  : mensajes informativos
- rojo                      : error
- rojo claro                : apagado
- rojo obscuro              : LOS
- rojo obscuro [vinotinto]  : LOS por mas de 5 dias
- azul                      : datos de cliente
- morado                    : error en data de cliente
- gris                      : cliente desactivado por menos de 60 dias
- gris obscuro              : cliente desactivado por mas de 60 dias
- naranja                   : advertencia
