# Capítulo 15. Resultados experimentales

## Predicción del mercado eléctrico español mediante técnicas de aprendizaje automático

### 15.1. Entrenamiento con datos de enero a marzo de 2025

El primer experimento documentado se realizó con datos comprendidos entre el 1 de enero de 2025 y el 31 de marzo de 2025. Este periodo permite realizar una prueba inicial con varios meses de información, suficiente para construir retardos, medias móviles y validación temporal, pero todavía relativamente pequeño en comparación con un año completo.

El comando utilizado fue:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model auto
```

Se utilizó el modo `auto`, por lo que el sistema entrenó los modelos candidatos disponibles y seleccionó el mejor según MAE en el tramo de validación. En este experimento, el mejor modelo fue `ridge`.

Los resultados obtenidos fueron:

```text
Mejor modelo: ridge
MAE: 10.02 EUR/MWh
RMSE: 15.70 EUR/MWh
R2: 0.871
Baseline lag 24 MAE: 20.97 EUR/MWh
```

El MAE de `10.02 EUR/MWh` indica que, de media, el modelo cometió un error absoluto de unos diez euros por megavatio hora en el tramo de validación. El RMSE fue superior, `15.70 EUR/MWh`, lo que sugiere la existencia de algunos errores más grandes que aumentan la penalización cuadrática. El R2 de `0.871` indica que el modelo explica una parte elevada de la variabilidad observada en el periodo de validación.

La comparación con el baseline es especialmente relevante. El baseline `lag 24` obtuvo un MAE de `20.97 EUR/MWh`, más del doble que el modelo Ridge. Esto muestra que el modelo de aprendizaje automático aporta valor respecto a una regla simple basada en el precio de 24 periodos antes.

La comparación entre candidatos fue:

```text
ridge: MAE 10.02
mlp: MAE 13.70
hist_gradient_boosting: MAE 10.23
```

Estos resultados muestran que, para este rango temporal, Ridge fue ligeramente mejor que HistGradientBoosting y claramente mejor que MLP. La diferencia entre Ridge y boosting fue pequeña, lo que sugiere que las variables construidas ya capturaban buena parte del comportamiento mediante relaciones relativamente estables. La red neuronal, en cambio, no fue la mejor opción para este periodo concreto.

Este experimento cumple una función inicial: validar que el pipeline completo funciona y que los modelos superan una referencia sencilla. También muestra que un modelo más complejo no siempre obtiene mejores resultados. La selección debe hacerse mediante evaluación, no por intuición.

### 15.2. Entrenamiento con datos de todo 2025

El segundo experimento amplio se realizó usando datos desde el 1 de enero de 2025 hasta el 31 de diciembre de 2025. El objetivo era comprobar como cambia el rendimiento al aumentar el histórico disponible. Un año completo permite incluir más estacionalidad, mayor variedad de situaciones de mercado y más ejemplos para entrenamiento.

El comando utilizado fue:

```bash
omie-price-train --start 2025-01-01 --end 2025-12-31 --model auto
```

Durante la descarga se detecto que OMIE no devolvio datos para dos fechas concretas del rango consultado:

```text
2025-10-30
2025-11-27
```

El programa registro estos fallos y continuó con el resto de días disponibles. Este comportamiento confirma la utilidad de la gestión de errores por día: un rango largo puede seguir siendo útil aunque existan ausencias puntuales.

Los resultados del entrenamiento fueron:

```text
Mejor modelo: hist_gradient_boosting
MAE: 3.17 EUR/MWh
RMSE: 4.59 EUR/MWh
R2: 0.973
Baseline lag 24 MAE: 24.91 EUR/MWh
```

El resultado muestra una mejora muy notable frente al experimento de enero a marzo. El MAE baja de `10.02` a `3.17 EUR/MWh`, el RMSE baja de `15.70` a `4.59 EUR/MWh`, y el R2 sube de `0.871` a `0.973`. Esto indica que el modelo entrenado con más datos captura mejor los patrones del mercado en el tramo de validación utilizado.

La comparación entre candidatos fue:

```text
ridge: MAE 4.10
mlp: MAE 3.98
hist_gradient_boosting: MAE 3.17
```

En este caso, HistGradientBoosting fue el mejor modelo. Ridge y MLP obtuvieron resultados razonables, pero el modelo basado en boosting redujo más el error. Esto es coherente con la capacidad de los árboles secuenciales para capturar relaciones no lineales e interacciones entre variables tabulares.

La diferencia frente al baseline es muy amplia. Mientras el baseline `lag 24` tuvo un MAE de `24.91 EUR/MWh`, el mejor modelo obtuvo `3.17 EUR/MWh`. Esto indica que el modelo no se limita a repetir un precio anterior, sino que aprovecha las variables construidas para mejorar la predicción.

No obstante, el resultado debe interpretarse con prudencia. Una métrica muy buena en un tramo de validación no garantiza que el modelo acierte todos los días futuros. El mercado puede cambiar y existen situaciones específicas, como festivos o eventos extremos, que pueden producir errores significativos.

### 15.3. Comparación entre `ridge`, `mlp` y `hist_gradient_boosting`

Los experimentos realizados permiten comparar tres familias de modelos. `ridge` representa un modelo lineal regularizado. `mlp` representa una red neuronal multicapa. `hist_gradient_boosting` representa un modelo no lineal basado en árboles de decisión entrenados de forma secuencial.

En el experimento de enero a marzo de 2025, los resultados fueron:

| Modelo | MAE |
| --- | ---: |
| `ridge` | 10.02 |
| `mlp` | 13.70 |
| `hist_gradient_boosting` | 10.23 |

En este primer caso, `ridge` fue el mejor por un margen pequeño respecto a `hist_gradient_boosting`. La red neuronal quedó por detrás. Esto puede deberse a que el periodo era relativamente corto, por lo que un modelo lineal regularizado generalizó mejor que alternativas más flexibles.

En el experimento con casi todo 2025, los resultados fueron:

| Modelo | MAE |
| --- | ---: |
| `ridge` | 4.10 |
| `mlp` | 3.98 |
| `hist_gradient_boosting` | 3.17 |

Con más datos, `hist_gradient_boosting` paso a ser el mejor modelo. La red neuronal también mejoró y quedó por encima de Ridge, aunque sin alcanzar el rendimiento del boosting. Esto sugiere que los modelos no lineales pueden beneficiarse más de conjuntos de datos amplios, siempre que la validación sea adecuada.

La comparación evidencia que no existe un ganador universal. El mejor modelo depende del rango temporal, de la cantidad de datos, de la estructura de variables y de las condiciones del mercado. Por eso la aplicación permite selección manual y modo automático.

Desde una perspectiva práctica, Ridge es atractivo por su rapidez y estabilidad. MLP es interésante porque representa un enfoque neuronal, aunque requiere más cuidado. HistGradientBoosting ofrece muy buen rendimiento en datos tabulares y se muestra especialmente competitivo cuando hay suficiente histórico.

### 15.4. Resultados del modo `auto`

El modo `auto` fue utilizado en los dos experimentos principales. Su función es entrenar los tres modelos candidatos, evaluarlos sobre el mismo tramo temporal y guardar el que obtiene menor MAE. Esto evita elegir manualmente un modelo sin evidencia previa.

En enero-marzo de 2025, `auto` seleccionó `ridge`. En casi todo 2025, `auto` seleccionó `hist_gradient_boosting`. Este comportamiento es deseable, porque demuestra que el sistema no fuerza siempre el mismo algoritmo. La selección cambia según los resultados obtenidos con los datos disponibles.

El modo `auto` aporta comodidad y rigor. Comodidad porque el usuario no necesita ejecutar tres comandos separados para comparar modelos. Rigor porque todos los modelos se entrenan y validan bajo las mismas condiciones, con el mismo dataset y la misma división temporal.

La selección por MAE es adecuada porque esta métrica se interpreta directamente en EUR/MWh. Un MAE menor significa que, en promedio, el modelo se equivoca menos en unidades económicas comprensibles. Aunque RMSE y R2 también son útiles, MAE resulta especialmente claro para decidir entre modelos.

La principal desventaja del modo `auto` es el tiempo de ejecución. Entrenar tres modelos tarda más que entrenar uno solo. En la interfaz gráfica, este inconveniente se mitiga mostrando logs y progreso. En consola, el usuario puede ver los mensajes de entrenamiento y las métricas al finalizar.

En una futura ampliación, el modo `auto` podría incorporar más modelos, búsqueda de hiperparámetros o evaluación por varios tramos temporales. Sin embargo, incluso en su versión actual, cumple una función muy valiosa: convertir la comparación de modelos en parte natural del flujo de trabajo.

### 15.5. Comparación con baseline `lag 24`

El baseline `lag 24` es una referencia sencilla que predice usando el precio de 24 periodos antes. Su objetivo no es ser un modelo sofisticado, sino proporcionar un punto de comparación minimo. Un modelo de machine learning debe mejorar esta regla simple para justificar su usó.

En el experimento de enero a marzo de 2025, el baseline obtuvo:

```text
Baseline lag 24 MAE: 20.97 EUR/MWh
```

El mejor modelo, Ridge, obtuvo:

```text
MAE: 10.02 EUR/MWh
```

La mejora es clara. El modelo reduce aproximadamente a la mitad el error absoluto medio del baseline. Esto indica que las variables de calendario, retardos múltiples, medias móviles, desviaciones, diferencias y ratios aportan información adicional frente a usar solo un precio anterior.

En el experimento con casi todo 2025, el baseline obtuvo:

```text
Baseline lag 24 MAE: 24.91 EUR/MWh
```

El mejor modelo, HistGradientBoosting, obtuvo:

```text
MAE: 3.17 EUR/MWh
```

La diferencia en este segundo caso es aún mayor. El baseline queda muy lejos del modelo entrenado. Este resultado confirma que la aproximación de aprendizaje automático aprovecha mejor el histórico que una regla fija.

No obstante, debe tenerse en cuenta una limitación: `lag 24` no siempre representa exactamente el mismo concepto si la resolución cambia. En datos horarios, equivale aproximadamente al mismo periodo del día anterior. En datos cuarto-horarios, equivale a seis horas antes. Por tanto, en futuras versiones sería conveniente definir baselines por duración temporal real, como 24 horas, en lugar de por número fijo de filas.

### 15.6. Análisis del error en predicciones concretas

Además de las métricas agregadas, se analizo una predicción concreta. Este tipo de análisis es importante porque permite entender situaciones particulares en las que el modelo puede fallar. Una métrica promedio puede ser buena y, aun así, existir errores relevantes en días especiales.

Tras entrenar con datos de 2025, se generó una predicción para el primer periodo posterior disponible:

```text
Predicción para 2026-01-01 00:00:00: 94.20 EUR/MWh
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

