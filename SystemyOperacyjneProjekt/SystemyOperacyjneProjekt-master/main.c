#define _GNU_SOURCE
#include <stdio.h>
#include <sys/shm.h>
#include <sys/sem.h>
#include <err.h>
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

#define rozmiar 500
#define PDES_READ 0
#define PDES_WRITE 1
#define STOP SIGINT
#define START SIGCONT
#define EXIT SIGTERM

bool Stop=false;
int Pids[3];
int ProcessID;

//SEMAFORY
union semun{
    int val;
    struct semid_ds *buf;
    unsigned short int *array;
    struct seminfo *__buf;
};
int SemLock(int semid){
    struct sembuf opr;
    opr.sem_num=0;
    opr.sem_op=-1;
    opr.sem_flg=0;
    if(semop(semid,&opr,1)==-1)
    {
        perror("Blad przy blokowaniu semafora.\n");
    }
    else
    {
        return 1;
    }
}
int SemUnlock(int semid){
    struct sembuf opr;
    opr.sem_num=0;
    opr.sem_op=1;
    opr.sem_flg=0;
    if(semop(semid,&opr,1)==-1)
    {
        perror("Blad przy odblokowaniu semafora.\n");
    }
    else
    {
        return 1;
    }
}
int CreateSemaphore(char letter){
    key_t key;
    int semid;
    union semun ctl;
    if ((key = ftok(".", letter)) == -1)
        perror("Blad przy tworzeniu klucza.\n");

    if ((semid = semget(key, 1, IPC_CREAT | 0600)) == -1)
        perror("Blad przy tworzeniu semafora.\n");

    ctl.val = 1;
    if (semctl(semid, 0, SETVAL, ctl) == -1)
        perror("Nie mozna ustawic semfora.\n");
    return semid;
}
//PAMIEC WSPOLDZIELONA
int CreateSharedMemory(size_t size)
{
    key_t key;//unikalny
    int shmid; //int na id do shared memory
    if((key=ftok(".",'Q'))==-1)
        perror("Blad utworzenia klucza.\n");
    if((shmid=shmget(key,size,IPC_CREAT|0666))<0)
        perror("Blad tworzenia segmentu.\n");
    return shmid;//id segmentu pamieci
}
//ODCZYT
FILE *ChooseInput()
{
    int wybor;
    printf("Witaj w procesie 1.\n");
    printf("Proces pobiera dane z tekstu wpisanego badz pliku.Wybierz:\n");
    printf("1 - aby pobrac z tekstu wpisanego\n");
    printf("2 - aby pobrac z pliku\n");
    wybor=getchar()-'0';
    if (wybor==1)
    {
        return stdin;
    }
    FILE *input;
    char name[150];
    printf("Nazwa pliku: ");
    fscanf(stdin,"%s",name);

    input=fopen(name,"r");

    if(input==NULL)
        perror("Nie ma pliku.\n");
    return input;
}
//SYGNALY
void SetHandler(sighandler_t handler)
{
    struct sigaction newAction;
    newAction.sa_handler=handler;
    sigaction(STOP,&newAction,NULL);
    sigaction(START,&newAction,NULL);
    sigaction(EXIT,&newAction,NULL);
}
void Handler(int sig)
{

    if(ProcessID==1) {
        if (sig == STOP)
            Stop = true;
        else if (sig == START)
            Stop = false;
        else if (sig == EXIT)
            exit(0);
    }
    else
        {
            kill(Pids[0],sig);
            if(sig==EXIT)
            {
                exit(0);
            }
        }
}
void p1(int pipes[])
{
    sleep(1);
    ProcessID=1;
    close(pipes[PDES_READ]);
    char data[rozmiar]={};
    FILE *input=ChooseInput();
    while(1)
    {
        if(Stop)
        {
            sleep(1);
            continue;
        }
    if(fgets(data,rozmiar,input)!=NULL)
        {
            sleep(1);
            write(pipes[PDES_WRITE],data,rozmiar);
        }
//    else
//        {
//            fclose(input);
//        }
    }
}
void p2(int pipes[],int semid1,int semid2,int shmid)
{
    ProcessID=2;
    close(pipes[PDES_WRITE]);
    char data[rozmiar];
    //char liczba[rozmiar];
    char *shm=shmat(shmid,NULL,0);//podlaczenie do shm
    while(1)
    {
        SemLock(semid1);
        memset(data, 0, rozmiar);
        read(pipes[PDES_READ],data,rozmiar);
        printf("%s\n",data);
        data[0]=(char)(strlen(data)-1);
        memcpy(shm, data, rozmiar);
        SemUnlock(semid2);
    }
}
void p3(int shmid,int semid1,int semid2)
{
    ProcessID=3;
    char *shm;
    char data[rozmiar];
    shm=shmat(shmid,NULL,0);
    while(1)
    {
        SemLock(semid2);
        memcpy(data, shm, rozmiar);
        fprintf(stderr,"%d",data[0]);
        putchar('\n');
        SemUnlock(semid1);
    }
}
void SavePids()
{
    FILE *file = fopen("data","w");
    if(!file)
    {
        perror("data");
        exit(1);
    }
    fprintf(file,"PPID:%d PID1: %d PID2: %d PID3: %d\n", getpid(),Pids[0],Pids[1],Pids[2]);
    fclose(file);
}
//****************************
//****************************
int main()
{
    int shmid=CreateSharedMemory(rozmiar);
    int semid1=CreateSemaphore('b');
    int semid2=CreateSemaphore('c');
    SemLock(semid2);
    //PIPES
    int pipeDes[2];
    pipe(pipeDes);
    if(pipe(pipeDes)==-1)
    {
        perror("Blad przy tworzeniu pipe.\n");
    }
    SetHandler(Handler);

    if ((Pids[0]=fork())==0)
    {
        printf("Proces konsumenta 1 PID:%d PPID: %d\n", getpid(), getppid());
        p1(pipeDes);
    }
    if ((Pids[1]=fork())==0)
    {
        printf("Proces konsumenta 2 PID:%d PPID: %d\n", getpid(), getppid());
        p2(pipeDes,semid1,semid2,shmid);
    }
    if ((Pids[2]=fork())==0)
    {
        printf("Proces konsumenta 3 PID:%d PPID: %d\n", getpid(), getppid());
        p3(shmid,semid1,semid2);
    }
    SavePids();
    wait(NULL);
    for(int i=0;i<3;i++)
    {
        kill(Pids[i],SIGKILL);
    }
    shmctl(shmid,IPC_RMID,NULL);
    semctl(semid1,0,IPC_RMID);
    semctl(semid2,0,IPC_RMID);
    return 0;
}

