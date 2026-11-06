#include <stdio.h>

#include "lucia.h"

int main(int argn, char* args[]) {
    // Dimensiones
    int rows = 3, cols = 3;
   
    // Difusibidad termica (qué material es)
    double alpha = 0.1;

    // Temperatura inicial de la placa
    double T0 = 25.0;

    // Temperatura y posición de la fuente de calor
    double Th = 100.0;
    int sourceRow = 1;
    int sourceCol = 1;

    // Matriz de temperaturas actual y siguiente
    double **actual = makeMatrix(rows, cols);
    double **next = makeMatrix(rows, cols);

    if(actual == NULL || next == NULL) {
        fprintf(stdout, "Fallo la asignación de memoria\n");
        freeMatrix(actual, rows);
        freeMatrix(next, rows);
        
        return 1;
    }
     
    for(int i = 0; i < rows; i++) {
        for(int j = 0; j < cols; j++) {
            actual[i][j] = T0;
            
            if(i == sourceRow && j == sourceCol) {
                actual[i][j] = Th;
            }
        }
    }

    // Hasta aquí tenemos la matriz de temperaturas con la fuente de calor inicializadas
    for(int i = 0; i < 5; i++) {
        thermalChange(actual, next, alpha, rows, cols);
        
        double **aux = actual;
        actual = next;
        next = aux;

        actual[sourceRow][sourceCol] = Th;
    }
 

    freeMatrix(actual, rows);
    freeMatrix(next, rows);

    return 0;
}