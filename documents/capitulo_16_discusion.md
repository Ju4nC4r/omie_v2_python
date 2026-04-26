# Capítulo 16. Discusión

## Predicción del mercado eléctrico español mediante técnicas de aprendizaje automático

### 16.1. Interpretacion de resultados

Los resultados obtenidos muestran que el enfoque desarrollado es capaz de aprender patrones útiles del mercado eléctrico español. En los experimentos realizados, los modelos entrenados mejoraron de forma clara el baseline `lag 24`, lo que indica que la combinación de variables de calendario, retardos, medias móviles, diferencias y ratios aporta información predictiva relevante.

En el entrenamiento con datos de enero a marzo de 2025, el mejor modelo fue Ridge, con un MAE de `10.02 EUR/MWh`, frente a `20.97 EUR/MWh` del baseline. En el entrenamiento con casi todo 2025, el mejor modelo fue HistGradientBoosting, con un MAE de `3.17 EUR/MWh`, frente a `24.91 EUR/MWh` del baseline. Esta diferencia evidencia que el sistema no se limita a repetir precios pasados, sino que aprovecha la estructura temporal de los datos.

La mejora al ampliar el rango temporal es especialmente significativa. El modelo anual dispone de más ejemplos, más variedad de situaciones y más ciclos estacionales. Esto permite que el algoritmo capture mejor patrones recurrentes del mercado. Sin embargo, también debe interpretarse con prudencia: una buena métrica agregada no garantiza acierto en todos los casos concretos.

La inferencia para `2026-01-01 00:00` ilustra esta limitación. El modelo predijo `94.20 EUR/MWh`, mientras que el valor real de OMIE fue `112.01 EUR/MWh`. El error absoluto fue `17.81 EUR/MWh`. Aunque el modelo había mostrado buenas métricas en validación, fallo de forma apreciable en un periodo concreto. Esto confirma que la predicción de precios eléctricos combina patrones aprendibles con situaciones excepcionales difíciles de anticipar.

En conjunto, los resultados son positivos para el alcance del proyecto. Se ha construido una aplicación funcional, reproducible y capaz de comparar varios modelos. No obstante, el sistema debe entenderse como una base académica y técnica, no como una herramienta comercial de predicción garantizada.

### 16.2. Influencia de la cantidad de datos históricos

La cantidad de datos históricos tuvo un impacto claro en el rendimiento. Con tres meses de datos, Ridge fue el mejor modelo. Con casi todo 2025, HistGradientBoosting obtuvo mejores resultados. Este cambio sugiere que los modelos no lineales necesitan más ejemplos para aprovechar plenamente su capacidad.

Un conjunto pequeño puede favorecer modelos más simples y regularizados. Ridge, al ser lineal y estar regularizado, puede generalizar bien cuando hay menos datos. En cambio, modelos más flexibles como MLP o boosting pueden necesitar más observaciones para aprender interacciones sin sobreajustar.

El uso de un año completo también permite incorporar más diversidad temporal: días laborables, fines de semana, meses con distinta irradiación solar, periodos de mayor y menor demanda y cambios de comportamiento estacional. Esta variedad ayuda al modelo a construir una representación más completa del mercado.

Sin embargo, más datos no siempre implican automáticamente mejor predicción. Si el mercado cambia estructuralmente, datos muy antiguos pueden dejar de ser representativos. También pueden aparecer cambios regulatorios, variaciones de resolución temporal o modificaciones en el mix de generación. Por ello, en una aplicación real sería conveniente reentrenar periódicamente y evaluar por ventanas temporales.

### 16.3. Impacto esperado de las variables renovables

La integración opcional de ESIOS permite incorporar previsiones de generación eólica, solar fotovoltaica y solar térmica. Desde el punto de vista teórico, estas variables son muy relevantes. La generación renovable tiene costes variables bajos y puede desplazar tecnologías más caras, afectando directamente al precio marginal.

El modelo inicial, basado solo en OMIE, aprende patrones desde calendario e histórico de precios. Esta aproximación captura regularidades, pero no observa directamente las condiciones físicas esperadas del sistema. Por ejemplo, dos días con la misma hora y mismo mes pueden tener precios distintos si la previsión eólica o solar es muy diferente.

Las variables ESIOS permiten enriquecer el dataset con información exógena. `wind_forecast_mwh`, `solar_pv_forecast_mwh` y `solar_thermal_forecast_mwh` aportan contexto sobre la generación renovable prevista. Las variables derivadas, como `renewable_forecast_mwh` y `wind_solar_ratio`, resumen cantidad y composición renovable.

El impacto esperado es una mejora de precisión, sobre todo en horas donde la renovable condiciona el precio. Sin embargo, su utilidad depende de la calidad de las previsiones, de la alineación temporal y de que el modelo sea capaz de explotar esas variables. También requiere disponer de token ESIOS y mantener los datos externos en inferencia.

