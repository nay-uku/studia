#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

#define STOP SIGINT
#define START SIGCONT
#define EXIT SIGTERM

int Pids[3];
int ParentPid;

void LoadPids()
{
    FILE *file = fopen("data","r");
    if(!file)
    {
        perror("data");
        exit(1);
    }
    fscanf(file,"PPID:%d PID1: %d PID2: %d PID3: %d\n", &ParentPid,&Pids[0],&Pids[1],&Pids[2]);
    fclose(file);

}
int main()
{
    LoadPids();
    int nr=1;
    int syg;
    while(1)
    {
        printf("Proces macierzysty: %d . Wybierz proces do wyslania sygnalu: \n",ParentPid);
        printf("1.Proces 1 %d\n", Pids[0]);
        printf("2.Proces 2 %d\n", Pids[1]);
        printf("3.Proces 3 %d\n", Pids[2]);
        printf("4.Wyjdz z programu\n\n");
        scanf("%d",&nr);
        if(nr==4)
            exit(0);
        else if(nr!=1&&nr!=2&&nr!=3)
        {
            printf("Niepoprawny wybor numeru procesu. Sprobuj ponownie");
            continue;
        }
        nr--;
        printf("Lista sygnalow:.\n1. Wstrzymaj dzialanie;\n2. Wznow dzialanie;\n3. Zakoncz dzialanie.\n\n");
        printf("Wybierz sygnal: 1 - 3 \n");

       scanf("%d",&syg);


        switch(syg){
            case 1:
                kill(Pids[nr],STOP);
                break;
            case 2:
                kill(Pids[nr],START);
                break;
            case 3:
                kill(Pids[nr],EXIT);
                break;
            default:
                printf("Niepoprawny wybor sygnalu.Sprobuj ponownie\n");
                break;
        }

    }

    return 0;
}
