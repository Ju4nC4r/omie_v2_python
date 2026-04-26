# Capitulo 15. Resultados experimentales

## Prediccion del mercado electrico espanol mediante tecnicas de aprendizaje automatico

### 15.1. Entrenamiento con datos de enero a marzo de 2025

El primer experimento documentado se realizo con datos comprendidos entre el 1 de enero de 2025 y el 31 de marzo de 2025. Este periodo permite realizar una prueba inicial con varios meses de informacion, suficiente para construir retardos, medias moviles y validacion temporal, pero todavia relativamente pequeno en comparacion con un ano completo.

El comando utilizado fue:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model auto
```

Se utilizo el modo `auto`, por lo que el sistema entreno los modelos candidatos disponibles y selecciono el mejor segun MAE en el tramo de validacion. En este experimento, el mejor modelo fue `ridge`.

Los resultados obtenidos fueron:

```text
Mejor modelo: ridge
MAE: 10.02 EUR/MWh
RMSE: 15.70 EUR/MWh
R2: 0.871
Baseline lag 24 MAE: 20.97 EUR/MWh
```

El MAE de `10.02 EUR/MWh` indica que, de media, el modelo cometio un error absoluto de unos diez euros por megavatio hora en el tramo de validacion. El RMSE fue superior, `15.70 EUR/MWh`, lo que sugiere la existencia de algunos errores mas grandes que aumentan la penalizacion cuadratica. El R2 de `0.871` indica que el modelo explica una parte elevada de la variabilidad observada en el periodo de validacion.

La comparacion con el baseline es especialmente relevante. El baseline `lag 24` obtuvo un MAE de `20.97 EUR/MWh`, mas del doble que el modelo Ridge. Esto muestra que el modelo de aprendizaje automatico aporta valor respecto a una regla simple basada en el precio de 24 periodos antes.

La comparacion entre candidatos fue:

```text
ridge: MAE 10.02
mlp: MAE 13.70
hist_gradient_boosting: MAE 10.23
```

Estos resultados muestran que, para este rango temporal, Ridge fue ligeramente mejor que HistGradientBoosting y claramente mejor que MLP. La diferencia entre Ridge y boosting fue pequena, lo que sugiere que las variables construidas ya capturaban buena parte del comportamiento mediante relaciones relativamente estables. La red neuronal, en cambio, no fue la mejor opcion para este periodo concreto.

Este experimento cumple una funcion inicial: validar que el pipeline completo funciona y que los modelos superan una referencia sencilla. Tambien muestra que un modelo mas complejo no siempre obtiene mejores resultados. La seleccion debe hacerse mediante evaluacion, no por intuicion.

### 15.2. Entrenamiento con datos de todo 2025

El segundo experimento amplio se realizo usando datos desde el 1 de enero de 2025 hasta el 31 de diciembre de 2025. El objetivo era comprobar como cambia el rendimiento al aumentar el historico disponible. Un ano completo permite incluir mas estacionalidad, mayor variedad de situaciones de mercado y mas ejemplos para entrenamiento.

El comando utilizado fue:

```bash
omie-price-train --start 2025-01-01 --end 2025-12-31 --model auto
```

Durante la descarga se detecto que OMIE no devolvio datos para dos fechas concretas del rango consultado:

```text
2025-10-30
2025-11-27
```

El programa registro estos fallos y continuo con el resto de dias disponibles. Este comportamiento confirma la utilidad de la gestion de errores por dia: un rango largo puede seguir siendo util aunque existan ausencias puntuales.

Los resultados del entrenamiento fueron:

```text
Mejor modelo: hist_gradient_boosting
MAE: 3.17 EUR/MWh
RMSE: 4.59 EUR/MWh
R2: 0.973
Baseline lag 24 MAE: 24.91 EUR/MWh
```

El resultado muestra una mejora muy notable frente al experimento de enero a marzo. El MAE baja de `10.02` a `3.17 EUR/MWh`, el RMSE baja de `15.70` a `4.59 EUR/MWh`, y el R2 sube de `0.871` a `0.973`. Esto indica que el modelo entrenado con mas datos captura mejor los patrones del mercado en el tramo de validacion utilizado.

La comparacion entre candidatos fue:

```text
ridge: MAE 4.10
mlp: MAE 3.98
hist_gradient_boosting: MAE 3.17
```

En este caso, HistGradientBoosting fue el mejor modelo. Ridge y MLP obtuvieron resultados razonables, pero el modelo basado en boosting redujo mas el error. Esto es coherente con la capacidad de los arboles secuenciales para capturar relaciones no lineales e interacciones entre variables tabulares.

La diferencia frente al baseline es muy amplia. Mientras el baseline `lag 24` tuvo un MAE de `24.91 EUR/MWh`, el mejor modelo obtuvo `3.17 EUR/MWh`. Esto indica que el modelo no se limita a repetir un precio anterior, sino que aprovecha las variables construidas para mejorar la prediccion.

No obstante, el resultado debe interpretarse con prudencia. Una metrica muy buena en un tramo de validacion no garantiza que el modelo acierte todos los dias futuros. El mercado puede cambiar y existen situaciones especificas, como festivos o eventos extremos, que pueden producir errores significativos.

### 15.3. Comparacion entre `ridge`, `mlp` y `hist_gradient_boosting`

Los experimentos realizados permiten comparar tres familias de modelos. `ridge` representa un modelo lineal regularizado. `mlp` representa una red neuronal multicapa. `hist_gradient_boosting` representa un modelo no lineal basado en arboles de decision entrenados de forma secuencial.

En el experimento de enero a marzo de 2025, los resultados fueron:

| Modelo | MAE |
| --- | ---: |
| `ridge` | 10.02 |
| `mlp` | 13.70 |
| `hist_gradient_boosting` | 10.23 |

En este primer caso, `ridge` fue el mejor por un margen pequeno respecto a `hist_gradient_boosting`. La red neuronal quedo por detras. Esto puede deberse a que el periodo era relativamente corto, por lo que un modelo lineal regularizado generalizo mejor que alternativas mas flexibles.

En el experimento con casi todo 2025, los resultados fueron:

| Modelo | MAE |
| --- | ---: |
| `ridge` | 4.10 |
| `mlp` | 3.98 |
| `hist_gradient_boosting` | 3.17 |

Con mas datos, `hist_gradient_boosting` paso a ser el mejor modelo. La red neuronal tambien mejoro y quedo por encima de Ridge, aunque sin alcanzar el rendimiento del boosting. Esto sugiere que los modelos no lineales pueden beneficiarse mas de conjuntos de datos amplios, siempre que la validacion sea adecuada.

La comparacion evidencia que no existe un ganador universal. El mejor modelo depende del rango temporal, de la cantidad de datos, de la estructura de variables y de las condiciones del mercado. Por eso la aplicacion permite seleccion manual y modo automatico.

Desde una perspectiva practica, Ridge es atractivo por su rapidez y estabilidad. MLP es interesante porque representa un enfoque neuronal, aunque requiere mas cuidado. HistGradientBoosting ofrece muy buen rendimiento en datos tabulares y se muestra especialmente competitivo cuando hay suficiente historico.

### 15.4. Resultados del modo `auto`

El modo `auto` fue utilizado en los dos experimentos principales. Su funcion es entrenar los tres modelos candidatos, evaluarlos sobre el mismo tramo temporal y guardar el que obtiene menor MAE. Esto evita elegir manualmente un modelo sin evidencia previa.

En enero-marzo de 2025, `auto` selecciono `ridge`. En casi todo 2025, `auto` selecciono `hist_gradient_boosting`. Este comportamiento es deseable, porque demuestra que el sistema no fuerza siempre el mismo algoritmo. La seleccion cambia segun los resultados obtenidos con los datos disponibles.

El modo `auto` aporta comodidad y rigor. Comodidad porque el usuario no necesita ejecutar tres comandos separados para comparar modelos. Rigor porque todos los modelos se entrenan y validan bajo las mismas condiciones, con el mismo dataset y la misma division temporal.

La seleccion por MAE es adecuada porque esta metrica se interpreta directamente en EUR/MWh. Un MAE menor significa que, en promedio, el modelo se equivoca menos en unidades economicas comprensibles. Aunque RMSE y R2 tambien son utiles, MAE resulta especialmente claro para decidir entre modelos.

La principal desventaja del modo `auto` es el tiempo de ejecucion. Entrenar tres modelos tarda mas que entrenar uno solo. En la interfaz grafica, este inconveniente se mitiga mostrando logs y progreso. En consola, el usuario puede ver los mensajes de entrenamiento y las metricas al finalizar.

En una futura ampliacion, el modo `auto` podria incorporar mas modelos, busqueda de hiperparametros o evaluacion por varios tramos temporales. Sin embargo, incluso en su version actual, cumple una funcion muy valiosa: convertir la comparacion de modelos en parte natural del flujo de trabajo.

### 15.5. Comparacion con baseline `lag 24`

El baseline `lag 24` es una referencia sencilla que predice usando el precio de 24 periodos antes. Su objetivo no es ser un modelo sofisticado, sino proporcionar un punto de comparacion minimo. Un modelo de machine learning debe mejorar esta regla simple para justificar su uso.

En el experimento de enero a marzo de 2025, el baseline obtuvo:

```text
Baseline lag 24 MAE: 20.97 EUR/MWh
```

El mejor modelo, Ridge, obtuvo:

```text
MAE: 10.02 EUR/MWh
```

La mejora es clara. El modelo reduce aproximadamente a la mitad el error absoluto medio del baseline. Esto indica que las variables de calendario, retardos multiples, medias moviles, desviaciones, diferencias y ratios aportan informacion adicional frente a usar solo un precio anterior.

En el experimento con casi todo 2025, el baseline obtuvo:

```text
Baseline lag 24 MAE: 24.91 EUR/MWh
```

El mejor modelo, HistGradientBoosting, obtuvo:

```text
MAE: 3.17 EUR/MWh
```

La diferencia en este segundo caso es aun mayor. El baseline queda muy lejos del modelo entrenado. Este resultado confirma que la aproximacion de aprendizaje automatico aprovecha mejor el historico que una regla fija.

No obstante, debe tenerse en cuenta una limitacion: `lag 24` no siempre representa exactamente el mismo concepto si la resolucion cambia. En datos horarios, equivale aproximadamente al mismo periodo del dia anterior. En datos cuarto-horarios, equivale a seis horas antes. Por tanto, en futuras versiones seria conveniente definir baselines por duracion temporal real, como 24 horas, en lugar de por numero fijo de filas.

### 15.6. Analisis del error en predicciones concretas

Ademas de las metricas agregadas, se analizo una prediccion concreta. Este tipo de analisis es importante porque permite entender situaciones particulares en las que el modelo puede fallar. Una metrica promedio puede ser buena y, aun asi, existir errores relevantes en dias especiales.

Tras entrenar con datos de 2025, se genero una prediccion para el primer periodo posterior disponible:

```text
Prediccion para 2026-01-01 00:00:00: 94.20 EUR/MWh
```

Posteriormente se comparo con el valor real publicado por OMIE:

```text
Valor real OMIE: 112.01 EUR/MWh
```

El error fue:

```text
Error: -17.81 EUR/MWh
Error absoluto: 17.81 EUR/MWh
Error relativo: 15.90%
```

El signo negativo indica que el modelo infraestimo el precio real. Es decir, predijo un precio inferior al publicado por OMIE. El error absoluto fue relevante, aunque no invalida necesariamente el comportamiento global del modelo. Este caso muestra que existen periodos concretos dificiles de anticipar.

El 1 de enero es un dia especial. Al tratarse de un festivo, los patrones de demanda pueden diferir de un dia laborable normal. Si el modelo no incorpora una variable explicita de festivos, debe intentar deducir ese comportamiento solo desde calendario general e historico de precios. Esto puede no ser suficiente.

Tambien pueden influir variables no incluidas, como demanda prevista, meteorologia, disponibilidad de generacion, precios de gas, CO2, interconexiones o informacion intradiaria. Este analisis permite orientar mejoras futuras.

### 15.7. Caso practico: prediccion para `2026-01-01 00:00`

El caso de `2026-01-01 00:00` es especialmente util como ejemplo practico porque representa una prediccion fuera del periodo de entrenamiento de 2025. No es una observacion interna usada para ajustar el modelo, sino un periodo posterior sobre el que se realiza inferencia.

La prediccion obtenida fue:

```text
94.20 EUR/MWh
```

El valor real fue:

```text
112.01 EUR/MWh
```

La diferencia muestra que el modelo estaba capturando una tendencia general, pero no alcanzo el nivel real del precio para esa hora concreta. En terminos practicos, un usuario que hubiera utilizado esa prediccion habria esperado un precio mas bajo del que finalmente se publico.

Este caso tambien permite discutir la importancia de la validacion externa. Un modelo puede tener buen R2 y bajo MAE en validacion, pero la verdadera prueba es su comportamiento ante nuevos datos futuros. Por eso es recomendable seguir acumulando predicciones y compararlas posteriormente con valores reales.

La aplicacion facilita este flujo porque puede generar inferencias y, una vez publicados los datos OMIE, comparar manualmente el resultado. En una futura version podria automatizarse esta comparacion, creando un registro historico de predicciones y valores reales.

### 15.8. Comparacion con el valor real publicado por OMIE

La comparacion con OMIE es el cierre natural del experimento. OMIE actua como fuente oficial del valor real, por lo que permite medir el error de la inferencia. Esta comparacion convierte la prediccion en un resultado verificable.

En el caso estudiado, la prediccion fue inferior al valor real. El error absoluto de `17.81 EUR/MWh` muestra que el modelo no capturo completamente las condiciones de mercado de ese periodo. Al mismo tiempo, el error relativo del `15.90 %` ofrece una interpretacion proporcional del fallo.

Este resultado no debe interpretarse como fracaso global, sino como evidencia de limitaciones. El modelo entrenado era intencionadamente pequeno y basado principalmente en calendario, ciclos y retardos. Aunque posteriormente se anadio soporte para ESIOS, una prediccion concreta puede requerir variables adicionales para mejorar.

Las principales lineas de mejora derivadas de esta comparacion son: incorporar festivos, demanda prevista, meteorologia, generacion renovable prevista completa, disponibilidad de tecnologias, precios de gas, derechos de CO2 e interconexiones. Tambien seria conveniente realizar backtesting mensual y evaluar errores por hora, dia de la semana y regimen de precios.

En conjunto, los resultados experimentales muestran que la aplicacion funciona, que los modelos superan claramente al baseline en los experimentos agregados y que el aumento de datos mejora el rendimiento. Tambien muestran que la inferencia real puede presentar errores relevantes en casos concretos. Esta combinacion de aciertos y limitaciones es valiosa para un TFG, porque permite presentar conclusiones equilibradas y justificar lineas futuras de trabajo.
