

# Predicción del mercado eléctrico español mediante técnicas de aprendizaje automático


## Capítulos desarrollados

- [Capítulo 1. Resumen](capitulo_01_resumen.md)
- [Capítulo 2. Introducción](capitulo_02_introduccion.md)
- [Capítulo 3. Objetivos](capitulo_03_objetivos.md)
- [Capítulo 4. Marco teórico](capitulo_04_marco_teorico.md)
- [Capítulo 5. Estado del arte](capitulo_05_estado_del_arte.md)
- [Capítulo 6. Fuentes de datos](capitulo_06_fuentes_de_datos.md)
- [Capítulo 7. Preparación de datos](capitulo_07_preparacion_de_datos.md)
- [Capítulo 8. Ingeniería de variables](capitulo_08_ingenieria_de_variables.md)
- [Capítulo 9. Modelos de predicción](capitulo_09_modelos_de_prediccion.md)
- [Capítulo 10. Metodología de evaluación](capitulo_10_metodologia_de_evaluacion.md)
- [Capítulo 11. Diseño de la aplicación práctica](capitulo_11_diseno_aplicacion_practica.md)
- [Capítulo 12. Implementación del proyecto](capitulo_12_implementacion_proyecto.md)
- [Capítulo 13. Aplicación práctica desarrollada](capitulo_13_aplicacion_practica_desarrollada.md)
- [Capítulo 14. Información concreta del proyecto implementado](capitulo_14_informacion_concreta_proyecto.md)
- [Capítulo 15. Resultados experimentales](capitulo_15_resultados_experimentales.md)
- [Capítulo 16. Discusión](capitulo_16_discusion.md)
- [Capítulo 17. Conclusiones](capitulo_17_conclusiones.md)
- [Capítulo 18. Líneas futuras](capitulo_18_lineas_futuras.md)
- [Capítulo 19. Planificación del proyecto](capitulo_19_planificacion_proyecto.md)
- [Capítulo 20. Bibliografía y referencias](capitulo_20_bibliografia_referencias.md)
- [Capítulo 21. Anexos](capitulo_21_anexos.md)

> Nota: a medida que se desarrollen nuevos capítulos, se añadirán enlaces a sus ficheros Markdown correspondientes.

### [1. Resumen](capitulo_01_resumen.md)

1.1. Contexto del mercado eléctrico español  
1.2. Objetivo principal del trabajo  
1.3. Metodología empleada  
1.4. Resultados esperados  
1.5. Aplicación práctica desarrollada  
1.6. Contribuciones del trabajo  
1.7. Alcance y límites del resumen  
1.8. Síntesis del capítulo  

### [2. Introducción](capitulo_02_introduccion.md)

2.1. Motivación del estudio  
2.2. Importancia de la predicción del precio eléctrico  
2.3. Problema a resolver  
2.4. Alcance del trabajo  
2.5. Estructura del documento  

### [3. Objetivos](capitulo_03_objetivos.md)

3.1. Objetivo general  
3.2. Objetivos específicos  
3.3. Requisitos funcionales de la aplicación  
3.4. Requisitos no funcionales  
3.5. Limitaciones iniciales  

### [4. Marco teórico](capitulo_04_marco_teorico.md)

4.1. Funcionamiento del mercado eléctrico español  
4.2. Mercado diario e intradiario  
4.3. Papel de OMIE en el mercado eléctrico  
4.4. Papel de Red Eléctrica y ESIOS  
4.5. Factores que influyen en el precio eléctrico  
4.6. Generación renovable y formación de precios  
4.7. Particularidades de la energía eólica  
4.8. Particularidades de la energía solar fotovoltaica  
4.9. Series temporales aplicadas a mercados eléctricos  
4.10. Conceptos básicos de aprendizaje automático supervisado  

### [5. Estado del arte](capitulo_05_estado_del_arte.md)

