# Indice propuesto de Trabajo Fin de Grado

## Prediccion del mercado electrico espanol mediante tecnicas de aprendizaje automatico

## Capitulos desarrollados

- [Capitulo 1. Resumen](capitulo_01_resumen.md)
- [Capitulo 2. Introduccion](capitulo_02_introduccion.md)
- [Capitulo 3. Objetivos](capitulo_03_objetivos.md)
- [Capitulo 4. Marco teorico](capitulo_04_marco_teorico.md)
- [Capitulo 5. Estado del arte](capitulo_05_estado_del_arte.md)
- [Capitulo 6. Fuentes de datos](capitulo_06_fuentes_de_datos.md)
- [Capitulo 7. Preparacion de datos](capitulo_07_preparacion_de_datos.md)
- [Capitulo 8. Ingenieria de variables](capitulo_08_ingenieria_de_variables.md)
- [Capitulo 9. Modelos de prediccion](capitulo_09_modelos_de_prediccion.md)
- [Capitulo 10. Metodologia de evaluacion](capitulo_10_metodologia_de_evaluacion.md)
- [Capitulo 11. Diseno de la aplicacion practica](capitulo_11_diseno_aplicacion_practica.md)
- [Capitulo 12. Implementacion del proyecto](capitulo_12_implementacion_proyecto.md)
- [Capitulo 13. Aplicacion practica desarrollada](capitulo_13_aplicacion_practica_desarrollada.md)
- [Capitulo 14. Informacion concreta del proyecto implementado](capitulo_14_informacion_concreta_proyecto.md)
- [Capitulo 15. Resultados experimentales](capitulo_15_resultados_experimentales.md)

> Nota: a medida que se desarrollen nuevos capitulos, se anadiran enlaces a sus ficheros Markdown correspondientes.

### [1. Resumen](capitulo_01_resumen.md)

1.1. Contexto del mercado electrico espanol  
1.2. Objetivo principal del trabajo  
1.3. Metodologia empleada  
1.4. Resultados esperados  
1.5. Aplicacion practica desarrollada  
1.6. Contribuciones del trabajo  
1.7. Alcance y limites del resumen  
1.8. Sintesis del capitulo  

### [2. Introduccion](capitulo_02_introduccion.md)

2.1. Motivacion del estudio  
2.2. Importancia de la prediccion del precio electrico  
2.3. Problema a resolver  
2.4. Alcance del trabajo  
2.5. Estructura del documento  

### [3. Objetivos](capitulo_03_objetivos.md)

3.1. Objetivo general  
3.2. Objetivos especificos  
3.3. Requisitos funcionales de la aplicacion  
3.4. Requisitos no funcionales  
3.5. Limitaciones iniciales  

### [4. Marco teorico](capitulo_04_marco_teorico.md)

4.1. Funcionamiento del mercado electrico espanol  
4.2. Mercado diario e intradiario  
4.3. Papel de OMIE en el mercado electrico  
4.4. Papel de Red Electrica y ESIOS  
4.5. Factores que influyen en el precio electrico  
4.6. Generacion renovable y formacion de precios  
4.7. Particularidades de la energia eolica  
4.8. Particularidades de la energia solar fotovoltaica  
4.9. Series temporales aplicadas a mercados electricos  
4.10. Conceptos basicos de aprendizaje automatico supervisado  

### [5. Estado del arte](capitulo_05_estado_del_arte.md)

5.1. Modelos estadisticos clasicos para prediccion de precios  
5.2. Modelos de machine learning aplicados a energia  
5.3. Redes neuronales en prediccion de series temporales  
5.4. Modelos basados en arboles y boosting  
5.5. Comparacion de enfoques existentes  
5.6. Principales retos detectados en la literatura  

### [6. Fuentes de datos](capitulo_06_fuentes_de_datos.md)

6.1. Datos de precio del mercado diario OMIE  
6.2. Formato de los ficheros `MARGINALPDBC`  
6.3. Datos de prevision eolica de ESIOS  
6.4. Datos de prevision solar fotovoltaica de ESIOS  
6.5. Datos de prevision solar termica de ESIOS  
6.6. Frecuencia temporal de los datos  
6.7. Tratamiento de datos horarios y cuarto-horarios  
6.8. Problemas de disponibilidad y calidad de datos  
6.9. Estrategia de cache y almacenamiento local  

### [7. Preparacion de datos](capitulo_07_preparacion_de_datos.md)

7.1. Descarga automatizada de datos OMIE  
7.2. Descarga opcional de datos ESIOS  
7.3. Limpieza de datos  
7.4. Normalizacion de fechas y periodos  
7.5. Union de datos por `timestamp`  
7.6. Gestion de datos ausentes  
7.7. Construccion del dataset supervisado  
7.8. Separacion temporal entre entrenamiento y validacion  

### [8. Ingenieria de variables](capitulo_08_ingenieria_de_variables.md)

8.1. Variables de calendario  
8.2. Variables ciclicas de hora, dia y mes  
8.3. Retardos del precio electrico  
8.4. Medias moviles  
8.5. Desviaciones moviles  
8.6. Minimos y maximos recientes  
8.7. Diferencias frente a periodos anteriores  
8.8. Ratios temporales  
8.9. Variables externas de generacion renovable  
8.10. Variables derivadas de eolica y solar  

### [9. Modelos de prediccion](capitulo_09_modelos_de_prediccion.md)

9.1. Modelo baseline `lag 24`  
9.2. Regresion Ridge `RidgeCV`  
9.3. Red neuronal `MLPRegressor`  
9.4. Modelo `HistGradientBoostingRegressor`  
9.5. Modo automatico de seleccion de modelo  
9.6. Justificacion de los modelos seleccionados  
9.7. Hiperparametros utilizados  
9.8. Ventajas e inconvenientes de cada modelo  

