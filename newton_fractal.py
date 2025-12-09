"""
Newton Fractal Generator
========================
Genera frattali di Newton ad alta risoluzione per la funzione f(z) = z³ - 1

Il frattale mostra a quale delle tre radici complesse dell'unità converge
il metodo di Newton partendo da ogni punto del piano complesso.

Autore: Python Scientific Expert
Corso: Analisi 1 - Derivate e Metodo di Newton
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def newton_fractal(width=3840, height=2160, max_iter=80, bound=2.0):
    """
    Genera un frattale di Newton per f(z) = z³ - 1 con shading artistico
    
    Parametri:
    ----------
    width : int
        Larghezza dell'immagine in pixel (default 4K: 3840)
    height : int
        Altezza dell'immagine in pixel (default 4K: 2160)
    max_iter : int
        Numero massimo di iterazioni del metodo di Newton
    bound : float
        Limite del piano complesso da visualizzare (da -bound a +bound)
    
    Returns:
    --------
    tuple(numpy.ndarray, numpy.ndarray)
        (convergence, iterations) - Radice di convergenza e numero iterazioni per shading
    """
    
    # ============================================================
    # STEP 1: Creazione della griglia di numeri complessi
    # ============================================================
    # Creiamo una griglia nel piano complesso dove ogni pixel rappresenta
    # un punto di partenza z₀ per il metodo di Newton
    
    # Coordinate reali (asse x) e immaginarie (asse y)
    x = np.linspace(-bound, bound, width)
    y = np.linspace(-bound, bound, height)
    
    # meshgrid crea matrici 2D dalle coordinate 1D
    # X contiene le coordinate x ripetute per ogni riga
    # Y contiene le coordinate y ripetute per ogni colonna
    X, Y = np.meshgrid(x, y)
    
    # Combinazione in numeri complessi: z = x + iy
    # Ogni elemento della matrice Z è un numero complesso
    Z = X + 1j * Y
    
    # ============================================================
    # STEP 2: Definizione delle radici di z³ - 1 = 0
    # ============================================================
    # Le tre radici cubiche dell'unità (soluzioni di z³ = 1)
    # Queste sono distribuite uniformemente su un cerchio nel piano complesso
    roots = np.array([
        1,                                    # radice reale: z₁ = 1
        np.exp(2j * np.pi / 3),              # z₂ = e^(i·2π/3) = -1/2 + i√3/2
        np.exp(4j * np.pi / 3)               # z₃ = e^(i·4π/3) = -1/2 - i√3/2
    ])
    
    # ============================================================
    # STEP 3: Applicazione vettorizzata del Metodo di Newton
    # ============================================================
    # Il metodo di Newton itera la formula:
    #   z_{n+1} = z_n - f(z_n) / f'(z_n)
    #
    # Per f(z) = z³ - 1:
    #   f(z) = z³ - 1
    #   f'(z) = 3z²
    #
    # Quindi:
    #   z_{n+1} = z_n - (z_n³ - 1) / (3z_n²)
    #   z_{n+1} = z_n - z_n³/(3z_n²) + 1/(3z_n²)
    #   z_{n+1} = z_n - z_n/3 + 1/(3z_n²)
    #   z_{n+1} = (2z_n)/3 + 1/(3z_n²)
    #
    # Forma alternativa semplificata:
    #   z_{n+1} = (2z_n³ + 1) / (3z_n²)
    
    # Matrice per memorizzare a quale radice converge ogni pixel
    # Inizialmente tutti i pixel sono impostati a -1 (non ancora assegnati)
    convergence = np.zeros(Z.shape, dtype=int) - 1
    
    # ============================================================
    # NOVITÀ: Tracciamento delle iterazioni per effetto 3D
    # ============================================================
    # Memorizziamo quante iterazioni sono necessarie per convergere
    # Questo crea un effetto di "profondità" dove convergenze rapide
    # appaiono diverse da quelle lente, simulando rilievo/ombreggiatura
    iterations = np.full(Z.shape, max_iter, dtype=float)
    
    # Iterazione del metodo di Newton
    # Applichiamo la formula a TUTTI i pixel simultaneamente (vettorizzazione!)
    for iteration in range(max_iter):
        # Formula di Newton: z_{n+1} = z_n - f(z_n) / f'(z_n)
        # Con f(z) = z³ - 1 e f'(z) = 3z²
        
        # Calcoliamo f(z) = z³ - 1 per ogni pixel
        f_z = Z**3 - 1
        
        # Calcoliamo f'(z) = 3z² per ogni pixel
        f_prime_z = 3 * Z**2
        
        # Evitiamo divisioni per zero sostituendo gli zeri con un valore molto piccolo
        f_prime_z = np.where(np.abs(f_prime_z) < 1e-10, 1e-10, f_prime_z)
        
        # Applichiamo un'iterazione del metodo di Newton a tutti i pixel
        Z_new = Z - f_z / f_prime_z
        
        # ============================================================
        # STEP 4: Controllo della convergenza
        # ============================================================
        # Per ogni pixel, verifichiamo se è sufficientemente vicino a una radice
        
        # Calcoliamo la distanza da ciascuna delle tre radici
        for idx, root in enumerate(roots):
            # Distanza di ogni pixel dalla radice corrente
            distance = np.abs(Z_new - root)
            
            # Se un pixel è molto vicino a questa radice (entro tolleranza)
            # e non è ancora stato assegnato, lo assegniamo a questa radice
            mask = (distance < 1e-3) & (convergence == -1)
            convergence[mask] = idx
            
            # NOVITÀ: Memorizziamo l'iterazione di convergenza per lo shading
            # Più basso = convergenza veloce (zone chiare)
            # Più alto = convergenza lenta (zone scure/profonde)
            iterations[mask] = iteration
        
        # Aggiorna Z per la prossima iterazione
        Z = Z_new
    
    # ============================================================
    # STEP 5: Preparazione dati per colorazione artistica avanzata
    # ============================================================
    # I pixel che non hanno converso (rimasti -1) vengono settati a 3
    # per avere un colore di sfondo distinto
    convergence[convergence == -1] = 3
    
    return convergence, iterations


def plot_fractal(convergence, iterations, save_path='newton_fractal_4k.png', dpi=300):
    """
    Visualizza e salva il frattale di Newton con effetto 3D professionale
    
    Parametri:
    ----------
    convergence : numpy.ndarray
        Array 2D con i valori di convergenza (a quale radice)
    iterations : numpy.ndarray
        Array 2D con il numero di iterazioni (per shading/profondità)
    save_path : str
        Percorso dove salvare l'immagine
    dpi : int
        Risoluzione dell'immagine salvata (dots per inch)
    """
    
    # ============================================================
    # STEP 1: Creazione del campo colorato con effetto profondità
    # ============================================================
    # Normalizziamo le iterazioni per creare un gradiente di luminosità
    # Convergenze rapide → luminose (in alto)
    # Convergenze lente → scure (in profondità)
    
    # Normalizzazione logaritmica per migliore distribuzione visiva
    iterations_normalized = np.log(iterations + 1) / np.log(iterations.max() + 1)
    
    # Invertiamo: convergenze veloci = valori alti (più luminose)
    depth = 1.0 - iterations_normalized
    
    # Applichiamo contrasto aumentato per effetto drammatico
    depth = np.power(depth, 0.7)  # Gamma correction per maggiore dinamica
    
    # ============================================================
    # STEP 2: Palette elegante scura/neon professionale
    # ============================================================
    # Definiamo colori base per ciascuna radice con tonalità neon/oro
    base_colors = np.array([
        [1.0, 0.84, 0.0],    # Oro brillante per radice z₁ = 1
        [0.0, 0.9, 1.0],     # Ciano elettrico per radice z₂
        [1.0, 0.2, 0.6],     # Magenta neon per radice z₃
        [0.05, 0.05, 0.08]   # Nero profondo per non convergenza
    ])
    
    # Creiamo un'immagine RGB combinando convergenza (colore) e iterazioni (luminosità)
    height, width = convergence.shape
    image = np.zeros((height, width, 3))
    
    # Per ogni pixel, assegniamo il colore base modulato dalla profondità
    for i in range(4):  # 3 radici + 1 per non convergenza
        mask = (convergence == i)
        for channel in range(3):
            # Il colore finale è: colore_base * intensità_profondità
            # Questo crea l'effetto tridimensionale con ombreggiatura
            image[:, :, channel][mask] = base_colors[i, channel] * depth[mask]
    
    # ============================================================
    # STEP 3: Post-processing per look professionale
    # ============================================================
    # Aggiungiamo un leggero boost ai neri per contrasto aumentato
    image = np.power(image, 0.9)  # Slight darkening per look più drammatico
    
    # ============================================================
    # STEP 4: Visualizzazione e salvataggio 4K
    # ============================================================
    fig = plt.figure(figsize=(19.2, 10.8), facecolor='#000000')  # 4K aspect ratio
    ax = fig.add_axes([0, 0, 1, 1])  # Rimuove margini per clean export
    ax.axis('off')
    
    # Mostra l'immagine RGB con interpolazione di qualità
    ax.imshow(image, interpolation='bilinear', extent=[-2, 2, -2, 2], origin='lower')
    
    # ============================================================
    # Salvataggio ultra-qualità
    # ============================================================
    print(f"💾 Salvando immagine 4K in '{save_path}' con {dpi} DPI...")
    plt.savefig(save_path, dpi=dpi, facecolor='#000000', 
                edgecolor='none', bbox_inches='tight', pad_inches=0)
    print(f"✅ Generative Art salvata con successo!")
    
    # Visualizzazione con UI minimalista
    print("🎨 Visualizzazione del capolavoro frattale...")
    plt.show()
    plt.close()


def main():
    """
    Funzione principale che orchestra la generazione del frattale artistico
    """
    print("=" * 70)
    print("🎨 NEWTON FRACTAL - PROFESSIONAL GENERATIVE ART GENERATOR")
    print("=" * 70)
    print("📐 Funzione Matematica: f(z) = z³ - 1")
    print("📊 Algoritmo: Newton-Raphson vettorizzato (NumPy)")
    print("✨ Caratteristiche: 4K + Depth Shading + Palette Neon/Oro")
    print("=" * 70)
    print()
    
    # Parametri di configurazione 4K
    WIDTH = 3840        # Risoluzione 4K orizzontale
    HEIGHT = 2160       # Risoluzione 4K verticale
    MAX_ITER = 80       # Iterazioni aumentate per dettaglio extra
    BOUND = 2.0         # Limiti del piano complesso
    DPI = 300           # Risoluzione professionale per stampa
    
    print(f"⚙️  Configurazione Ultra-Alta Qualità:")
    print(f"   • Risoluzione: {WIDTH}x{HEIGHT} pixel (4K UHD)")
    print(f"   • Iterazioni: {MAX_ITER} (maggiore dettaglio)")
    print(f"   • Effetti: Depth Shading 3D + Palette Elegante")
    print(f"   • Range: [{-BOUND}, {BOUND}] + [{-BOUND}, {BOUND}]i")
    print()
    
    # Genera il frattale con dati di profondità
    print("🚀 Generazione in corso (può richiedere 10-20 secondi)...")
    convergence, iterations = newton_fractal(width=WIDTH, height=HEIGHT, 
                                             max_iter=MAX_ITER, bound=BOUND)
    print("✨ Frattale 4K generato con successo!")
    print()
    
    # Visualizza e salva con qualità professionale
    plot_fractal(convergence, iterations, 
                 save_path='newton_fractal_4k.png', dpi=DPI)
    
    print()
    print("=" * 70)
    print("🎉 GENERATIVE ART COMPLETATA!")
    print("=" * 70)
    print()
    print("🎭 Interpretazione Artistica:")
    print("   • Oro/Ciano/Magenta: Le tre radici cubiche dell'unità")
    print("   • Luminosità: Velocità di convergenza (effetto 3D)")
    print("   • Struttura frattale: Caos deterministico alle frontiere")
    print("   • Output: newton_fractal_4k.png (pronto per stampa/galleria)")
    print()


if __name__ == "__main__":
    main()
