#ifndef LUCIA_H
#define LUCIA_H

double **makeMatrix(int rows, int cols);

void freeMatrix(double **matrix, int rows);

double **thermalChange(double **actual, double **next, double alpha, int rows, int cols);

#endif /* LUCIA_H */