import matplotlib.pyplot as plt

# Formo la matriz
with open("matriz.txt") as archivo:
    matriz = []

    for fila in archivo:
        nums = fila.split()
        nums = list(map(int, nums))
        matriz.append(nums) 
    
# Busco el hongo y las hifas
hongo = None
hifas = []

# Itero por la matriz
for i in range(len(matriz)):
    for j in range(len(matriz[i])):
        val = matriz[i][j]

        if val == 1:                    # Si encuentro el hongo almaceno su posicion
            hongo = (i, j)

        elif val > 1:                   # Si es hifa (val > 1)
            hifas.append((val, i, j))

# Ordeno las hifas
hifas.sort()

# Inicializo coordenadas
x = [hongo[1]]
y = [hongo[0]]

# Agrego las coordenadas de las hifas
for val, fil, col in hifas:
    x.append(col)
    y.append(fil)

# Graficar
plt.plot(x, y, "g-")
plt.scatter(hongo[1], hongo[0], color="red")
plt.scatter(x, y, color="green", s=10)
plt.gca().invert_yaxis()
plt.axis("off")
plt.show()
