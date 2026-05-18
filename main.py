import os
import math
import matplotlib.pyplot as plt

# ==========================================
# 1. FUNCIONES DEL ALGORTIMO DIVIDE Y VENCERÁS
# ==========================================

def distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def fuerza_bruta(puntos):
    min_dist = float('inf')
    par_cercano = None
    n = len(puntos)
    for i in range(n):
        for j in range(i + 1, n):
            d = distancia(puntos[i], puntos[j])
            if d < min_dist:
                min_dist = d
                par_cercano = (puntos[i], puntos[j])
    return min_dist, par_cercano

def franja_mas_cercano(franja, delta, par_actual):
    min_dist = delta
    mejor_par = par_actual
    franja.sort(key=lambda punto: punto[1]) 
    
    n = len(franja)
    for i in range(n):
        for j in range(i + 1, n):
            if (franja[j][1] - franja[i][1]) >= min_dist:
                break
            d = distancia(franja[i], franja[j])
            if d < min_dist:
                min_dist = d
                mejor_par = (franja[i], franja[j])
                
    return min_dist, mejor_par

def par_cercano_recursivo(puntos_x):
    n = len(puntos_x)
    if n <= 3:
        return fuerza_bruta(puntos_x)
    
    mitad = n // 2
    punto_medio = puntos_x[mitad]
    
    izq = puntos_x[:mitad]
    der = puntos_x[mitad:]
    
    dl, par_l = par_cercano_recursivo(izq)
    dr, par_r = par_cercano_recursivo(der)
    
    if dl < dr:
        delta = dl
        mejor_par = par_l
    else:
        delta = dr
        mejor_par = par_r
    
    franja = [p for p in puntos_x if abs(p[0] - punto_medio[0]) < delta]
    d_franja, par_franja = franja_mas_cercano(franja, delta, mejor_par)
    
    if d_franja < delta:
        return d_franja, par_franja
    else:
        return delta, mejor_par

def buscar_par_mas_cercano(puntos):
    puntos_ordenados = sorted(puntos, key=lambda punto: punto[0])
    return par_cercano_recursivo(puntos_ordenados)

# ==========================================
# 2. LECTURA DE LOS DATOS DESDE ARCHIVO
# ==========================================

