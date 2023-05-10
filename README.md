# mqtt
1. "broker.py"
    Se encarga de gestionar las publicaciones y subscripciones de los distintos
    elementos que se conectan.
    Los usuarios que se conectan, pueden enviar y recibir mensajes en el topic
    clients.
2. "numbers.py"
    Se publican constantemente numeros enteros y reales. El códgio realiza tareas
    con los números leídos (separar enteros y reales y calcular la suma, ser primo
    o no...)
3. "temperature.py"
    Puede haber varios sensores emitiendo valores, lo que vamos a hacer es leer
    los subtopics y dado un intervalo de tiempo (entre cuatro y ocho segundos),
    se calcule la temperatura máxima, mínima y media para cada sensor y en total.
4. "temperature_humidity.py".
    Se elige un termómetro concreto al que escuchar (uno de los que publican en 
    temperature). La misión es escuchar un termómetro, y si su valor supera la 
    temperatura K_0 = 20 entonces pasa a escuchar también humidity. Si la 
    temperatura baja de K_0 o el valor humidity sube de K_1 = 80 entonces
    el cliente deja de escuchar en el topic humidity.
5. "temporitzador.py"
    El cliente lee mensajes en los que se indican el tiempo de espera, el topic y 
    el mensaje a publicar una vez pasado el tiempo de espera. El cliente tendrá
    que encargarse de esperar el tiempo adecuado y luego publicar el mensaje en
    el topic correspondiente.
