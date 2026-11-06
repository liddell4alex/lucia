#include "lucia.h"
#include <stdlib.h>

double **makeMatrix(int rows, int cols) {
    // Aparto la memoria para las filas
    double **matrix = malloc(rows * sizeof(double *));

    // Si fallo malloc retorno NULL
    if(matrix == NULL) {
        return NULL;
    }

    // Si no falló continúo con la alocación de memoria para las columnas
    for(int i = 0; i < rows; i++) {
        matrix[i] = malloc(cols * sizeof(double));

        if(matrix[i] == NULL) {
            for(int j = 0; j < i; j++) {
                free(matrix[j]);
            }
        
            // Fallo la alocación completa
            free(matrix);
            return NULL;
        }
    }

    return matrix;
}

void freeMatrix(double **matrix, int rows) {
    if(matrix == NULL) {
        return;
    }

    for(int i = 0; i < rows; i++) {
        free(matrix[i]);
    }

    free(matrix);
}