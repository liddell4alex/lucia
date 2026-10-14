#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define F 80
#define C 80

int distChevichev(int ox, int oy, int x, int y) {
    int dfil = abs(ox - x);
    int dcol = abs(oy - y);

    return ((dfil > dcol) ? dfil : dcol);
}

int main(int argc, char** argv)
{
    FILE *file = fopen("matriz.txt", "w");
    if(file == NULL) {
        printf("Error al crear archivo");
        return 1;
    }

    // Semilla de aleatoriedad
    srand(time(NULL));

    // Dirs       N, NE, E, SE, S, SO,  O,  NO  vecinos moore
    int dfil[] = { -1, -1, 0,  1, 1,  1,  0,  -1};
    int dcol[] = {  0,  1, 1,  1, 0, -1, -1,  -1};
    
    // Matriz micelio
    static int micelio[F][C] = {0};

    // Posición del hongo
    int h_fil = F/2;
    int h_col = C/2;
    micelio[h_fil][h_col] = 1;

    int n = 2;  // Movimientos de la hifa, el hongo es 1 entonces empieza desde 2
    int actfil = h_fil, actcol = h_col;     // Para saber la posicion actual de la hifa
    int dists[8] = {0};     // Lista de distancias entre el hongo y la pos. actual de la hifa
    int idist[8] = {0};     // Lista de indices de las distancias

    // Termina cuando se llega a un borde
    while(actfil-1 > 0 && actfil+1 < F && actcol-1 > 0 && actcol+1 < C) {
       
        // Agrego la distancia entre el hongo y la pos actual de la hifa
        for(int i = 0; i < 8; i++) {
            dists[i] = distChevichev(h_fil, h_col, actfil+dfil[i], actcol+dcol[i]);
            idist[i] = i;
        }

        // Ordeno la lista, son 8 entonces hago bubblesort
        int cnt = 1;
        while(cnt != 0) {
            cnt = 0;
            for(int i = 0; i < 8; i++) {
                if(dists[i] < dists[i+1]) {
                    // Reordeno en las distancias
                    int aux = dists[i];
                    dists[i] = dists[i+1];
                    dists[i+1] = aux;

                    // Reordeno en el indice de distancias
                    aux = idist[i];
                    idist[i] = idist[i+1];
                    idist[i+1] = aux;

                    cnt++;
                }
            }
        }

        //for(int i = 0; i < 8; i++) {
        //    printf("%d ", dists[i]);
        //}
        //printf("\n");
        //for(int i = 0; i < 8; i++) {
        //    printf("%d ", idist[i]);
        //}
        //printf("\n\n");
       
        // Una vez ordenadas las listas, entre las primeras 5 que son las distancias mas grandes tomo 1 aleatoriamente
        int dirf = rand() % 5;
        int afil = actfil + dfil[idist[dirf]];
        int acol = actcol + dcol[idist[dirf]];

        // Compruebo que la celda sea invadible
        if(micelio[afil][acol] == 0) {  
            actfil = afil;
            actcol = acol;

            micelio[actfil][actcol] = n; n++;
            //printf("%d\n", n);
        }

        //if(count < max) {
        //    count++;
        //} else {
        //    break;
        //}
    }
    
    //for(int i = 0; i < F; i++) {
    //    for(int j = 0; j < C; j++) {
    //        printf("%d ", micelio[i][j]);
    //    }
    //    printf("\n");
    //}
    
    for(int i = 0; i < F; i++) {
        for(int j = 0; j < C; j++) {
            fprintf(file, "%d ", micelio[i][j]);
        }
        fprintf(file, "\n");
    }

    fclose(file);

    return 0;
}