El signo negativo indica que el modelo infraestimo el precio real. Es decir, predijo un precio inferior al publicado por OMIE. El error absoluto fue relevante, aunque no invalida necesariamente el comportamiento global del modelo. Este caso muestra que existen periodos concretos difíciles de anticipar.

El 1 de enero es un día especial. Al tratarse de un festivo, los patrones de demanda pueden diferir de un día laborable normal. Si el modelo no incorpora una variable explícita de festivos, debe intentar deducir ese comportamiento solo desde calendario general e histórico de precios. Esto puede no ser suficiente.

También pueden influir variables no incluidas, como demanda prevista, meteorología, disponibilidad de generación, precios de gas, CO2, interconexiones o información intradiaria. Este análisis permite orientar mejoras futuras.

### 15.7. Caso práctico: predicción para `2026-01-01 00:00`

El caso de `2026-01-01 00:00` es especialmente útil como ejemplo práctico porque representa una predicción fuera del periodo de entrenamiento de 2025. No es una observación interna usada para ajustar el modelo, sino un periodo posterior sobre el que se realiza inferencia.

La predicción obtenida fue:

```text
94.20 EUR/MWh
```

El valor real fue:

```text
112.01 EUR/MWh
```

La diferencia muestra que el modelo estaba capturando una tendencia general, pero no alcanzó el nivel real del precio para esa hora concreta. En términos prácticos, un usuario que hubiera utilizado esa predicción habría esperado un precio más bajo del que finalmente se publicó.

