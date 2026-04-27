# Capítulo 17. Conclusiones

## Predicción del mercado eléctrico español mediante técnicas de aprendizaje automático

### 17.1. Cumplimiento de objetivos

El objetivo principal del trabajo era desarrollar una aplicación capaz de predecir el precio del mercado eléctrico español mediante técnicas de aprendizaje automático, utilizando datos públicos de OMIE y, opcionalmente, variables renovables de ESIOS. Este objetivo se ha cumplido.

Se ha creado un proyecto Python funcional, con entorno virtual, estructura modular, comandos de consola e interfaz gráfica. La aplicación descarga datos OMIE, los procesa, genera variables, entrena modelos, calcula métricas, guarda artefactos y realiza inferencia del siguiente periodo disponible.

También se ha cumplido el objetivo de comparar varios modelos. Aunque la idea inicial se centraba en una red neuronal sencilla, el proyecto evolucióno para incluir Ridge, MLP, HistGradientBoosting y un modo automático de selección. Esta ampliación mejora el valor académico del trabajo porque permite comparar enfoques en igualdad de condiciones.

La documentación también se ha desarrollado de forma amplia. Se ha creado un directorio `documents/`, un índice de Proyecto y múltiples capítulos que explican contexto, teoria, datos, preparación, modelos, evaluación, aplicación y resultados.

### 17.2. Principales aportaciones del trabajo

La primera aportación es una aplicación reproducible para trabajar con datos reales del mercado eléctrico español. El proyecto no se limita a describir un modelo, sino que implementa un flujo completo desde la descarga hasta la inferencia.

La segunda aportación es la automatización de la preparación de datos OMIE. Los ficheros `MARGINALPDBC` se descargan, parsean, normalizan y transforman en una serie temporal útil para aprendizaje supervisado.

La tercera aportación es la ingeniería de variables. El sistema genera variables de calendario, ciclos, retardos, medias móviles, desviaciones, mínimos, máximos, diferencias y ratios. Estas variables permiten qué modelos relativamente sencillos capturen patrones temporales relevantes.

La cuarta aportación es la comparación de modelos. La aplicación permite seleccionar manualmente `ridge`, `mlp` o `hist_gradient_boosting`, o usar `auto` para elegir el mejor por MAE. Esto evita asumir que una red neuronal será siempre superior.

La quinta aportación es la integración opcional con ESIOS. Esta funcionalidad permite incorporar previsión eólica y solar, acercando el modelo a factores físicos reales del sistema eléctrico.

### 17.3. Conclusiones técnicas

Desde el punto de vista técnico, el proyecto demuestra que scikit-learn es suficiente para construir una primera aproximación sólida al problema. Los modelos utilizados pueden entrenarse localmente y ofrecer resultados comparables sin recurrir a infraestructuras complejas.

Los resultados muestran que la cantidad de datos influye de forma notable. Con enero-marzo de 2025, Ridge fue el mejor modelo. Con casi todo 2025, HistGradientBoosting obtuvo el mejor resultado. Esto confirma que la elección del modelo depende del rango temporal y de la cantidad de información disponible.

La interfaz gráfica aporta valor práctico porque permite ejecutar el flujo por fases y observar progreso. Este punto fue importante para evitar que el entrenamiento pareciera bloqueado. La consola, por su parte, permite reproducir experimentos con comandos claros.

La serialización del modelo junto con sus columnas de entrada es una decisión correcta. Evita incoherencias entre entrenamiento e inferencia y permite reutilizar el modelo guardado.

### 17.4. Conclusiones sobre el mercado eléctrico

El mercado eléctrico español presenta patrones temporales que pueden aprenderse parcialmente a partir del histórico de precios. Los ciclos horarios, diarios y semanales son relevantes, y los retardos aportan información útil.

Sin embargo, el precio eléctrico no depende solo de su historia. La comparación con el valor real de `2026-01-01 00:00` muestra que pueden existir errores importantes en situaciones concretas. Factores como festivos, demanda, meteorología, renovables, gas, CO2 e interconexiones influyen de forma significativa.

Por tanto, una predicción robusta del mercado eléctrico requiere combinar histórico de precios con variables externas. El proyecto ha iniciado este camino incorporando ESIOS, pero todavía hay margen para enriquecer el modelo.

También se concluye que una buena métrica agregada no elimina la necesidad de análisis de errores. El mercado puede presentar comportamientos especiales en días concretos, y esos casos deben estudiarse de forma individual.

### 17.5. Valor de la aplicación práctica

El valor principal de la aplicación es que convierte un problema teórico en una herramienta ejecutable. Permite descargar datos, entrenar modelos y obtener predicciones reales. Esto facilita la comprensión del flujo completo de un proyecto de machine learning aplicado a energía.

La aplicación también tiene valor como base de ampliación. Su estructura modular permite incorporar nuevas fuentes de datos, nuevos modelos y nuevas métricas. El trabajo no queda cerrado en una única versión, sino que deja un camino claro para evolucionar.

Desde el punto de vista del Proyecto, el proyecto demuestra competencias de programación, análisis de datos, aprendizaje automático, documentación, control de versiones y reflexion crítica sobre resultados. La combinación de código y memoria aporta una visión completa del problema.

En conclusión, el trabajo cumple su propósito: desarrollar y documentar una aplicación práctica para la predicción del precio eléctrico español, mostrando tanto sus posibilidades como sus limitaciones.
