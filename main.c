#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "lucia.h"

int main(int argn, char* args[]) {

    if(strcmp(args[1], "help") == 0) {
        fprintf(stdout, "Uso: lucia <metal> <alpha> <puntos x> <puntos y> <T0> <Th> <hx> <hy> <iter>\n\n");
        fprintf(stdout, "Donde:\n"
                        "   - <metal> ====> Nombre del metal con el que se va a trabajar (minusculas)"
                        "   - <alpha> ====> Difusividad térmica del material en m²/s.\n"
                        "   - <puntos x> => Cantidad de puntos en x de la placa.\n"
                        "   - <puntos y> => Cantidad de puntos en y de la placa.\n"
                        "   - <T0> =======> Temperatura inicial de la placa en °C.\n"
                        "   - <Th> =======> Temperatura de la fuente en °C.\n"
                        "   - <hx> =======> Punto de aplicación de la fuente en la placa en °C.\n"
                        "   - <hy> =======> Punto de aplicación de la fuente en la placa en °C.\n"
                        "   - <iter> =====> Número de iteraciones.\n\n"

                        "La cantidad de puntos en x y y también influye en las dimensiones de la placa,"
                        " la distancia entre cada punto vertical y horizontalmente es 0.01 metros. Si se"
                        " determina que en x hay 100 puntos la placa medirá 1.0 metros de ancho.\n\n"
                        
                        "Ejemplo: lucia silver 149e-6 5 5 25.0 200.0 0 3 200\n");
        return 0;

    } else if(argn != 10) {
        fprintf(stderr, "Error: Faltan argumentos\n");
        fprintf(stdout, "Ayuda: lucia help\n\n");

        fprintf(stdout, "Uso: lucia <metal> <alpha> <puntos x> <puntos y> <T0> <Th> <hx> <hy> <iter>\n"
                        "Ejemplo: lucia silver 149e-6 5 5 25.0 200.0 0 3 200\n");
        return 1;
    }

    // Nombre del metal
    char *metal = args[1];
    
    // Difusibidad termica (qué material es)
    double alpha = atof(args[2]);  // m²/s


    // Dimensiones
    int cols = atoi(args[3]), rows = atoi(args[4]);


    // Cambio
    double dx = 0.01;   // 1 cm
    double dy = 0.01;   // 1 cm
    double dt = 0.1;    // seg

    // Temperatura inicial de la placa
    double T0 = atof(args[5]);

    // Temperatura y posición de la fuente de calor
    double Th = atof(args[6]);
    int sourceCol = atoi(args[7]);
    int sourceRow = atoi(args[8]);

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

    // Comprobando si existe el directorio simulations
    FILE *test = fopen("simulations/test.tmp", "w");

    if(test == NULL) {
        fprintf(stderr, "Error: El directorio 'simulations' no existe o no tiene permisos de escritura\n"
                        "Es necesario crear el directorio 'simulations' con permisos de escritura.\n");

        freeMatrix(actual, rows);
        freeMatrix(next, rows);
        return 1; 
    }

    fclose(test);
    remove("simulations/test.tmp");


    // Creando el archivo con nombre <metal>.csv
    char filename[256];
    int length = snprintf(filename, sizeof(filename), "simulations/%s.csv", metal);

    if(length < 0 || length >= sizeof(filename)) {
        fprintf(stderr, "Error: Nombre del archivo demasiado largo\n");
        freeMatrix(actual, rows);
        freeMatrix(next, rows);
        return 1;
    }

    // Para almacenar el output en el archivo
    FILE *file = fopen(filename, "w");

    if(file == NULL) {
        perror("Error al crear el archivo CSV");
        freeMatrix(actual, rows);
        freeMatrix(next, rows);
        return 1;
    }

    // Escribiendo estructura del archivo, primero metadatos
    fprintf(file, "[METADATA]\n");
    fprintf(file, "rows,%d\n", rows);
    fprintf(file, "cols,%d\n", cols);
    fprintf(file, "alpha,%f\n", alpha);
    fprintf(file, "T0,%f\n", T0);
    fprintf(file, "Th,%f\n", Th);
    fprintf(file, "sourceRow,%d\n", sourceRow);
    fprintf(file, "sourceCol,%d\n", sourceCol);
    fprintf(file, "dx,%f\n", dx);
    fprintf(file, "dy,%f\n", dy);
    fprintf(file, "dt,%f\n", dt);
    fprintf(file, "iterations,%d\n", atoi(args[9]));

    fprintf(file, "[DATA]\n");

    // Hasta aquí tenemos la matriz de temperaturas con la fuente de calor inicializadas
    for(int i = 0; i < atoi(args[9]); i++) {
        thermalChange(actual, next, rows, cols, alpha, dt, dx, dy);
        
        double **aux = actual;
        actual = next;
        next = aux;

        actual[sourceRow][sourceCol] = Th;
    
        fprintf(stdout, "Iteración: %i\n", i);
        fprintf(file, "iteration,%i\n", i);
        for(int j = 0; j < rows; j++) {
            for(int k = 0; k < cols; k++) {
                fprintf(stdout, "%f ", actual[j][k]);
                fprintf(file, "%f", actual[j][k]);

                if(k < cols - 1) {
                    fprintf(file, ",");
                }

            }
            fprintf(stdout, "\n");
            fprintf(file, "\n");
        }
    }

    fclose(file);
    freeMatrix(actual, rows);
    freeMatrix(next, rows);

    return 0;
}
