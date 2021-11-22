# Proyectos de Simulación basado en Eventos Discretos

Carmen Irene Cabrera Rodríguez 
C412

Perfil de Github: [cicr99](https://github.com/cicr99)

## Orden del problema

### Happy Computing

Happy Computing es un taller de reparaciones electrónicas donde se realizan las
siguientes actividades (el precio de cada servicio se muestra entre paréntesis):

1. Reparación por garantía (Gratis)
2. Reparación fuera de garantía ($350)
3. Cambio de equipo ($500)
4. Venta de equipos reparados ($750)
   
Se conoce además que el taller cuenta con 3 tipos de empleados: Vendedor,
Técnico y Técnico Especializado.

Para su funcionamiento, cuando un cliente llega al taller, es atendido por un vendedor y en caso de que el servicio que requiera sea una Reparación (sea
de tipo 1 o 2) el cliente debe ser atendido por un técnico (especializado o no). Además en caso de que el cliente quiera un cambio de equipo este debe ser atendido por un técnico especializado. Si todos los empleados que pueden atender al cliente están ocupados, entonces se establece una cola para sus servicios. Un técnico especializado solo realizará reparaciones si no hay ningún cliente que desee un cambio de equipo en la cola.

Se conoce que los clientes arriban al local con un intervalo de tiempo que distribuye poisson con λ = 20 minuts y que el tipo de servicios que requieren puede ser descrito mediante la tabla de probabilidades:
| Tipo de Servicio | Probabilidad |
| ---------------- | ------------ |
| 1                | 0.45         |
| 2                | 0.25         |
| 3                | 0.1          |
| 4                | 0.2          |

Además se conoce que un técnico tarda un tiempo que distribuye exponecial con λ = 20 minutos, en realizar una reparación cualquiera. Un técnico especializdo tarda un tiempo que distribuye exponencial con λ = 15 minutos para
realizar un cambio de equipos y la vendedora puede atender cualquier servicio
en un tiempo que distribuye normal (N(5 min, 2 min)).
El dueño del lugar desea realizar una simulación de la ganancia que tendría en
una jornada laboral si tuviera 2 vendedores, 3 técnicos y 1 técnico especializado.

## Principales ideas seguidas para la solución del problema

La solución del problema está basada en un modelo de eventos discretos. Se trabaja sobre una línea temporal (*timeline*) que contiene los eventos en orden ascendente de tiempo, lo que quiere decir que se manejará primero aquel evento que se encuentre más cercano al tiempo actual. Cada vez que se toma un evento, se generan los tiempos necesarios para su tratamiento, ya sea el tiempo para que finalice, o para que ocurra el siguiente evento del mismo tipo; con dicho tiempo se crea un nuevo evento que se añade a la línea temporal.

Se implementó para el comportamiento de los empleados del taller la clase *Worker* (clase más general de la que heredan otras). Cada trabajador tiene un *status* que puede ser *Busy* o *Free* en dependencia si está ateniendo a algún cliente o no respectivamente. Con dicha clase se maneja la generación del tiempo que demora realizar un trabajo dependiendo de cada empleado, el cambio de satus según la actividad, la atención a un cliente nada más que este arribe al taller o si está en la cola, etcétera.

Igualmente se implementó una clase para los clientes que almacena el servicio que este requiere así como su número de cliente (este número indica que fue el n-ésimo cliente en arribar al taller). Para trabajar con mayor facilidad la cola de clientes, se creó la clase cola que contiene una cola por cada servicio y se encarga de remover y añadir los clientes a las colas correspondientes.

La simulación comienza con el arribo de un cliente al taller. Se genera de igual forma el tipo de servicio que este desea. El evento de arribo del cliente viene acompañado de la generación del próximo evento de este tipo, como se mencionó al inicio. Se hace un recorrido por los trabajadores para determinar si el cliente puede ser atendido o no instantáneamente. En caso de que sí, se debe generar también el tiempo de finalización del trabajo por el empleado con el cliente, añadiendo un nuevo evento a la línea de tiempo. Si el cliente no puede ser atendido, pasa a ser añadido a la cola.

El otro evento con el que se debe lidiar es la finalización del trabajo por un empleado. El cliente realiza el pago y el empleado pasa a tener un *status Free*. Se pasa a revisar la cola para atender a algún cliente si es necesario. En caso de que se tome a algún cliente de la cola, el empleado vuelve a estar en estado *Busy* y se genera el nuevo evento de finalización de un trabajo.

## Modelo de Simulación de Eventos Discretos desarrollado para resolver el problema

El problema se basa en el Modelo de los servidores conectados en paralelo. Cuando los clientes arriban son atendidos por los empleados que se encuentren disponibles, en caso de que no haya ninguno que esté libre para atenderlo, el cliente deberá pasar a la cola y esperar a que alguno termine su trabajo para ser atendido. Note que el trabajo de los empleados se realiza de forma "paralela".

Los eventos del modelo serían:
- *ClientArrival* : La llegada de un cliente al taller
- *WorkerFinished* : Un empleado terminó de atender a un cliente
  
Las variables del modelo sería las siguientes:
1. Variables de tiempo:
    - *current_time* - tiempo actual de la simulación
    - *max_time* - tiempo máximo que demora la simulación
    - *t* - tiempo generado de arribo del próximo cliente
    - *wt* - tiempo generado para la finalización de un trabajo por un empleado
2. Variables contadoras:
    - *client_count* - Cantidad de clientes que ha llegado al taller
    - *profit* - Suma de la ganancia obtenida por cada trabajo realizado
3. Variables de estado:
    - *timeline* - Lista que contiene los eventos del modelo en orden ascendente de tiempo
    - *q* - Instancia de la clase *Queue* que maneja la cola de clientes
    - *workers* - Lista de trabajadores del taller donde es posible concocer el estado de cada uno, el cliente con el que está trabajando, en caso de estar atendiendo a alguno, entre otros detalles.

## Consideraciones obtenidas a partir de la ejecución de las simulaciones del problema

Usted puede determinar la cantidad de simulaciones que desea realizar, así como la cantidad de horas de la jornada laboral. Igualmente puede cambiar con facilidad la cantidad de trabajadores de cada tipo. En este caso se asumieron 8 horas de jornada laboral y se trabajó con la cantidad de trabajadores indicados por el problema: 2 vendedores, 3 técnicos y 1 técnico especializado. Se llevaron a cabo 10000 simulaciones.

Se tuvo en cuenta además, a la hora de generar el nuevo arribo de un cliente, que si el tiempo de llegada superaba el tiempo máximo de la jornada laboral, este evento no era añadido. Sin embargo, es posible que queden clientes en el sistema, aún cuando ya se haya alcanzado el máximo de tiempo; estos clientes son atendidos, generando, en dichas ocasiones un *overtime*. Este indicador también se tuvo en cuenta durante la ejecución de las simulaciones.

A partir de lo mencionado anteriormente, se obtuvo una ganancia promedio de 6762, con aproximadamente 24 clientes al día. El tiempo que se tomó después de que terminara la jornada laboral rondaba los 3 minutos aproximadamente.

## El enlace al repositorio del proyecto en Github

Puede acceder al código de solución del problema a través de este [enlace](https://github.com/cicr99/Happy-Computing)