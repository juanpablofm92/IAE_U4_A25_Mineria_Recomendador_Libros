"""
=============================================================================
TECNOLÓGICO NACIONAL DE MÉXICO - INSTITUTO TECNOLÓGICO SUPERIOR DE URUAPAN
DIVISIÓN DE ESTUDIOS DE POSGRADO E INVESTIGACIÓN
MAESTRÍA EN INTELIGENCIA ARTIFICIAL

Materia: Inteligencia Artificial y su Ética
Actividad 25: Minería de Datos - Sistema Recomendador de Libros por Reglas de Asociación
Alumno: Juan Pablo Figueroa Moran (Matrícula: M26040059)
=============================================================================
"""

import sys
import random
import numpy as np
import pandas as pd
from typing import List, Set, Dict, Tuple, Any

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from mlxtend.preprocessing import TransactionEncoder
    from mlxtend.frequent_patterns import apriori, association_rules
except ImportError:
    TransactionEncoder = None


def generar_transacciones_libreria(n_compras: int = 1500, random_seed: int = 42) -> List[List[str]]:
    """
    Genera un historial sintético de compras de libros estructurado por afinidades temáticas:
    - Inteligencia Artificial: Clean Code, Python Crash Course, Deep Learning (Goodfellow), Pattern Recognition (Bishop), Hands-On ML (Geron)
    - Ciencia Ficción: Dune, Fundacion, Neuromante, Fahrenheit 451, Hyperion
    - Filosofía y Ética: La Republica, Etica a Nicomaco, Mas alla del bien y del mal, El contrato social, Meditaciones
    """
    random.seed(random_seed)
    
    clusters_libros = [
        # AI & Data Science
        ["Python Crash Course", "Hands-On ML", "Deep Learning Book", "Pattern Recognition", "Clean Code"],
        # Sci-Fi
        ["Dune", "Fundacion", "Neuromante", "Fahrenheit 451", "Hyperion"],
        # Filosofía & Ética
        ["Meditaciones", "La Republica", "Etica a Nicomaco", "Mas alla del bien y del mal", "El Contrato Social"]
    ]

    otros_libros = ["Sapiens", "El Principito", "1984", "Cien Anos de Soledad", "Breve Historia del Tiempo"]

    dataset = []
    for _ in range(n_compras):
        canasta = set()
        # Seleccionar un clúster temático primario
        cluster_elegido = random.choice(clusters_libros)
        k = random.randint(2, min(4, len(cluster_elegido)))
        canasta.update(random.sample(cluster_elegido, k))

        # Posibilidad de libro de interés general
        if random.random() < 0.25:
            canasta.add(random.choice(otros_libros))

        dataset.append(sorted(list(canasta)))
    
    return dataset


