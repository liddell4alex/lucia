#include "lucia.h"

double **thermalChange(double **actual, double **next, double alpha, int rows, int cols) {
    const double dt = 0.1;
    const double dx = 1.0;
    const double dy = 1.0;

    // Modificando el interior de la matriz
    for(int i = 1; i < rows-1; i++) {
        for(int j = 1; j < cols-1; j++) {
            next[i][j] = actual[i][j] + alpha*dt*(
                (actual[i+1][j] - 2*actual[i][j] + actual[i-1][j]) / (dx*dx) +
                (actual[i][j+1] - 2*actual[i][j] + actual[i][j-1]) / (dy*dy)

            )
        }
    }

    // Modificando los bordes izquierdo y derecho de la matriz (bordes verticales. la aproximada para el eje y no se modifica)
    for(int i = 1; i < rows-1; i++) {
        // Izquierdo
        next[i][0] = actual[i][0] + alpha*dt*(
            (actual[0][0] - 2*actual[i][0] + actual[i-1][0]) / (dx*dx) +
            (actual[i][1] - actual[i][0]) / (dy*dy)
        )
        
        // Derecho
        next[i][cols-1] = actual[i][cols-1] + alpha*dt*(
            (actual[i+1][cols-1] - 2*actual[i][cols-1] + actual[i-1][cols-1]) / (dx*dx) +
            (actual[i][cols-2] - actual[i][cols-1]) / (dy*dy)
        )
    }
    
    // Modificando los bordes superior y inferior de la matriz (bordes horizontales. la aproximada para el eje y no se modifica)
    for(int i = 1; i < cols-1; i++) {
        // Superior
        next[0][i] = actual[0][i] + alpha*dt*(
            (actual[1][i] - actual[0][i]) / (dx*dx) +
            (actual[2][i] - 2*actual[1][] + actual[0][]) / (dy*dy)

        )
        
        // Inferior
        next[i][j] = actual[i][j] + alpha*dt*(
            (actual[i+1][j] - 2*actual[i][j] + actual[i-1][j]) / (dx*dx) +
            (actual[i][j+1] - 2*actual[i][j] + actual[i][j-1]) / (dy*dy)

        )
    }


    return next;
}