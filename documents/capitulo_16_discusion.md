# Capitulo 16. Discusion

## Prediccion del mercado electrico espanol mediante tecnicas de aprendizaje automatico

### 16.1. Interpretacion de resultados

Los resultados obtenidos muestran que el enfoque desarrollado es capaz de aprender patrones utiles del mercado electrico espanol. En los experimentos realizados, los modelos entrenados mejoraron de forma clara el baseline `lag 24`, lo que indica que la combinacion de variables de calendario, retardos, medias moviles, diferencias y ratios aporta informacion predictiva relevante.

En el entrenamiento con datos de enero a marzo de 2025, el mejor modelo fue Ridge, con un MAE de `10.02 EUR/MWh`, frente a `20.97 EUR/MWh` del baseline. En el entrenamiento con casi todo 2025, el mejor modelo fue HistGradientBoosting, con un MAE de `3.17 EUR/MWh`, frente a `24.91 EUR/MWh` del baseline. Esta diferencia evidencia que el sistema no se limita a repetir precios pasados, sino que aprovecha la estructura temporal de los datos.

La mejora al ampliar el rango temporal es especialmente significativa. El modelo anual dispone de mas ejemplos, mas variedad de situaciones y mas ciclos estacionales. Esto permite que el algoritmo capture mejor patrones recurrentes del mercado. Sin embargo, tambien debe interpretarse con prudencia: una buena metrica agregada no garantiza acierto en todos los casos concretos.

La inferencia para `2026-01-01 00:00` ilustra esta limitacion. El modelo predijo `94.20 EUR/MWh`, mientras que el valor real de OMIE fue `112.01 EUR/MWh`. El error absoluto fue `17.81 EUR/MWh`. Aunque el modelo habia mostrado buenas metricas en validacion, fallo de forma apreciable en un periodo concreto. Esto confirma que la prediccion de precios electricos combina patrones aprendibles con situaciones excepcionales dificiles de anticipar.

En conjunto, los resultados son positivos para el alcance del proyecto. Se ha construido una aplicacion funcional, reproducible y capaz de comparar varios modelos. No obstante, el sistema debe entenderse como una base academica y tecnica, no como una herramienta comercial de prediccion garantizada.

### 16.2. Influencia de la cantidad de datos historicos

La cantidad de datos historicos tuvo un impacto claro en el rendimiento. Con tres meses de datos, Ridge fue el mejor modelo. Con casi todo 2025, HistGradientBoosting obtuvo mejores resultados. Este cambio sugiere que los modelos no lineales necesitan mas ejemplos para aprovechar plenamente su capacidad.

Un conjunto pequeno puede favorecer modelos mas simples y regularizados. Ridge, al ser lineal y estar regularizado, puede generalizar bien cuando hay menos datos. En cambio, modelos mas flexibles como MLP o boosting pueden necesitar mas observaciones para aprender interacciones sin sobreajustar.

El uso de un ano completo tambien permite incorporar mas diversidad temporal: dias laborables, fines de semana, meses con distinta irradiacion solar, periodos de mayor y menor demanda y cambios de comportamiento estacional. Esta variedad ayuda al modelo a construir una representacion mas completa del mercado.

Sin embargo, mas datos no siempre implican automaticamente mejor prediccion. Si el mercado cambia estructuralmente, datos muy antiguos pueden dejar de ser representativos. Tambien pueden aparecer cambios regulatorios, variaciones de resolucion temporal o modificaciones en el mix de generacion. Por ello, en una aplicacion real seria conveniente reentrenar periodicamente y evaluar por ventanas temporales.

### 16.3. Impacto esperado de las variables renovables

La integracion opcional de ESIOS permite incorporar previsiones de generacion eolica, solar fotovoltaica y solar termica. Desde el punto de vista teorico, estas variables son muy relevantes. La generacion renovable tiene costes variables bajos y puede desplazar tecnologias mas caras, afectando directamente al precio marginal.

El modelo inicial, basado solo en OMIE, aprende patrones desde calendario e historico de precios. Esta aproximacion captura regularidades, pero no observa directamente las condiciones fisicas esperadas del sistema. Por ejemplo, dos dias con la misma hora y mismo mes pueden tener precios distintos si la prevision eolica o solar es muy diferente.

Las variables ESIOS permiten enriquecer el dataset con informacion exogena. `wind_forecast_mwh`, `solar_pv_forecast_mwh` y `solar_thermal_forecast_mwh` aportan contexto sobre la generacion renovable prevista. Las variables derivadas, como `renewable_forecast_mwh` y `wind_solar_ratio`, resumen cantidad y composicion renovable.

El impacto esperado es una mejora de precision, sobre todo en horas donde la renovable condiciona el precio. Sin embargo, su utilidad depende de la calidad de las previsiones, de la alineacion temporal y de que el modelo sea capaz de explotar esas variables. Tambien requiere disponer de token ESIOS y mantener los datos externos en inferencia.