5.1. Modelos estadísticos clásicos para predicción de precios  
5.2. Modelos de machine learning aplicados a energía  
5.3. Redes neuronales en predicción de series temporales  
5.4. Modelos basados en árboles y boosting  
5.5. Comparación de enfoques existentes  
5.6. Principales retos detectados en la literatura  

### [6. Fuentes de datos](capitulo_06_fuentes_de_datos.md)

6.1. Datos de precio del mercado diario OMIE  
6.2. Formato de los ficheros `MARGINALPDBC`  
6.3. Datos de previsión eólica de ESIOS  
6.4. Datos de previsión solar fotovoltaica de ESIOS  
6.5. Datos de previsión solar térmica de ESIOS  
6.6. Frecuencia temporal de los datos  
6.7. Tratamiento de datos horarios y cuarto-horarios  
6.8. Problemas de disponibilidad y calidad de datos  
6.9. Estrategia de cache y almacenamiento local  

### [7. Preparación de datos](capitulo_07_preparacion_de_datos.md)

7.1. Descarga automatizada de datos OMIE  
7.2. Descarga opcional de datos ESIOS  
7.3. Limpieza de datos  
7.4. Normalización de fechas y periodos  
7.5. Unión de datos por `timestamp`  
7.6. Gestión de datos ausentes  
7.7. Construcción del dataset supervisado  
7.8. Separación temporal entre entrenamiento y validación  

### [8. Ingeniería de variables](capitulo_08_ingenieria_de_variables.md)

8.1. Variables de calendario  
8.2. Variables cíclicas de hora, día y mes  
8.3. Retardos del precio eléctrico  
8.4. Medias móviles  
8.5. Desviaciones móviles  
8.6. Mínimos y máximos recientes  
8.7. Diferencias frente a periodos anteriores  
8.8. Ratios temporales  
8.9. Variables externas de generación renovable  
8.10. Variables derivadas de eólica y solar  

### [9. Modelos de predicción](capitulo_09_modelos_de_prediccion.md)

9.1. Modelo baseline `lag 24`  
9.2. Regresión Ridge `RidgeCV`  
9.3. Red neuronal `MLPRegressor`  
9.4. Modelo `HistGradientBoostingRegressor`  
9.5. Modo automático de selección de modelo  
9.6. Justificación de los modelos seleccionados  
9.7. Hiperparámetros utilizados  
9.8. Ventajas e inconvenientes de cada modelo  

### [10. Metodología de evaluación](capitulo_10_metodologia_de_evaluacion.md)

10.1. Validación temporal  
10.2. Evitar fuga de información futura  
10.3. Métrica MAE  
10.4. Métrica RMSE  
10.5. Métrica R2  
10.6. Comparación contra baseline  
10.7. Análisis de errores  
10.8. Evaluación por rangos temporales  

### [11. Diseño de la aplicación práctica](capitulo_11_diseno_aplicacion_practica.md)

11.1. Arquitectura general del software  
11.2. Módulos principales del proyecto  
11.3. Flujo de ejecución completo  
11.4. Interfaz gráfica  
11.5. Interfaz por consola  
11.6. Gestión de artefactos generados  
11.7. Configuración del entorno Python  
11.8. Control de versiones con Git  

### [12. Implementación del proyecto](capitulo_12_implementacion_proyecto.md)

12.1. Estructura de directorios  
12.2. Módulo de descarga y parseo de OMIE  
12.3. Módulo de integración con ESIOS  
12.4. Módulo de generación de variables  
12.5. Módulo de entrenamiento  
12.6. Módulo de inferencia  
12.7. Interfaz gráfica con Tkinter  
12.8. Serialización del modelo entrenado  
12.9. Generación de gráficas de validación  

### [13. Aplicación práctica desarrollada](capitulo_13_aplicacion_practica_desarrollada.md)

