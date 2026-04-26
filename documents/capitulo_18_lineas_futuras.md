# Capitulo 18. Lineas futuras

## Prediccion del mercado electrico espanol mediante tecnicas de aprendizaje automatico

### 18.1. Incorporacion de demanda prevista

Una de las mejoras mas importantes seria incorporar demanda electrica prevista. La demanda es uno de los factores fundamentales en la formacion del precio del mercado diario. Cuando la demanda aumenta, el sistema necesita mas generacion y puede entrar tecnologia mas cara en el orden de merito.

Actualmente, el modelo aprende indirectamente patrones de demanda a traves del calendario y del historico de precios. Sin embargo, no observa la demanda prevista de forma explicita. Incluir esta variable podria mejorar la prediccion, especialmente en olas de frio, olas de calor, dias festivos o cambios de actividad economica.

La demanda podria obtenerse desde ESIOS u otras fuentes oficiales. Seria necesario normalizarla por `timestamp`, unirla al dataset y generar variables derivadas, como demanda respecto a la media semanal o demanda prevista por franja horaria.

### 18.2. Incorporacion de meteorologia

La meteorologia afecta tanto a la demanda como a la generacion renovable. Temperatura, viento, radiacion solar, nubosidad y precipitacion pueden influir de forma importante en el precio electrico.

Incorporar meteorologia permitiria mejorar la explicacion de varios fenomenos. La temperatura afecta al consumo por calefaccion y refrigeracion. El viento condiciona la produccion eolica. La radiacion y nubosidad afectan a la solar fotovoltaica. La precipitacion y reservas hidraulicas pueden afectar a la generacion hidraulica.

Una posible mejora seria integrar datos meteorologicos por zonas representativas de Espana peninsular. Para no complicar excesivamente el modelo, se podria empezar con variables agregadas: temperatura media prevista, viento medio previsto y radiacion solar prevista.

### 18.3. Incorporacion de festivos nacionales y autonomicos

El error observado en `2026-01-01 00:00` sugiere la importancia de los festivos. El modelo actual diferencia fines de semana, pero no identifica festivos nacionales, autonomicos o locales. Esto limita su capacidad para anticipar patrones de demanda especiales.

Incorporar festivos permitiria crear variables como `is_holiday`, `is_christmas_period`, `is_new_year` o `bridge_day`. Estas variables podrian ayudar a distinguir un miercoles normal de un miercoles festivo.

La implementacion podria apoyarse en calendarios publicos o bibliotecas Python de festivos. Seria importante definir claramente el ambito geografico, ya que algunos festivos son nacionales y otros autonomicos.

### 18.4. Prediccion del dia completo

La aplicacion actual predice el siguiente periodo disponible. Una extension natural seria predecir el dia completo, generando 24 valores horarios o 96 valores cuarto-horarios. Este horizonte es mas cercano al funcionamiento del mercado diario, donde se negocia energia para todos los periodos del dia siguiente.

Para implementar esta mejora, habria que construir variables futuras para cada periodo del dia objetivo. Las variables de calendario son conocidas, pero las variables basadas en precios retardados deberian actualizarse cuidadosamente para no introducir informacion futura. Tambien seria necesario disponer de previsiones externas para todo el horizonte.

La prediccion del dia completo permitiria generar curvas de precio previstas, comparar perfiles horarios y evaluar el error por franja.

### 18.5. Backtesting mensual

El backtesting mensual permitiria evaluar el modelo de forma mas robusta. En lugar de entrenar una vez y validar sobre un unico tramo, se podrian crear multiples experimentos: entrenar hasta cierto mes, predecir el mes siguiente y repetir el proceso.

Esta metodologia mostraria si el modelo mantiene su rendimiento a lo largo del tiempo. Tambien permitiria detectar meses especialmente dificiles y comparar estabilidad entre Ridge, MLP e HistGradientBoosting.

El resultado podria resumirse en una tabla de MAE, RMSE y R2 por mes. Esta informacion seria muy valiosa para la discusion del TFG y para futuras mejoras.

### 18.6. Modelos especificos de series temporales

Aunque el proyecto utiliza modelos tabulares, existen modelos especificos de series temporales que podrian explorarse. Entre ellos se encuentran ARIMA, SARIMA, Prophet, modelos recurrentes como LSTM o GRU, y arquitecturas modernas basadas en atencion.

Estos modelos podrian capturar secuencias de forma mas directa. Por ejemplo, una LSTM podria recibir ventanas de precios y variables externas, mientras que un Transformer temporal podria aprender relaciones a distintos horizontes.

No obstante, estos enfoques requieren mas complejidad, mas datos y una evaluacion cuidadosa. Por ello, se plantean como linea futura y no como sustituto inmediato del sistema actual.

### 18.7. Optimizacion de hiperparametros

Los hiperparametros actuales se eligieron de forma razonable y conservadora. Una mejora futura seria realizar busqueda sistematica de hiperparametros mediante validacion temporal. Esto podria aplicarse a Ridge, MLP e HistGradientBoosting.

Para Ridge, se podria ampliar el rango de `alpha`. Para MLP, se podrian probar arquitecturas, tasas de aprendizaje, regularizacion y funciones de activacion. Para HistGradientBoosting, se podrian ajustar profundidad, numero de iteraciones, tasa de aprendizaje y regularizacion.

La optimizacion deberia evitar fuga de informacion. No bastaria con una validacion aleatoria; seria necesario usar particiones temporales o backtesting. El objetivo seria mejorar precision sin sacrificar generalizacion.

### 18.8. Despliegue como aplicacion web

Otra linea futura seria desplegar la aplicacion como web. Actualmente se ejecuta localmente mediante GUI Tkinter o consola. Una version web permitiria acceder desde navegador, seleccionar rangos, lanzar entrenamientos y visualizar resultados de forma mas amigable.

Una posible arquitectura seria un backend Python con FastAPI y una interfaz web sencilla. El backend ejecutaria descargas, entrenamiento e inferencia; el frontend mostraria formularios, metricas y graficas. Tambien podria incluir autenticacion para proteger tokens ESIOS.

El despliegue web abriria la puerta a programar entrenamientos periodicos, almacenar historico de predicciones y comparar automaticamente prediccion frente a valor real cuando OMIE publique nuevos datos.

En conjunto, las lineas futuras muestran que el proyecto puede evolucionar en varias direcciones: mas datos, mejores variables, modelos mas avanzados, evaluacion mas robusta y despliegue mas accesible. La version actual constituye una base funcional sobre la que construir esas mejoras.