Este caso también permite discutir la importancia de la validación externa. Un modelo puede tener buen R2 y bajo MAE en validación, pero la verdadera prueba es su comportamiento ante nuevos datos futuros. Por eso es recomendable seguir acumulando predicciones y compararlas posteriormente con valores reales.

La aplicación facilita este flujo porque puede generar inferencias y, una vez publicados los datos OMIE, comparar manualmente el resultado. En una futura versión podría automatizarse esta comparación, creando un registro histórico de predicciones y valores reales.

### 15.8. Comparación con el valor real publicado por OMIE

La comparación con OMIE es el cierre natural del experimento. OMIE actua como fuente oficial del valor real, por lo que permite medir el error de la inferencia. Esta comparación convierte la predicción en un resultado verificable.

En el caso estudiado, la predicción fue inferior al valor real. El error absoluto de `17.81 EUR/MWh` muestra que el modelo no capturo completamente las condiciones de mercado de ese periodo. Al mismo tiempo, el error relativo del `15.90 %` ofrece una interpretación proporcional del fallo.

Este resultado no debe interpretarse como fracaso global, sino como evidencia de limitaciones. El modelo entrenado era intencionadamente pequeño y basado principalmente en calendario, ciclos y retardos. Aunque posteriormente se añadió soporte para ESIOS, una predicción concreta puede requerir variables adicionales para mejorar.

Las principales líneas de mejora derivadas de esta comparación son: incorporar festivos, demanda prevista, meteorología, generación renovable prevista completa, disponibilidad de tecnologías, precios de gas, derechos de CO2 e interconexiones. También sería conveniente realizar backtesting mensual y evaluar errores por hora, día de la semana y régimen de precios.

En conjunto, los resultados experimentales muestran que la aplicación funciona, que los modelos superan claramente al baseline en los experimentos agregados y que el aumento de datos mejora el rendimiento. También muestran que la inferencia real puede presentar errores relevantes en casos concretos. Esta combinación de aciertos y limitaciones es valiosa para un TFG, porque permite presentar conclusiones equilibradas y justificar líneas futuras de trabajo.