13.1. Descripción general de la aplicación  
13.2. Objetivo de la aplicación  
13.3. Datos utilizados  
13.4. Flujo de trabajo en la interfaz gráfica  
13.5. Selección manual de modelos  
13.6. Modo automático de selección  
13.7. Entrenamiento con datos OMIE  
13.8. Entrenamiento con variables ESIOS opcionales  
13.9. Inferencia del siguiente periodo  
13.10. Comparación entre predicción y valor real  

### [14. Información concreta del proyecto implementado](capitulo_14_informacion_concreta_proyecto.md)

14.1. Nombre del proyecto: `omie_v2_python`  
14.2. Lenguaje utilizado: Python  
14.3. Entorno virtual: `.venv`  
14.4. Paquete principal: `omie_price_nn`  
14.5. Repositorio GitHub: `https://github.com/Ju4nC4r/omie_v2_python.git`  
14.6. Comando de interfaz gráfica: `omie-price-gui`  
14.7. Comando de entrenamiento: `omie-price-train`  
14.8. Comando de predicción: `omie-price-predict`  
14.9. Modelo guardado: `models/omie_model.joblib`  
14.10. Gráfica generada: `models/validation_plot.png`  

### [15. Resultados experimentales](capitulo_15_resultados_experimentales.md)

15.1. Entrenamiento con datos de enero a marzo de 2025  
15.2. Entrenamiento con datos de todo 2025  
15.3. Comparación entre `ridge`, `mlp` y `hist_gradient_boosting`  
15.4. Resultados del modo `auto`  
15.5. Comparación con baseline `lag 24`  
15.6. Análisis del error en predicciones concretas  
15.7. Caso práctico: predicción para `2026-01-01 00:00`  
15.8. Comparación con el valor real publicado por OMIE  

### [16. Discusión](capitulo_16_discusion.md)

16.1. Interpretacion de resultados  
16.2. Influencia de la cantidad de datos históricos  
16.3. Impacto esperado de las variables renovables  
16.4. Limitaciones del modelo sin variables externas  
16.5. Limitaciones del modelo con variables ESIOS  
16.6. Riesgos de sobreajuste  
16.7. Robustez del sistema ante datos ausentes  

### [17. Conclusiones](capitulo_17_conclusiones.md)

17.1. Cumplimiento de objetivos  
17.2. Principales aportaciones del trabajo  
17.3. Conclusiones técnicas  
17.4. Conclusiones sobre el mercado eléctrico  
17.5. Valor de la aplicación práctica  

### [18. Líneas futuras](capitulo_18_lineas_futuras.md)

18.1. Incorporación de demanda prevista  
18.2. Incorporación de meteorología  
18.3. Incorporación de festivos nacionales y autonómicos  
18.4. Predicción del día completo  
18.5. Backtesting mensual  
18.6. Modelos específicos de series temporales  
18.7. Optimización de hiperparámetros  
18.8. Despliegue como aplicación web  

### [19. Planificación del proyecto](capitulo_19_planificacion_proyecto.md)

19.1. Fases del desarrollo  
19.2. Cronograma estimado  
19.3. Herramientas utilizadas  
19.4. Riesgos identificados  
19.5. Gestión del repositorio  

### [20. Bibliografía y referencias](capitulo_20_bibliografia_referencias.md)

20.1. Documentación de OMIE  
20.2. Documentación de ESIOS/REE  
20.3. Documentación de scikit-learn  
20.4. Bibliografía sobre predicción de precios eléctricos  
20.5. Bibliografía sobre series temporales  
20.6. Bibliografía sobre aprendizaje automático  

### [21. Anexos](capitulo_21_anexos.md)

21.1. Manual de instalación  
21.2. Manual de usuario de la interfaz gráfica  
21.3. Manual de ejecución por consola  
21.4. Configuración de token ESIOS  
21.5. Configuración de GitHub mediante SSH  
21.6. Fragmentos relevantes de código  
21.7. Resultados completos de experimentación  
21.8. Capturas de pantalla de la aplicación  