### [10. Metodologia de evaluacion](capitulo_10_metodologia_de_evaluacion.md)

10.1. Validacion temporal  
10.2. Evitar fuga de informacion futura  
10.3. Metrica MAE  
10.4. Metrica RMSE  
10.5. Metrica R2  
10.6. Comparacion contra baseline  
10.7. Analisis de errores  
10.8. Evaluacion por rangos temporales  

### [11. Diseno de la aplicacion practica](capitulo_11_diseno_aplicacion_practica.md)

11.1. Arquitectura general del software  
11.2. Modulos principales del proyecto  
11.3. Flujo de ejecucion completo  
11.4. Interfaz grafica  
11.5. Interfaz por consola  
11.6. Gestion de artefactos generados  
11.7. Configuracion del entorno Python  
11.8. Control de versiones con Git  

### [12. Implementacion del proyecto](capitulo_12_implementacion_proyecto.md)

12.1. Estructura de directorios  
12.2. Modulo de descarga y parseo de OMIE  
12.3. Modulo de integracion con ESIOS  
12.4. Modulo de generacion de variables  
12.5. Modulo de entrenamiento  
12.6. Modulo de inferencia  
12.7. Interfaz grafica con Tkinter  
12.8. Serializacion del modelo entrenado  
12.9. Generacion de graficas de validacion  

### [13. Aplicacion practica desarrollada](capitulo_13_aplicacion_practica_desarrollada.md)

13.1. Descripcion general de la aplicacion  
13.2. Objetivo de la aplicacion  
13.3. Datos utilizados  
13.4. Flujo de trabajo en la interfaz grafica  
13.5. Seleccion manual de modelos  
13.6. Modo automatico de seleccion  
13.7. Entrenamiento con datos OMIE  
13.8. Entrenamiento con variables ESIOS opcionales  
13.9. Inferencia del siguiente periodo  
13.10. Comparacion entre prediccion y valor real  

### [14. Informacion concreta del proyecto implementado](capitulo_14_informacion_concreta_proyecto.md)

14.1. Nombre del proyecto: `omie_v2_python`  
14.2. Lenguaje utilizado: Python  
14.3. Entorno virtual: `.venv`  
14.4. Paquete principal: `omie_price_nn`  
14.5. Repositorio GitHub: `https://github.com/Ju4nC4r/omie_v2_python.git`  
14.6. Comando de interfaz grafica: `omie-price-gui`  
14.7. Comando de entrenamiento: `omie-price-train`  
14.8. Comando de prediccion: `omie-price-predict`  
14.9. Modelo guardado: `models/omie_model.joblib`  
14.10. Grafica generada: `models/validation_plot.png`  

### [15. Resultados experimentales](capitulo_15_resultados_experimentales.md)

15.1. Entrenamiento con datos de enero a marzo de 2025  
15.2. Entrenamiento con datos de todo 2025  
15.3. Comparacion entre `ridge`, `mlp` y `hist_gradient_boosting`  
15.4. Resultados del modo `auto`  
15.5. Comparacion con baseline `lag 24`  
15.6. Analisis del error en predicciones concretas  
15.7. Caso practico: prediccion para `2026-01-01 00:00`  
15.8. Comparacion con el valor real publicado por OMIE  

### 16. Discusion _(pendiente de desarrollar)_

16.1. Interpretacion de resultados  
16.2. Influencia de la cantidad de datos historicos  
16.3. Impacto esperado de las variables renovables  
16.4. Limitaciones del modelo sin variables externas  
16.5. Limitaciones del modelo con variables ESIOS  
16.6. Riesgos de sobreajuste  
16.7. Robustez del sistema ante datos ausentes  

### 17. Conclusiones _(pendiente de desarrollar)_

17.1. Cumplimiento de objetivos  
17.2. Principales aportaciones del trabajo  
17.3. Conclusiones tecnicas  
17.4. Conclusiones sobre el mercado electrico  
17.5. Valor de la aplicacion practica  

### 18. Lineas futuras _(pendiente de desarrollar)_

18.1. Incorporacion de demanda prevista  
18.2. Incorporacion de meteorologia  
18.3. Incorporacion de festivos nacionales y autonomicos  
18.4. Prediccion del dia completo  
18.5. Backtesting mensual  
18.6. Modelos especificos de series temporales  
18.7. Optimizacion de hiperparametros  
18.8. Despliegue como aplicacion web  

### 19. Planificacion del proyecto _(pendiente de desarrollar)_

19.1. Fases del desarrollo  
19.2. Cronograma estimado  
19.3. Herramientas utilizadas  
19.4. Riesgos identificados  
19.5. Gestion del repositorio  

### 20. Bibliografia y referencias _(pendiente de desarrollar)_

20.1. Documentacion de OMIE  
20.2. Documentacion de ESIOS/REE  
20.3. Documentacion de scikit-learn  
20.4. Bibliografia sobre prediccion de precios electricos  
20.5. Bibliografia sobre series temporales  
20.6. Bibliografia sobre aprendizaje automatico  

### 21. Anexos _(pendiente de desarrollar)_

21.1. Manual de instalacion  
21.2. Manual de usuario de la interfaz grafica  
21.3. Manual de ejecucion por consola  
21.4. Configuracion de token ESIOS  
21.5. Configuracion de GitHub mediante SSH  
21.6. Fragmentos relevantes de codigo  
21.7. Resultados completos de experimentacion  
21.8. Capturas de pantalla de la aplicacion  
