# Capitulo 21. Anexos

## Prediccion del mercado electrico espanol mediante tecnicas de aprendizaje automatico

### 21.1. Manual de instalacion

Para instalar el proyecto en un equipo local se recomienda usar un entorno virtual Python. Desde la raiz del repositorio:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Despues de instalar en modo editable, quedan disponibles los comandos:

```text
omie-price-gui
omie-price-train
omie-price-predict
```

Si se desea comprobar la instalacion:

```bash
omie-price-train --help
omie-price-predict --help
```

El entorno `.venv` no debe subirse a Git. Cada usuario puede crearlo de nuevo en su equipo.

### 21.2. Manual de usuario de la interfaz grafica

La interfaz grafica se ejecuta con:

```bash
omie-price-gui
```

La ventana permite indicar:

- fecha inicial
- fecha final
- modelo de entrenamiento
- uso opcional de ESIOS
- token ESIOS

Botones principales:

- `1. Extraccion`: descarga datos.
- `2. Preparacion`: prepara el dataset.
- `3. Entrenamiento + test`: entrena y evalua.
- `4. Inferencia`: predice el siguiente periodo.
- `Abrir grafica`: abre `models/validation_plot.png`.
- `Limpiar log`: limpia mensajes de la ventana.

El boton `Ejecutar todo` lanza el flujo completo. Durante la ejecucion se muestran logs y barra de progreso.

### 21.3. Manual de ejecucion por consola

Entrenamiento basico con OMIE:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model auto
```

Entrenar solo Ridge:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model ridge
```

Entrenar red neuronal:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model mlp
```

Entrenar HistGradientBoosting:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model hist_gradient_boosting
```

Inferencia:

```bash
omie-price-predict
```

El modelo se guarda por defecto en:

```text
models/omie_model.joblib
```

La grafica se guarda en:

```text
models/validation_plot.png
```

### 21.4. Configuracion de token ESIOS

Para usar variables renovables de ESIOS se necesita token. Puede indicarse mediante variable de entorno:

```bash
export ESIOS_TOKEN="tu_token_esios"
```

Despues se entrena con:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model auto --include-esios
```

Tambien puede pasarse directamente:

```bash
omie-price-train --start 2025-01-01 --end 2025-03-31 --model auto --include-esios --esios-token "tu_token_esios"
```

En la GUI, el token puede pegarse en el campo `Token ESIOS` y activar la casilla `ESIOS`.

### 21.5. Configuracion de GitHub mediante SSH

Para subir el repositorio a GitHub mediante SSH se necesita una clave registrada.

Generar clave:

```bash
ssh-keygen -t ed25519 -C "tu_email@example.com"
```

Mostrar clave publica:

```bash
cat ~/.ssh/id_ed25519.pub
```

Esa clave debe copiarse en GitHub, en:

```text
Settings -> SSH and GPG keys -> New SSH key
```

Probar conexion:

```bash
ssh -T git@github.com
```

Configurar remoto SSH:

```bash
git remote set-url origin git@github.com:Ju4nC4r/omie_v2_python.git
```

Subir cambios:

```bash
git push -u origin main
```

### 21.6. Fragmentos relevantes de codigo

Modulos principales:

```text
src/omie_price_nn/data.py
src/omie_price_nn/esios.py
src/omie_price_nn/features.py
src/omie_price_nn/train.py
src/omie_price_nn/predict.py
src/omie_price_nn/gui.py
```

Funciones relevantes:

- `load_omie_prices`
- `parse_marginalpdbc`
- `enrich_with_esios_generation`
- `make_supervised_dataset`
- `make_next_prediction_features`
- `train_model`

Estos fragmentos pueden incluirse en una version final de anexos si se desea mostrar codigo representativo sin sobrecargar el cuerpo principal de la memoria.

### 21.7. Resultados completos de experimentacion

Experimento enero-marzo 2025:

```text
Mejor modelo: ridge
MAE: 10.02 EUR/MWh
RMSE: 15.70 EUR/MWh
R2: 0.871
Baseline lag 24 MAE: 20.97 EUR/MWh
```

Comparacion:

```text
ridge: MAE 10.02
mlp: MAE 13.70
hist_gradient_boosting: MAE 10.23
```

Experimento casi todo 2025:

```text
Mejor modelo: hist_gradient_boosting
MAE: 3.17 EUR/MWh
RMSE: 4.59 EUR/MWh
R2: 0.973
Baseline lag 24 MAE: 24.91 EUR/MWh
```

Comparacion:

```text
ridge: MAE 4.10
mlp: MAE 3.98
hist_gradient_boosting: MAE 3.17
```

Inferencia:

```text
Prediccion para 2026-01-01 00:00:00: 94.20 EUR/MWh
Valor real OMIE: 112.01 EUR/MWh
Error absoluto: 17.81 EUR/MWh
Error relativo: 15.90 %
```

### 21.8. Capturas de pantalla de la aplicacion

En una version final del TFG pueden incorporarse capturas de:

- ventana principal de la GUI
- selector de modelo
- opcion ESIOS y token
- log durante entrenamiento
- resumen de metricas
- grafica `models/validation_plot.png`

Estas capturas ayudarian a documentar visualmente la aplicacion practica. Dado que las imagenes dependen de una ejecucion concreta, se recomienda generarlas al final, cuando la interfaz y los resultados esten cerrados.
