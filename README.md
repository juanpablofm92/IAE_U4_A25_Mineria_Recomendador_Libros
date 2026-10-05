# Actividad 25: Proyecto "Sistema de Recomendación Basado en Reglas de Asociación"

**Tecnológico Nacional de México**  
**Instituto Tecnológico Superior de Uruapan**  
**División de Estudios de Posgrado e Investigación**  
**Maestría en Inteligencia Artificial**  

* **Asignatura:** Inteligencia Artificial y su Ética (Unidad 4)  
* **Alumno:** Juan Pablo Figueroa Moran  
* **Matrícula:** M26040059  

---

## 🎯 Contexto y Desafíos del Proyecto

Desarrollo de un motor inteligente de recomendación para una **librería en línea**, diseñado para personalizar la experiencia de lectura de los usuarios mediante el descubrimiento de patrones de co-compra en cestas bibliográficas.

El proyecto resuelve tres desafíos fundamentales:
1. **Análisis de Compras:** Minería de patrones frecuentes para descubrir qué libros se adquieren conjuntamente (cálculo de Soporte, Confianza y *Lift*).
2. **Sistema de Recomendación:** Implementación del método `recomendar_libros(carrito_actual, top_n=3)`, que evalúa los títulos en el carrito y sugiere lecturas complementarias ponderadas por su fuerza de asociación ($\text{Score} = \text{Lift} \times \text{Confianza}$).
3. **Evaluación:** Medición cuantitativa de la efectividad del sistema recomendador mediante la métrica estandarizada **Precision@K** (*Hit-Rate@K* en evaluación *leave-one-out*).

---

## 📋 Resultados de los Desafíos

### Desafío 1: Patrones de Compra Descubiertos
* Se procesaron $2,000$ transacciones bibliográficas divididas en $80\%$ entrenamiento y $20\%$ evaluación.
* Se extrajeron más de $60$ reglas de asociación con *Lift* superior a $2.6\times$:
  * `['Hands-On ML'] → ['Deep Learning Book']`: Lift **$2.983$**, Confianza **$57.1\%$**
  * `['Python Crash Course'] → ['Pattern Recognition']`: Lift **$2.905$**, Confianza **$55.9\%$**
  * `['La República'] → ['El Contrato Social']`: Lift **$3.043$**, Confianza **$61.2\%$**
  * `['Dune'] → ['Fundación']`: Lift **$2.740$**, Confianza **$57.9\%$**

### Desafío 2: Demostración del Sistema de Recomendación
Al consultar carritos de prueba:
* **Carrito:** `['Python Crash Course', 'Hands-On ML']`
  * Recomendación 1: *Deep Learning Book* (Score $1.703$)
  * Recomendación 2: *Pattern Recognition* (Score $1.624$)
  * Recomendación 3: *Clean Code* (Score $1.589$)
* **Carrito:** `['Dune']`
  * Recomendación 1: *Fundación* (Score $1.586$)
  * Recomendación 2: *Hyperion* (Score $1.512$)
  * Recomendación 3: *Neuromante* (Score $1.467$)

### Desafío 3: Evaluación de Efectividad (Precision@K)
Evaluado sobre el conjunto ciego de prueba ($400$ carritos independientes):
* **Precision@1 (Hit-Rate@1):** **$35.27\%$**
* **Precision@3 (Hit-Rate@3):** **$86.64\%$**
* **Precision@5 (Hit-Rate@5):** **$89.38\%$**

---

## 📂 Estructura del Repositorio

```text
IAE_U4_A25_Mineria_Recomendador_Libros/
├── book_recommender.py       # Motor de minería, recomendación y evaluación Precision@K
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Documentación técnica completa
```

---

## 🚀 Instrucciones de Ejecución

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar motor de minería, recomendaciones y cálculo de métricas
python book_recommender.py
```

---

## ⚖️ Consideraciones Éticas en Sistemas Recomendadores

1. **Ruptura de la "Burbuja de Filtro" (*Filter Bubble*):** Los sistemas basados exclusivamente en afinidades pasadas pueden aislar ideológicamente al lector. El sistema debe inyectar un factor de diversidad bibliográfica para estimular el pensamiento crítico.
2. **Equidad para Autores Independientes:** Evitar la monopolización algorítmica de los *bestsellers* mediante penalización logarítmica de popularidad, otorgando visibilidad a títulos minoritarios.
3. **Explicabilidad Algorítmica:** Cada sugerencia presenta al usuario la regla de origen clara (*"Recomendado porque compraste X"*), respetando la autonomía de decisión del comprador.
