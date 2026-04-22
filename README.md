# 🎓 Proyecto Maestría – UIDE

## 📌 Descripción

Este proyecto implementa un **web scraper en Python** para la búsqueda automatizada de modelos 3D en plataformas populares como:

* Printables
* MakerWorld

El sistema permite buscar modelos a partir de una palabra clave, extraer información relevante (nombre, imagen y enlace) y guardar los resultados en un archivo Excel para su posterior análisis.

---

## ⚙️ Tecnologías utilizadas

* **Python 3**
* **Selenium** – Automatización del navegador
* **Pandas** – Manipulación y exportación de datos
* **WebDriver Manager** – Gestión automática de drivers
* **Chrome WebDriver**

---

## 🚀 Funcionalidades

* 🔍 Búsqueda de modelos 3D por palabra clave
* 🌐 Scraping de múltiples plataformas
* 🖼️ Extracción de imágenes de los modelos
* 🔗 Obtención de enlaces directos
* 📊 Exportación de resultados a Excel
* 🖥️ Visualización de resultados en consola

---

## 📂 Estructura del proyecto

```
project/
│
├── scraper.py
├── modelos_3d_encontrados.xlsx
└── README.md
```

---

## 🧠 Lógica del sistema

El sistema está basado en una clase principal:

### `ModelScraper`

Encargada de:

* Inicializar el navegador
* Ejecutar scraping en cada plataforma
* Almacenar resultados
* Exportar datos

### Métodos principales

| Método                          | Descripción                     |
| ------------------------------- | ------------------------------- |
| `scrape_printables()`           | Extrae modelos desde Printables |
| `scrape_makerworld()`           | Extrae modelos desde MakerWorld |
| `mostrar_primeros_resultados()` | Muestra resultados en consola   |
| `save_to_excel()`               | Guarda resultados en Excel      |
| `close()`                       | Cierra el navegador             |

---

## ▶️ Ejecución

### 1. Instalar dependencias

```bash
pip install pandas selenium webdriver-manager openpyxl
```

### 2. Ejecutar el script

```bash
python scraper.py
```

---

## 🔎 Ejemplo de uso

```python
term = "macetas"

scraper = ModelScraper()

scraper.scrape_printables(term)
scraper.scrape_makerworld(term)

scraper.mostrar_primeros_resultados()
scraper.save_to_excel("modelos_3d_encontrados.xlsx")

scraper.close()
```

---

## 📊 Salida esperada

* Archivo Excel: `modelos_3d_encontrados.xlsx`
* Contenido:

  * Plataforma
  * Nombre del modelo
  * Imagen
  * Link

---

## ⚠️ Consideraciones

* Algunas páginas utilizan **lazy loading**, por lo que se implementan scrolls y esperas.
* Los selectores CSS pueden cambiar con el tiempo.
* Se limita la extracción a **3 resultados por plataforma** (configurable).
