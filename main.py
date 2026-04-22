import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class ModelScraper:
    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless") 
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.results = []

    def scrape_printables(self, search_term):
        print(f"Buscando '{search_term}' en Printables...")
        url = f"https://www.printables.com/search/models?ctx=models&q={search_term}"
        self.driver.get(url)
        
        try:
            # Esperamos a que los artículos (cards) estén presentes
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "article.card"))
            )
            time.sleep(2) 
            
            # Extraemos los artículos (ajusta el límite si necesitas más de 3)
            items = self.driver.find_elements(By.CSS_SELECTOR, "article.card")[:3]
            
            for item in items:
                try:
                    # El nombre y el link se encuentran en el mismo tag 'a' dentro del h5
                    title_elem = item.find_element(By.CSS_SELECTOR, "h5 a.clamp-two-lines")
                    name = title_elem.text.strip()
                    link = title_elem.get_attribute("href")
                    
                    # Para la imagen, buscamos dentro del picture que tiene la clase 'image-inside'
                    # Intentamos obtener el atributo srcset del tag source para evitar el placeholder base64
                    try:
                        img_container = item.find_element(By.CSS_SELECTOR, "picture.image-inside source")
                        img_src = img_container.get_attribute("srcset").split(",")[0].split(" ")[0]
                    except:
                        # Fallback si no encuentra el source (por ejemplo, si aún no cargó)
                        img_elem = item.find_element(By.CSS_SELECTOR, "img.svelte-11pdzs1")
                        img_src = img_elem.get_attribute("src")

                    self.results.append({
                        "Plataforma": "Printables",
                        "Nombre": name,
                        "Imagen": img_src,
                        "Link": link
                    })
                except Exception as e:
                    print(f"Error procesando un item de Printables: {e}")
                    continue

        except Exception as e:
            print(f"Error general en Printables: {e}")

    def scrape_makerworld(self, search_term):
        print(f"Buscando '{search_term}' en MakerWorld...")
        url = f"https://makerworld.com/es/search/models?keyword={search_term}"
        self.driver.get(url)
        
        try:
            # 1. Espera a que aparezcan los contenedores de los modelos
            # Usamos 'js-design-card' que es el selector real en el HTML que enviaste
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".js-design-card, [data-testid='design-card']"))
            )
            
            # 2. Scroll para cargar las imágenes y el contenido (Lazy Load)
            self.driver.execute_script("window.scrollTo(0, 800);")
            time.sleep(3)
            
            # 3. Obtenemos todas las tarjetas de modelos
            cards = self.driver.find_elements(By.CSS_SELECTOR, '.js-design-card, [data-testid="design-card"]')
            
            found_count = 0
            for card in cards:
                if found_count >= 3: # Límite de 3 resultados
                    break
                
                try:
                    # Extraer el enlace que contiene el TÍTULO (es el que tiene el atributo 'title')
                    # Esto evita el "Modelo sin nombre"
                    title_link = card.find_element(By.CSS_SELECTOR, "a[title][href*='/models/']")
                    name = title_link.get_attribute("title")
                    link = title_link.get_attribute("href")
                    
                    # Extraer la IMAGEN
                    img_src = "No disponible"
                    try:
                        img_elem = card.find_element(By.TAG_NAME, "img")
                        # Probamos primero el 'src' normal
                        img_src = img_elem.get_attribute("src")
                        
                        # Si el src es un placeholder (base64, blob o vacío), buscamos en 'data-src'
                        if not img_src or "base64" in img_src or "blob" in img_src:
                            data_src = img_elem.get_attribute("data-src")
                            if data_src:
                                img_src = data_src
                    except:
                        pass

                    if name and link:
                        self.results.append({
                            "Plataforma": "MakerWorld",
                            "Nombre": name,
                            "Imagen": img_src,
                            "Link": link
                        })
                        found_count += 1
                        
                except Exception:
                    # Si una tarjeta falla (ej. es un anuncio), pasamos a la siguiente
                    continue

        except Exception as e:
            print(f"Error crítico en MakerWorld: {e}")

    
    # NUEVO MÉTODO: Muestra los primeros 3 resultados por consola
    def mostrar_primeros_resultados(self):
        print("\n--- PRIMEROS 3 RESULTADOS POR PLATAFORMA ---")
        # Agrupamos por plataforma para mostrar 3 de cada una
        plataformas = ["Printables", "MakerWorld", "CrealityCloud"]
        for p in plataformas:
            print(f"\n>> {p}:")
            count = 0
            for res in self.results:
                if res["Plataforma"] == p and count < 3:
                    print(f"{count+1}. Nombre: {res['Nombre']}")
                    print(f"   Imagen: {res['Imagen']}")
                    count += 1
            if count == 0:
                print("   No se encontraron resultados.")

    def save_to_excel(self, filename):
        if self.results:
            df = pd.DataFrame(self.results)
            df.to_excel(filename, index=False)
            print(f"\nResultados totales guardados en {filename}")
        else:
            print("No hay datos para guardar.")

    def close(self):
        self.driver.quit()

# --- Ejecución ---
term = "macetas" 
scraper = ModelScraper()

scraper.scrape_printables(term)
scraper.scrape_makerworld(term)


# Llamada al nuevo método para ver los datos en consola
scraper.mostrar_primeros_resultados()

scraper.save_to_excel("modelos_3d_encontrados.xlsx")
scraper.close()