### 16.4. Limitaciones del modelo sin variables externas

El modelo sin variables externas tiene una ventaja importante: es simple, reproducible y puede ejecutarse con datos públicos de OMIE. No requiere credenciales adicionales ni depende de APIs externas autenticadas. Esto lo convierte en una base sólida para comenzar.

Su principal limitación es que intenta explicar el precio solo a partir de su historia y del calendario. El mercado eléctrico, sin embargo, depende de muchos factores adicionales: demanda prevista, meteorología, generación renovable, disponibilidad nuclear e hidráulica, precios de gas, CO2, interconexiones y restricciones del sistema.

Cuando esos factores cambian bruscamente, el histórico de precios puede no ser suficiente. Un ejemplo es un día festivo, una ola de frío, una caída de viento o un pico de gas. El modelo puede detectar patrones pasados, pero no siempre anticipa causas externas que no están presentes en sus variables.

Por ello, el modelo sin variables externas debe verse como una primera aproximación. Es útil para demostrar el pipeline, comparar algoritmos y obtener una referencia funcional, pero no agota el problema predictivo.

### 16.5. Limitaciones del modelo con variables ESIOS

El modelo con ESIOS mejora el planteamiento al incorporar previsión renovable. No obstante, también introduce nuevas limitaciones. La primera es la dependencia de un token de acceso. Si el usuario no dispone de token o la API no responde, el flujo enriquecido no puede ejecutarse.

La segunda limitación es la alineación temporal. OMIE puede tener datos horarios o cuarto-horarios, mientras que ESIOS se descarga con truncado horario. La aplicación resuelve esto mediante una unión hacia atrás con tolerancia de una hora, pero sigue siendo una aproximación. Una alineación incorrecta puede reducir la utilidad de las variables externas.

La tercera limitación es que ESIOS aporta solo una parte del contexto. Eólica y solar son importantes, pero no explican todo el precio. Para mejorar de forma más completa sería necesario incorporar demanda prevista, meteorología, tecnologías gestionables, gas, CO2 e interconexiones.

Finalmente, el modelo entrenado con ESIOS necesita disponer de esas mismas columnas en inferencia. Esto obliga a conservar el dataset enriquecido o descargar previsiones actualizadas. La coherencia entre entrenamiento e inferencia se vuelve más exigente.

### 16.6. Riesgos de sobreajuste

El sobreajuste aparece cuando un modelo aprende demasiado bien las particularidades del entrenamiento y pierde capacidad para generalizar. En este proyecto, el riesgo existe porque se generan muchas variables a partir del histórico de precios y se prueban modelos flexibles como MLP e HistGradientBoosting.

Se han aplicado varias medidas para reducir este riesgo. Ridge utiliza regularización. MLP emplea `alpha`, parada temprana y validación interna. HistGradientBoosting incorpora regularización y parámetros moderados. Además, la evaluación se realiza sobre un tramo temporal posterior, no sobre los mismos datos de entrenamiento.

Aun así, el riesgo no desaparece. Un buen resultado en un tramo de validación puede depender de que ese tramo se parezca mucho al entrenamiento. Por ello, sería recomendable ampliar la evaluación con backtesting mensual y ventanas deslizantes. También convendria analizar la estabilidad del modelo en varios periodos.

El modo `auto` selecciona por MAE en validación, lo cual es práctico, pero puede elegir un modelo que se adapte especialmente bien a un tramo concreto. Una evaluación más robusta debería comprobar si ese modelo mantiene su ventaja en otros tramos temporales.

### 16.7. Robustez del sistema ante datos ausentes

El sistema incorpora algunas medidas de robustez ante datos ausentes. En OMIE, si un día falla durante un rango largo, el programa registra el fallo y continúa si existen otros días válidos. Esto permitió entrenar con casi todo 2025 aunque faltaran los ficheros de `2025-10-30` y `2025-11-27`.

En ESIOS, el sistema valida que existan datos de generación y que el token este disponible cuando se activa la opción. Tras la unión temporal, las columnas renovables se rellenan con `ffill` y `bfill`, lo que permite resolver pequeños huecos.

También se gestionan ausentes generados por la ingeniería de variables. Los retardos y ventanas móviles producen `NaN` en las primeras filas, y estas observaciones se eliminan antes del entrenamiento. Esto asegura que los modelos reciban matrices completas.

La robustez actual es suficiente para un proyecto académico, pero puede ampliarse. Sería recomendable registrar de forma más detallada los días omitidos, generar informes de calidad de datos, medir cobertura ESIOS y avisar si existen huecos temporales largos. La calidad del dato es una parte esencial de la fiabilidad predictiva.
