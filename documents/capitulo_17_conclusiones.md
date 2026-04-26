# Capitulo 17. Conclusiones

## Prediccion del mercado electrico espanol mediante tecnicas de aprendizaje automatico

### 17.1. Cumplimiento de objetivos

El objetivo principal del trabajo era desarrollar una aplicacion capaz de predecir el precio del mercado electrico espanol mediante tecnicas de aprendizaje automatico, utilizando datos publicos de OMIE y, opcionalmente, variables renovables de ESIOS. Este objetivo se ha cumplido.

Se ha creado un proyecto Python funcional, con entorno virtual, estructura modular, comandos de consola e interfaz grafica. La aplicacion descarga datos OMIE, los procesa, genera variables, entrena modelos, calcula metricas, guarda artefactos y realiza inferencia del siguiente periodo disponible.

Tambien se ha cumplido el objetivo de comparar varios modelos. Aunque la idea inicial se centraba en una red neuronal sencilla, el proyecto evoluciono para incluir Ridge, MLP, HistGradientBoosting y un modo automatico de seleccion. Esta ampliacion mejora el valor academico del trabajo porque permite comparar enfoques en igualdad de condiciones.

La documentacion tambien se ha desarrollado de forma amplia. Se ha creado un directorio `documents/`, un indice de TFG y multiples capitulos que explican contexto, teoria, datos, preparacion, modelos, evaluacion, aplicacion y resultados.

### 17.2. Principales aportaciones del trabajo

La primera aportacion es una aplicacion reproducible para trabajar con datos reales del mercado electrico espanol. El proyecto no se limita a describir un modelo, sino que implementa un flujo completo desde la descarga hasta la inferencia.

La segunda aportacion es la automatizacion de la preparacion de datos OMIE. Los ficheros `MARGINALPDBC` se descargan, parsean, normalizan y transforman en una serie temporal util para aprendizaje supervisado.

La tercera aportacion es la ingenieria de variables. El sistema genera variables de calendario, ciclos, retardos, medias moviles, desviaciones, minimos, maximos, diferencias y ratios. Estas variables permiten que modelos relativamente sencillos capturen patrones temporales relevantes.

La cuarta aportacion es la comparacion de modelos. La aplicacion permite seleccionar manualmente `ridge`, `mlp` o `hist_gradient_boosting`, o usar `auto` para elegir el mejor por MAE. Esto evita asumir que una red neuronal sera siempre superior.

La quinta aportacion es la integracion opcional con ESIOS. Esta funcionalidad permite incorporar prevision eolica y solar, acercando el modelo a factores fisicos reales del sistema electrico.

### 17.3. Conclusiones tecnicas

Desde el punto de vista tecnico, el proyecto demuestra que scikit-learn es suficiente para construir una primera aproximacion solida al problema. Los modelos utilizados pueden entrenarse localmente y ofrecer resultados comparables sin recurrir a infraestructuras complejas.

Los resultados muestran que la cantidad de datos influye de forma notable. Con enero-marzo de 2025, Ridge fue el mejor modelo. Con casi todo 2025, HistGradientBoosting obtuvo el mejor resultado. Esto confirma que la eleccion del modelo depende del rango temporal y de la cantidad de informacion disponible.

La interfaz grafica aporta valor practico porque permite ejecutar el flujo por fases y observar progreso. Este punto fue importante para evitar que el entrenamiento pareciera bloqueado. La consola, por su parte, permite reproducir experimentos con comandos claros.

La serializacion del modelo junto con sus columnas de entrada es una decision correcta. Evita incoherencias entre entrenamiento e inferencia y permite reutilizar el modelo guardado.

### 17.4. Conclusiones sobre el mercado electrico

El mercado electrico espanol presenta patrones temporales que pueden aprenderse parcialmente a partir del historico de precios. Los ciclos horarios, diarios y semanales son relevantes, y los retardos aportan informacion util.

Sin embargo, el precio electrico no depende solo de su historia. La comparacion con el valor real de `2026-01-01 00:00` muestra que pueden existir errores importantes en situaciones concretas. Factores como festivos, demanda, meteorologia, renovables, gas, CO2 e interconexiones influyen de forma significativa.

Por tanto, una prediccion robusta del mercado electrico requiere combinar historico de precios con variables externas. El proyecto ha iniciado este camino incorporando ESIOS, pero todavia hay margen para enriquecer el modelo.

Tambien se concluye que una buena metrica agregada no elimina la necesidad de analisis de errores. El mercado puede presentar comportamientos especiales en dias concretos, y esos casos deben estudiarse de forma individual.

### 17.5. Valor de la aplicacion practica

El valor principal de la aplicacion es que convierte un problema teorico en una herramienta ejecutable. Permite descargar datos, entrenar modelos y obtener predicciones reales. Esto facilita la comprension del flujo completo de un proyecto de machine learning aplicado a energia.

La aplicacion tambien tiene valor como base de ampliacion. Su estructura modular permite incorporar nuevas fuentes de datos, nuevos modelos y nuevas metricas. El trabajo no queda cerrado en una unica version, sino que deja un camino claro para evolucionar.

Desde el punto de vista del TFG, el proyecto demuestra competencias de programacion, analisis de datos, aprendizaje automatico, documentacion, control de versiones y reflexion critica sobre resultados. La combinacion de codigo y memoria aporta una vision completa del problema.

En conclusion, el trabajo cumple su proposito: desarrollar y documentar una aplicacion practica para la prediccion del precio electrico espanol, mostrando tanto sus posibilidades como sus limitaciones.
