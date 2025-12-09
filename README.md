# Newton Fractal Generator 🎨

Un progetto Python che genera frattali di Newton ad alta risoluzione, dimostrando visivamente la bellezza matematica della convergenza del metodo di Newton nel piano complesso.

## 📐 Concetto Matematico

Il **Frattale di Newton** è una visualizzazione del comportamento del metodo di Newton-Raphson applicato a numeri complessi. Questo script usa la funzione:

$$f(z) = z^3 - 1$$

Le tre radici complesse dell'equazione $z^3 = 1$ sono:
- $z_1 = 1$
- $z_2 = e^{i\frac{2\pi}{3}} = -\frac{1}{2} + i\frac{\sqrt{3}}{2}$
- $z_3 = e^{i\frac{4\pi}{3}} = -\frac{1}{2} - i\frac{\sqrt{3}}{2}$

### Metodo di Newton

La formula iterativa del metodo di Newton è:

$$z_{n+1} = z_n - \frac{f(z_n)}{f'(z_n)}$$

Per la nostra funzione:
- $f(z) = z^3 - 1$
- $f'(z) = 3z^2$

Quindi:

$$z_{n+1} = z_n - \frac{z_n^3 - 1}{3z_n^2}$$

Ogni pixel nel piano complesso rappresenta un punto di partenza $z_0$. Il colore del pixel indica a quale radice il metodo converge partendo da quel punto.

## 🚀 Installazione

```bash
pip install -r requirements.txt
```

## ▶️ Esecuzione

```bash
python newton_fractal.py
```

Lo script genererà:
1. Una visualizzazione interattiva del frattale
2. Un'immagine salvata come `newton_fractal.png` ad alta risoluzione

## 🎨 Output

L'immagine mostra tre regioni di colori diversi, una per ogni radice. I confini tra queste regioni hanno una struttura frattale infinitamente complessa, rivelando la natura caotica della convergenza del metodo di Newton.

## 🔧 Tecnologie

- **NumPy**: Calcoli vettoriali ad alte prestazioni (niente cicli for!)
- **Matplotlib**: Visualizzazione e salvataggio dell'immagine

## 📚 Contesto Didattico

Questo progetto dimostra concetti di **Analisi 1**:
- Derivate di funzioni complesse
- Metodo di Newton-Raphson
- Convergenza e divergenza
- Dinamic systems nel piano complesso

---

*Creato come dimostrazione della bellezza dell'analisi matematica applicata all'arte computazionale.*
