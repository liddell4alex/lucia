#ifndef LUCIA_H
#define LUCIA_H

double **makeMatrix(int rows, int cols);

void freeMatrix(double **matrix, int rows);

void thermalChange(double **actual, double **next, int rows, int cols, double alpha, double dt, double dx, double dy);

#endif /* LUCIA_H */