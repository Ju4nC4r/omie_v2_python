# Capítulo 18. Líneas futuras

## Predicción del mercado eléctrico español mediante técnicas de aprendizaje automático

### 18.1. Incorporación de demanda prevista

Una de las mejoras más importantes sería incorporar demanda eléctrica prevista. La demanda es uno de los factores fundamentales en la formación del precio del mercado diario. Cuando la demanda aumenta, el sistema necesita más generación y puede entrar tecnología más cara en el orden de mérito.

Actualmente, el modelo aprende indirectamente patrones de demanda a través del calendario y del histórico de precios. Sin embargo, no observa la demanda prevista de forma explícita. Incluir esta variable podría mejorar la predicción, especialmente en olas de frío, olas de calor, días festivos o cambios de actividad económica.

La demanda podría obtenerse desde ESIOS u otras fuentes oficiales. Sería necesario normalizarla por `timestamp`, unirla al dataset y generar variables derivadas, como demanda respecto a la media semanal o demanda prevista por franja horaria.

### 18.2. Incorporación de meteorología

La meteorología afecta tanto a la demanda como a la generación renovable. Temperatura, viento, radiación solar, nubosidad y precipitación pueden influir de forma importante en el precio eléctrico.

Incorporar meteorología permitiría mejorar la explicación de varios fenómenos. La temperatura afecta al consumo por calefacción y refrigeración. El viento condiciona la producción eólica. La radiación y nubosidad afectan a la solar fotovoltaica. La precipitación y reservas hidráulicas pueden afectar a la generación hidráulica.

Una posible mejora sería integrar datos meteorológicos por zonas representativas de España peninsular. Para no complicar excesivamente el modelo, se podría empezar con variables agregadas: temperatura media prevista, viento medio previsto y radiación solar prevista.

### 18.3. Incorporación de festivos nacionales y autonómicos

El error observado en `2026-01-01 00:00` sugiere la importancia de los festivos. El modelo actual diferencia fines de semana, pero no identifica festivos nacionales, autonómicos o locales. Esto limita su capacidad para anticipar patrones de demanda especiales.

Incorporar festivos permitiría crear variables como `is_holiday`, `is_christmas_period`, `is_new_year` o `bridge_day`. Estas variables podrían ayudar a distinguir un miercoles normal de un miercoles festivo.

La implementación podría apoyarse en calendarios públicos o bibliotecas Python de festivos. Sería importante definir claramente el ámbito geografico, ya que algunos festivos son nacionales y otros autonómicos.

### 18.4. Predicción del día completo

La aplicación actual predice el siguiente periodo disponible. Una extensión natural sería predecir el día completo, generando 24 valores horarios o 96 valores cuarto-horarios. Este horizonte es más cercano al funcionamiento del mercado diario, donde se negocia energía para todos los periodos del día siguiente.

Para implementar está mejora, habría que construir variables futuras para cada periodo del día objetivo. Las variables de calendario son conocidas, pero las variables basadas en precios retardados deberían actualizarse cuidadosamente para no introducir información futura. También sería necesario disponer de previsiones externas para todo el horizonte.

La predicción del día completo permitiría generar curvas de precio previstas, comparar perfiles horarios y evaluar el error por franja.

### 18.5. Backtesting mensual

El backtesting mensual permitiría evaluar el modelo de forma más robusta. En lugar de entrenar una vez y validar sobre un único tramo, se podrían crear múltiples experimentos: entrenar hasta cierto mes, predecir el mes siguiente y repetir el proceso.

Esta metodología mostraría si el modelo mantiene su rendimiento a lo largo del tiempo. También permitiría detectar meses especialmente difíciles y comparar estabilidad entre Ridge, MLP e HistGradientBoosting.

El resultado podría resumirse en una tabla de MAE, RMSE y R2 por mes. Esta información sería muy valiosa para la discusión del TFG y para futuras mejoras.

### 18.6. Modelos específicos de series temporales

Aunque el proyecto utiliza modelos tabulares, existen modelos específicos de series temporales que podrían explorarse. Entre ellos se encuentran ARIMA, SARIMA, Prophet, modelos recurrentes como LSTM o GRU, y arquitecturas modernas basadas en atencion.

Estos modelos podrían capturar secuencias de forma más directa. Por ejemplo, una LSTM podría recibir ventanas de precios y variables externas, mientras que un Transformer temporal podría aprender relaciones a distintos horizontes.

No obstante, estos enfoques requieren más complejidad, más datos y una evaluación cuidadosa. Por ello, se plantean como línea futura y no como sustituto inmediato del sistema actual.

### 18.7. Optimización de hiperparámetros

Los hiperparámetros actuales se eligieron de forma razonable y conservadora. Una mejora futura sería realizar búsqueda sistemática de hiperparámetros mediante validación temporal. Esto podría aplicarse a Ridge, MLP e HistGradientBoosting.

Para Ridge, se podría ampliar el rango de `alpha`. Para MLP, se podrían probar arquitecturas, tasas de aprendizaje, regularización y funciones de activacion. Para HistGradientBoosting, se podrían ajustar profundidad, número de iteraciones, tasa de aprendizaje y regularización.

La optimización debería evitar fuga de información. No bastaría con una validación aleatoria; sería necesario usar particiones temporales o backtesting. El objetivo sería mejorar precisión sin sacrificar generalización.

### 18.8. Despliegue como aplicación web

Otra línea futura sería desplegar la aplicación como web. Actualmente se ejecuta localmente mediante GUI Tkinter o consola. Una versión web permitiría acceder desde navegador, seleccionar rangos, lanzar entrenamientos y visualizar resultados de forma más amigable.

Una posible arquitectura sería un backend Python con FastAPI y una interfaz web sencilla. El backend ejecutaria descargas, entrenamiento e inferencia; el frontend mostraría formularios, métricas y gráficas. También podría incluir autenticación para proteger tokens ESIOS.

El despliegue web abriria la puerta a programar entrenamientos periódicos, almacenar histórico de predicciones y comparar automáticamente predicción frente a valor real cuando OMIE publique nuevos datos.

En conjunto, las líneas futuras muestran que el proyecto puede evolucionar en varias direcciones: más datos, mejores variables, modelos más avanzados, evaluación más robusta y despliegue más accesible. La versión actual constituye una base funcional sobre la que construir esas mejoras.
