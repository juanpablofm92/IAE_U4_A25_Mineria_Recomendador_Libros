# Actividad 25: Recomendador de Libros por Reglas de Asociación

**Tecnológico Nacional de México**  
**Instituto Tecnológico Superior de Uruapan**  
**División de Estudios de Posgrado e Investigación**  
**Maestría en Inteligencia Artificial**  

* **Asignatura:** Inteligencia Artificial y su Ética  
* **Alumno:** Juan Pablo Figueroa Moran  
* **Matrícula:** M26040059  

---

## 📌 1. Descripción del Proyecto

Este proyecto implementa un **motor de recomendación de libros basado en reglas de asociación** utilizando el algoritmo Apriori de la librería `mlxtend`. 

A diferencia de los sistemas de filtrado colaborativo tipo "caja negra", las reglas de asociación proporcionan recomendaciones **100% explicables e interpretables** mediante implicaciones lógicas:
$$\{\text{Libro}_A, \text{Libro}_B\} \Longrightarrow \{\text{Libro}_C\}$$

### Función de Sugerencia Personalizada
La función `recomendar_libros(carrito_actual, top_n=3)` evalúa dinámicamente los ítems en posesión del usuario y sugiere los títulos más afines ordenados por la función objetivo de correlación:
$$\text{Score} = \text{Lift} \times \text{Confianza}$$

---

## 📊 2. Métrica de Evaluación: Precision@K

Se evalúa cuantitativamente la capacidad predictiva del sistema mediante **Precision@K (Hit-Rate@K)** sobre un conjunto de prueba de compras ocultando un elemento del carrito:
$$\text{Precision@K} = \frac{1}{|U|} \sum_{u \in U} \mathbb{I}(\text{Libro\_Oculto}_u \in \text{TopK}_u)$$

---

## 🚀 3. Instalación y Ejecución

```bash
pip install -r requirements.txt
python book_recommender.py
```

---

## ⚖️ 4. Consideraciones Éticas en Sistemas Recomendadores

1. **Burbuja de Filtro (*Filter Bubble*):** La recomendación exclusiva de títulos análogos a lecturas pasadas encierra a las personas en cámaras de eco ideológico.
2. **Diversidad y Serendipia:** Es indispensable introducir un factor de exploración ética que exponga a los lectores a nuevas corrientes de pensamiento y autores independientes.