### 16.4. Limitaciones del modelo sin variables externas

El modelo sin variables externas tiene una ventaja importante: es simple, reproducible y puede ejecutarse con datos publicos de OMIE. No requiere credenciales adicionales ni depende de APIs externas autenticadas. Esto lo convierte en una base solida para comenzar.

Su principal limitacion es que intenta explicar el precio solo a partir de su historia y del calendario. El mercado electrico, sin embargo, depende de muchos factores adicionales: demanda prevista, meteorologia, generacion renovable, disponibilidad nuclear e hidraulica, precios de gas, CO2, interconexiones y restricciones del sistema.

Cuando esos factores cambian bruscamente, el historico de precios puede no ser suficiente. Un ejemplo es un dia festivo, una ola de frio, una caida de viento o un pico de gas. El modelo puede detectar patrones pasados, pero no siempre anticipa causas externas que no estan presentes en sus variables.

Por ello, el modelo sin variables externas debe verse como una primera aproximacion. Es util para demostrar el pipeline, comparar algoritmos y obtener una referencia funcional, pero no agota el problema predictivo.

### 16.5. Limitaciones del modelo con variables ESIOS

El modelo con ESIOS mejora el planteamiento al incorporar prevision renovable. No obstante, tambien introduce nuevas limitaciones. La primera es la dependencia de un token de acceso. Si el usuario no dispone de token o la API no responde, el flujo enriquecido no puede ejecutarse.

La segunda limitacion es la alineacion temporal. OMIE puede tener datos horarios o cuarto-horarios, mientras que ESIOS se descarga con truncado horario. La aplicacion resuelve esto mediante una union hacia atras con tolerancia de una hora, pero sigue siendo una aproximacion. Una alineacion incorrecta puede reducir la utilidad de las variables externas.

La tercera limitacion es que ESIOS aporta solo una parte del contexto. Eolica y solar son importantes, pero no explican todo el precio. Para mejorar de forma mas completa seria necesario incorporar demanda prevista, meteorologia, tecnologias gestionables, gas, CO2 e interconexiones.

Finalmente, el modelo entrenado con ESIOS necesita disponer de esas mismas columnas en inferencia. Esto obliga a conservar el dataset enriquecido o descargar previsiones actualizadas. La coherencia entre entrenamiento e inferencia se vuelve mas exigente.

### 16.6. Riesgos de sobreajuste

El sobreajuste aparece cuando un modelo aprende demasiado bien las particularidades del entrenamiento y pierde capacidad para generalizar. En este proyecto, el riesgo existe porque se generan muchas variables a partir del historico de precios y se prueban modelos flexibles como MLP e HistGradientBoosting.

Se han aplicado varias medidas para reducir este riesgo. Ridge utiliza regularizacion. MLP emplea `alpha`, parada temprana y validacion interna. HistGradientBoosting incorpora regularizacion y parametros moderados. Ademas, la evaluacion se realiza sobre un tramo temporal posterior, no sobre los mismos datos de entrenamiento.

Aun asi, el riesgo no desaparece. Un buen resultado en un tramo de validacion puede depender de que ese tramo se parezca mucho al entrenamiento. Por ello, seria recomendable ampliar la evaluacion con backtesting mensual y ventanas deslizantes. Tambien convendria analizar la estabilidad del modelo en varios periodos.

El modo `auto` selecciona por MAE en validacion, lo cual es practico, pero puede elegir un modelo que se adapte especialmente bien a un tramo concreto. Una evaluacion mas robusta deberia comprobar si ese modelo mantiene su ventaja en otros tramos temporales.

### 16.7. Robustez del sistema ante datos ausentes

El sistema incorpora algunas medidas de robustez ante datos ausentes. En OMIE, si un dia falla durante un rango largo, el programa registra el fallo y continua si existen otros dias validos. Esto permitio entrenar con casi todo 2025 aunque faltaran los ficheros de `2025-10-30` y `2025-11-27`.

En ESIOS, el sistema valida que existan datos de generacion y que el token este disponible cuando se activa la opcion. Tras la union temporal, las columnas renovables se rellenan con `ffill` y `bfill`, lo que permite resolver pequenos huecos.

Tambien se gestionan ausentes generados por la ingenieria de variables. Los retardos y ventanas moviles producen `NaN` en las primeras filas, y estas observaciones se eliminan antes del entrenamiento. Esto asegura que los modelos reciban matrices completas.

La robustez actual es suficiente para un proyecto academico, pero puede ampliarse. Seria recomendable registrar de forma mas detallada los dias omitidos, generar informes de calidad de datos, medir cobertura ESIOS y avisar si existen huecos temporales largos. La calidad del dato es una parte esencial de la fiabilidad predictiva.
