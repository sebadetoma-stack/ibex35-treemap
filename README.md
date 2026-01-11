# IBEX 35 Treemap - Visualización en Tiempo Real

Visualización interactiva del IBEX 35 con datos en tiempo real desde Yahoo Finance.

## 🚀 Deployment en Netlify

### Opción 1: Deployment Manual (Recomendado para empezar)

1. **Instala Python y las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecuta el script para generar los datos:**
   ```bash
   python update_ibex_data.py
   ```
   Esto creará el archivo `ibex_data.json` con los datos actuales.

3. **Sube a Netlify:**
   - Ve a https://app.netlify.com/
   - Arrastra y suelta estos archivos:
     - `ibex35_treemap.html` (renombrar a `index.html`)
     - `ibex_data.json`
   - ¡Listo! Tu sitio estará live

### Opción 2: Deployment Automático con GitHub Actions

1. **Sube el proyecto a GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin tu-repo-url
   git push -u origin main
   ```

2. **Conecta Netlify con GitHub:**
   - En Netlify: New site from Git → GitHub → Selecciona tu repo
   - Build settings:
     - Build command: `python update_ibex_data.py`
     - Publish directory: `.`

3. **Configura GitHub Actions para actualización automática:**
   
   Crea `.github/workflows/update-data.yml`:
   ```yaml
   name: Update IBEX Data
   
   on:
     schedule:
       - cron: '*/15 * * * *'  # Cada 15 minutos
     workflow_dispatch:  # Permite ejecución manual
   
   jobs:
     update:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         
         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.11'
         
         - name: Install dependencies
           run: pip install -r requirements.txt
         
         - name: Update data
           run: python update_ibex_data.py
         
         - name: Commit and push if changed
           run: |
             git config --global user.name 'GitHub Action'
             git config --global user.email 'action@github.com'
             git add ibex_data.json
             git diff --quiet && git diff --staged --quiet || (git commit -m "Update IBEX data" && git push)
   ```

4. **Netlify detectará automáticamente los cambios** y re-deployará el sitio.

### Opción 3: Actualización Local con Script Automático

Si preferís actualizar manualmente desde tu máquina:

**En Linux/Mac, crea un script `auto_update.sh`:**
```bash
#!/bin/bash
while true; do
    python update_ibex_data.py
    git add ibex_data.json
    git commit -m "Update IBEX data $(date)"
    git push
    sleep 900  # 15 minutos
done
```

**En Windows, crea `auto_update.bat`:**
```batch
:loop
python update_ibex_data.py
git add ibex_data.json
git commit -m "Update IBEX data %date% %time%"
git push
timeout /t 900
goto loop
```

Ejecutalo en background:
```bash
chmod +x auto_update.sh
./auto_update.sh &
```

## 📋 Estructura de Archivos

```
ibex35-treemap/
├── index.html              # Visualización principal (renombrado desde ibex35_treemap.html)
├── ibex_data.json         # Datos del IBEX 35 (generado automáticamente)
├── update_ibex_data.py    # Script de actualización
├── requirements.txt       # Dependencias Python
└── README.md             # Este archivo
```

## 🔧 Configuración

### Personalizar frecuencia de actualización

En `index.html`, línea final del script:
```javascript
// Recargar datos cada 15 minutos (900000 ms)
setInterval(loadData, 15 * 60 * 1000);
```

### Ajustar colores o estilos

Edita las variables CSS en el `<style>` del HTML o la función `getColor()` en JavaScript.

### Agregar/quitar empresas

Edita el array `IBEX_35_COMPANIES` en `update_ibex_data.py`:
```python
IBEX_35_COMPANIES = [
    {'name': 'Nombre', 'ticker': 'TICKER.MC', 'sector': 'Sector'},
    # ...
]
```

## 🐛 Troubleshooting

**Error "No module named 'yfinance'":**
```bash
pip install yfinance --upgrade
```

**Datos no se actualizan en Netlify:**
- Verifica que `ibex_data.json` se esté commiteando al repo
- Revisa los build logs en Netlify

**Empresas no aparecen:**
- Verifica que el ticker sea correcto (debe terminar en `.MC`)
- Algunos tickers pueden haber cambiado en Yahoo Finance

**Rate limiting de Yahoo Finance:**
- El script tiene delays incorporados
- Si persiste, aumenta el `time.sleep()` en el script

## 📊 Datos

- **Fuente:** Yahoo Finance
- **Índice:** ^IBEX (IBEX 35)
- **Empresas:** 35 valores del IBEX 35
- **Actualización sugerida:** Cada 15-20 minutos (límites de Yahoo Finance)

## 📝 Notas

- Yahoo Finance tiene rate limiting. No actualizar más frecuente que cada 10 minutos.
- Los datos tienen un delay de ~15 minutos respecto al mercado real.
- Para datos en tiempo real verdadero, necesitarías una API de pago (Bloomberg, Reuters, etc.)

## 🎨 Personalización para El Cronista

Si querés branded con los colores de El Cronista, edita estas líneas en el HTML:

```css
.header {
    background: linear-gradient(135deg, #TU_COLOR_1 0%, #TU_COLOR_2 100%);
}
```

## 📧 Soporte

Cualquier duda, revisá la documentación de:
- [Yahoo Finance Python](https://github.com/ranaroussi/yfinance)
- [Plotly](https://plotly.com/javascript/)
- [Netlify](https://docs.netlify.com/)