def cargar_datos(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        print(f"\n[Error] El archivo '{nombre_archivo}' no se encuentra en el directorio actual.")
        return None
        
    with open(nombre_archivo, 'r') as f:
        # Se lee absolutamente todo el contenido del archivo como una sola cadena
        contenido = f.read()
        
        # Se reemplazan saltos de línea por comas y limpiamos espacios vacíos
        contenido = contenido.replace('\n', ',').replace('\t', ',')
        # Se separan todos los números usando las comas como referencia
        valores_limpios = [v.strip() for v in contenido.split(',') if v.strip()]
        
    # Se convierten los fragmentos a números flotantes
    numeros = [float(x) for x in valores_limpios]
    
    # Se agrupan secuencialmente los números de dos en dos para formar coordenadas (X, Y)
    puntos = []
    for i in range(0, len(numeros) - 1, 2):
        puntos.append((numeros[i], numeros[i+1]))
        
    return puntos

def menu_seleccion():
    print("="*50)
    print("  ENCONTRAR EL PAR DE PUNTOS MÁS CERCANO.")
    print("="*50)
    print("Selecciona el archivo para encontrar par mas cercano:")
    print("1. datos_100.txt")
    print("2. datos_1000.txt")
    print("3. datos_10000.txt")
    print("4. Salir")
    print("="*50)
    
    opcion = input("Ingresa el número de tu opción (1-4): ").strip()
    
    if opcion == '1': return "datos_100.txt"
    elif opcion == '2': return "datos_1000.txt"
    elif opcion == '3': return "datos_10000.txt"
    elif opcion == '4': return None
    else:
        print("Opción inválida. Intenta de nuevo.\n")
        return menu_seleccion()

# ==========================================
# 3. FUNCIÓN DE GRAFICACIÓN DE RESULTADOS CON MATPLOTLIB
# ==========================================

def graficar_resultado(puntos, par_cercano, distancia_min, nombre_archivo):
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(13, 7))
    
    x_puntos = [p[0] for p in puntos]
    y_puntos = [p[1] for p in puntos]
    
    puntos_ordenados = sorted(puntos, key=lambda p: p[0])
    mitad = len(puntos_ordenados) // 2
    x_division = puntos_ordenados[mitad][0]
    
    # Se ajusta la densidad visual según el volumen real de datos cargados
    total_puntos = len(puntos)
    if total_puntos <= 100:
        tamano_punto = 35
        opacidad = 0.85
    elif total_puntos <= 1000:
        tamano_punto = 18
        opacidad = 0.75
    else: 
        tamano_punto = 8
        opacidad = 0.60

    # 1. Se dibuja la nube completa de puntos
    ax.scatter(x_puntos, y_puntos, color='#7ec8e3', s=tamano_punto, alpha=opacidad, zorder=2, label='Puntos de Datos (azules)')
    
    # 2. Se dibuja línea central divisoria
    ax.axvline(x=x_division, color='#2ca02c', linestyle='--', linewidth=1.2, zorder=1, label='División D&C (verde dashed)')
    
    # 3. Se dibuja la franja central (Strip)
    ax.axvspan(x_division - distancia_min, x_division + distancia_min, 
               color='#2ca02c', alpha=0.15, zorder=1, label='Franja Central (verde sombreado)')
    
    # 4. Se resalta el par de puntos más cercano
    if par_cercano:
        p1, p2 = par_cercano
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='#ffcc00', linewidth=2.5, zorder=5, label='Par Más Cercano')
        ax.scatter([p1[0], p2[0]], [p1[1], p2[1]], color='#ff3333', s=250, alpha=0.4, zorder=5)
        ax.scatter([p1[0], p2[0]], [p1[1], p2[1]], color='#7ec8e3', s=40, edgecolors='white', linewidths=1, zorder=6)
        
        punto_medio_par = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
        ax.annotate('Par Más Cercano', 
                    xy=punto_medio_par, 
                    xytext=(punto_medio_par[0] + (distancia_min * 1.5) + 5, punto_medio_par[1] + (distancia_min * 1.5) + 5),
                    arrowprops=dict(arrowstyle="->", color="white", connectionstyle="arc3,rad=.1"),
                    color='white', fontsize=10)

    # Para que el grafico quede escalado y con márgenes adecuados, se ajustan los límites del eje y la relación de aspecto
    ax.set_aspect('auto')
    margin_x = (max(x_puntos) - min(x_puntos)) * 0.08
    margin_y = (max(y_puntos) - min(y_puntos)) * 0.08
    ax.set_xlim(min(x_puntos) - margin_x, max(x_puntos) + margin_x)
    ax.set_ylim(min(y_puntos) - margin_y, max(y_puntos) + margin_y)

    ax.text(0.97, 0.95, f"Distancia: {distancia_min:.4f} unidades", 
            transform=ax.transAxes, color='white', fontsize=10, ha='right', va='top')

    ax.set_title(f"Visualización Completa: {nombre_archivo} ({total_puntos} puntos)", fontsize=14, pad=15)
    ax.set_xlabel("Eje X", fontsize=11)
    ax.set_ylabel("Eje Y", fontsize=11)
    ax.grid(True, linestyle='-', color='#ffffff', alpha=0.12, zorder=0)
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    plt.show()

# ==========================================
# 4. PROGRAMA DEEJECUCIÓN PRINCIPAL
# ==========================================

if __name__ == "__main__":
    archivo_elegido = menu_seleccion()
    
    if archivo_elegido:
        print(f"\n[1/3] Cargando coordenadas desde '{archivo_elegido}'...")
        datos = cargar_datos(archivo_elegido)
        
        if datos:
            print(f"[2/3] Procesando {len(datos)} puntos mediante Divide y Vencerás...")
            dist_minima, par_optimo = buscar_par_mas_cercano(datos)
            
            print("\n" + "="*40)
            print("         RESULTADOS ANALÍTICOS")
            print("="*40)
            print(f" Distancia mínima: {dist_minima:.6f}")
            print(f" Punto 1: {par_optimo[0]}")
            print(f" Punto 2: {par_optimo[1]}")
            print("="*40)
            
            print("\n[3/3] Generando interfaz gráfica. Por favor espera...")
            graficar_resultado(datos, par_optimo, dist_minima, archivo_elegido)