class RecomendadorLibrosPorReglas:
    def __init__(self, min_support: float = 0.05, min_confidence: float = 0.40):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.reglas_df = pd.DataFrame()
        self.catalogo_global: Set[str] = set()

    def entrenar(self, transacciones: List[List[str]]):
        for t in transacciones:
            self.catalogo_global.update(t)

        if TransactionEncoder is not None:
            te = TransactionEncoder()
            te_ary = te.fit(transacciones).transform(transacciones)
            df_onehot = pd.DataFrame(te_ary, columns=te.columns_)

            itemsets = apriori(df_onehot, min_support=self.min_support, use_colnames=True)
            if len(itemsets) == 0:
                print("[!] No se generaron itemsets frecuentes con el soporte dado.")
                return

            reglas = association_rules(itemsets, metric="confidence", min_threshold=self.min_confidence)
            reglas["antecedents_set"] = reglas["antecedents"].apply(set)
            reglas["consequents_set"] = reglas["consequents"].apply(set)
            self.reglas_df = reglas.sort_values(by=["lift", "confidence"], ascending=[False, False])
            print(f"[*] Modelo entrenado con mlxtend: {len(self.reglas_df)} reglas de asociación.")
        else:
            print("[*] 'mlxtend' no disponible. Usando motor nativo de reglas de asociación...")
            from collections import defaultdict
            N = len(transacciones)
            item_counts = defaultdict(int)
            for t in transacciones:
                for item in set(t):
                    item_counts[item] += 1
            freq_1 = {item: count / N for item, count in item_counts.items() if count / N >= self.min_support}

            pair_counts = defaultdict(int)
            for t in transacciones:
                items_en_t = [item for item in set(t) if item in freq_1]
                for i in range(len(items_en_t)):
                    for j in range(i + 1, len(items_en_t)):
                        pair = tuple(sorted([items_en_t[i], items_en_t[j]]))
                        pair_counts[pair] += 1

            rows = []
            for (item_a, item_b), count in pair_counts.items():
                supp_ab = count / N
                if supp_ab >= self.min_support:
                    # A -> B
                    conf_ab = supp_ab / freq_1[item_a]
                    lift_ab = conf_ab / freq_1[item_b]
                    if conf_ab >= self.min_confidence:
                        rows.append({
                            "antecedents_set": {item_a},
                            "consequents_set": {item_b},
                            "support": supp_ab,
                            "confidence": conf_ab,
                            "lift": lift_ab
                        })
                    # B -> A
                    conf_ba = supp_ab / freq_1[item_b]
                    lift_ba = conf_ba / freq_1[item_a]
                    if conf_ba >= self.min_confidence:
                        rows.append({
                            "antecedents_set": {item_b},
                            "consequents_set": {item_a},
                            "support": supp_ab,
                            "confidence": conf_ba,
                            "lift": lift_ba
                        })
            self.reglas_df = pd.DataFrame(rows)
            if not self.reglas_df.empty:
                self.reglas_df = self.reglas_df.sort_values(by=["lift", "confidence"], ascending=[False, False])
            print(f"[*] Modelo entrenado (motor nativo): {len(self.reglas_df)} reglas de asociación descubiertas.")

    def recomendar_libros(self, carrito_actual: List[str], top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Dada una lista de libros en el carrito, busca las reglas cuyos antecedentes
        sean un subconjunto del carrito y no hayan sido comprados aún.
        Ordena por Lift y Confianza.
        """
        carrito_set = set(carrito_actual)
        candidatos = {}

        if self.reglas_df.empty:
            return []

        for _, row in self.reglas_df.iterrows():
            antecedente = row["antecedents_set"]
            consecuente = row["consequents_set"]

            # Si el antecedente está contenido íntegramente en el carrito
            if antecedente.issubset(carrito_set):
                # Libros consecuentes que aún no están en el carrito
                libros_nuevos = consecuente - carrito_set
                for libro in libros_nuevos:
                    score = row["lift"] * row["confidence"]
                    if libro not in candidatos or score > candidatos[libro]["score"]:
                        candidatos[libro] = {
                            "libro": libro,
                            "lift": round(float(row["lift"]), 3),
                            "confianza": round(float(row["confidence"]), 3),
                            "soporte": round(float(row["support"]), 4),
                            "score": round(float(score), 4),
                            "regla_origen": f"{list(antecedente)} -> {libro}"
                        }

        # Ordenar por score combinado (Lift * Confianza)
        ranking = sorted(candidatos.values(), key=lambda x: x["score"], reverse=True)
        return ranking[:top_n]

    def evaluar_precision_en_k(self, test_transacciones: List[List[str]], k: int = 3) -> float:
        """
        Evalúa Precision@K: Oculta 1 libro del carrito del usuario, genera recomendaciones
        Top-K a partir de los libros restantes y evalúa si el libro oculto fue recomendado.
        """
        aciertos = 0
        total_evaluados = 0

        for trans in test_transacciones:
            if len(trans) < 3:
                continue
            
            # Ocultar 1 libro al azar como 'ground truth'
            idx_oculto = random.randint(0, len(trans) - 1)
            libro_ground_truth = trans[idx_oculto]
            carrito_parcial = [item for i, item in enumerate(trans) if i != idx_oculto]

            recs = self.recomendar_libros(carrito_parcial, top_n=k)
            libros_recomendados = [r["libro"] for r in recs]

            if libro_ground_truth in libros_recomendados:
                aciertos += 1
            total_evaluados += 1

        if total_evaluados == 0:
            return 0.0

        return aciertos / total_evaluados


def main():
    print("=" * 75)
    print("  TECNM / ITSU - RECOMENDADOR DE LIBROS POR REGLAS DE ASOCIACIÓN")
    print("=" * 75)

    transacciones = generar_transacciones_libreria(n_compras=2000, random_seed=42)
    # Partición 80% train, 20% test
    n_train = int(len(transacciones) * 0.8)
    train_trans = transacciones[:n_train]
    test_trans = transacciones[n_train:]
    print(f"[*] Total transacciones: {len(transacciones)} ({len(train_trans)} train, {len(test_trans)} test).")

    recomendador = RecomendadorLibrosPorReglas(min_support=0.04, min_confidence=0.45)
    recomendador.entrenar(train_trans)

    # 1. Prueba de recomendación con carritos muestra
    carritos_prueba = [
        ["Python Crash Course", "Hands-On ML"],
        ["Dune"],
        ["La Republica", "Etica a Nicomaco"]
    ]

    print("\n--- DEMOSTRACIÓN DE RECOMENDACIONES TOP-3 ---")
    for car in carritos_prueba:
        print(f"\n🛒 Carrito actual del cliente: {car}")
        recs = recomendador.recomendar_libros(car, top_n=3)
        if recs:
            for idx, r in enumerate(recs, 1):
                print(f"   {idx}. 📖 {r['libro']} (Lift: {r['lift']}, Confianza: {r['confianza']*100:.1f}%)")
                print(f"      Basado en: {r['regla_origen']}")
        else:
            print("   [!] No se encontraron reglas de alta confianza para este patrón.")

    # 2. Evaluación de Métrica Precision@K
    print("\n" + "=" * 75)
    print("  EVALUACIÓN CUANTITATIVA DEL MOTOR DE RECOMENDACIÓN")
    print("=" * 75)
    for k_val in [1, 3, 5]:
        p_at_k = recomendador.evaluar_precision_en_k(test_trans, k=k_val)
        print(f"  * Métrica Hit-Rate / Precision@{k_val} en conjunto de prueba: {p_at_k*100:.2f}%")

    print("\n" + "=" * 75)
    print("  CONSIDERACIONES ÉTICAS EN SISTEMAS RECOMENDADORES")
    print("=" * 75)
    print("""
    1. Efecto Cámara de Eco / Burbuja de Filtro: Los recomendadores basados en reglas
       frecuentes tienden a encerrar al lector en un mismo género temático, reduciendo
       la serendipia, el pensamiento crítico y la diversidad bibliográfica.
    2. Monopolización de Títulos Populares: Los libros de mayor venta (*bestsellers*)
       acumulan soporte artificialmente alto, invisibilizando a autores emergentes o minoritarios.
    3. Transparencia Algorítmica: Ofrecer explicaciones claras ('Te recomendamos X porque
       compraste Y') respeta el derecho del usuario a una toma de decisión informada.
    """)


if __name__ == "__main__":
    main()
