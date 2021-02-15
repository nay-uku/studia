#include <stdio.h>
#include <unistd.h>
#include <assert.h>
#include <string.h>
#include <sys/prctl.h>
#include <dirent.h>
#include <ctype.h>
#include <stdlib.h>
#include <time.h>
#include <errno.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <syslog.h>

void set_new_process_name(char *argv[],size_t space);
void set_last_char_to_null_term(char *name);
int is_numeric (const char * s);
int get_rand_num(int down_limit, int up_limit);
char *get_rand_process_name();
static void daemonize();
	
int main(int argc, char *argv[]) 
{
	if(strlen(argv[0])<200){
		char new_name[] = ".                                                                                                                                                                                                       ";
		execl(argv[0], new_name, (char *)NULL);
	}
	//DEBUG:
	//  printf("pid: %d\n", getpid());
	//  printf("nazwa: %s\n", argv[0]);
	//  printf("dlugosc: %d\n", strlen(argv[0]));

	// Liczenie długości na nową nazwę. Nie może być dłuższa od nazwy początkowej 
	size_t space = strlen(argv[0]); // długość nazwy
	int r = get_rand_num(120, 240);//Zakres czasu do losowania w sekundach

	
	//sleep(30);// Tylko po to by na filmiku na początku był bez zmiany nazwy
	while(1){
		// Zmiana nazwy
		set_new_process_name(argv, space);
		// Demonizacja - zmiana sesji i pidu
		daemonize();
		//Tutaj dowolne działanie programu
		
		//
		
		syslog (LOG_NOTICE, argv[0]);
		sleep(r);
		closelog();
	}

return 0;		
}

/*
 * Ustawia nową nazwę procesu, nie dłuższą od długości
 * pierwszej nazwy argv[0].
 * Jeżeli nie byłoby odpowiedniej ilości miejsca,
 * przycina nazwę,
 * tym samym unikając korupcji pamięci.        
 */
void set_new_process_name(char *argv[], size_t space) 
{
	char *new_process_name = get_rand_process_name();
	// Losuj dopóki długość nie będzie mniejsza/równa od przydzielonego
	// miejsca na nową nazwę.
	//printf("Dlugosc nowo wylosowanej nazwy: %ld\n", strlen(new_process_name)-1);
	//if(strlen(new_process_name)>space-1)
		//printf("Nazwa za dluga. Losuje ponownie\n");
	while(strlen(new_process_name)>space - 1)
	{
		new_process_name = get_rand_process_name();
		//printf("Dlugosc nowo wylosowanej nazwy: %ld\n", strlen(new_process_name)-1);
		if(strlen(new_process_name)>space-1){
			//printf("Nazwa za dluga. Losuje ponownie\n");
			sleep(1); // Bez czekania parę razy przydzieli tę samą nazwę 
		}
	}
	//printf("Nazwa zaakceptowana\n");
	// Zamiana \012 (newline) na \0.
	set_last_char_to_null_term(new_process_name);
	// Wyczyszczenie obecnej nazwy.
	memset(argv[0], '\0', space); 
	// Modyfikacja nazwy w /proc/$pid/cmdline.
    strncpy(argv[0], new_process_name, space - 1); // -1: Zostawienie null termination, jeżeli nowa nazwa byłaby dłuższa od space.
	// Modyfikacja nazwy w /proc/$pid/status.
	prctl(PR_SET_NAME, new_process_name);
} 
/**
 * Zwróć losowo wybraną nazwę procesu.
 */
char *get_rand_process_name()
{
	char *path = "/proc";
    struct dirent *dp;
    DIR *dir = opendir(path);
	int ran, pid_int, proc_amount = 0;
	int incr = 0;
	static char name[256];
	char command[30];
    // Nie można otworzyć folderu
    if (!dir){
        perror("Error ");
      	exit(EXIT_FAILURE);
	}
	// Czytanie katalogow 
    while ((dp = readdir(dir)) != NULL)
    {
		// Liczenie ilości procesów. Szukaj tylko folderów nazwanych od pidów procesów.
		if(is_numeric(dp->d_name)!=0){
			proc_amount += 1;
        	//printf("%ld\n", sizeof(dp->d_name)); //-256
		}
    }
	//printf("Ilosc procesow: %d\n", proc_amount);
	// Ustawienie wskaźnika folderu na początek.
	closedir(dir);
	dir = opendir(path);
	// Losowanie pidu do skopiowania jego nazwy
	// Losowanie w sposób - 1. policz ilość pidów 2. Wylosuj pozycje
	ran = get_rand_num(1, proc_amount);
	while ((dp = readdir(dir)) != NULL)
    {
		if(is_numeric(dp->d_name)!=0){
			incr += 1;
			memset(name, '\0', sizeof(name));
			strncpy(name, dp->d_name, sizeof(name)); //Przepisanie do zmiennej char* d_name (pid) 
			if(incr==ran)
				break;
		}
    }
	closedir(dir);
	// Konwersja pida w stringu na int.
	pid_int = atoi(name);// Po konwersji z char z wagi 256 schodzi na 4 jako int
	// Nazwa procesu z jego pidu:
	sprintf(command, "ps -p %d -o comm=", pid_int);
	FILE * ps = popen(command, "r"); // Ew. TODO znależć alternatywę w c zamiast popen
	memset(name, '\0', strlen(name));
	// Przepisanie wyniku komendy, która zwróci nazwę procesu, do zmiennej name.
	while (fgets(name, sizeof(name), ps) != 0) {/*...*/}	
	pclose(ps);
	//printf("Process name: %s", name);
	return name;
}
/**
 * Ustaw ostatni znak napisu na \0.
 */
void set_last_char_to_null_term(char *name)
{
	int len = strlen(name);
	char *pos = name + len -1;
	*pos = '\0';
}
/**
 * Sprawdź czy napis jest liczbą.
 */
int is_numeric (const char * s)
{
    if (s == NULL || *s == '\0' || isspace(*s))
      return 0;
    char * p;
    strtod (s, &p);
    return *p == '\0';
}
/**
 * Losuj liczbę od 1 do limitu.
 */
int get_rand_num(int down_limit, int up_limit)
{
	srand(time(NULL));
	int r_num = rand() % (up_limit + 1 - down_limit) + down_limit;
	return r_num;
}
/**
 * Demonizacja procesu
 */
static void daemonize()
{
    pid_t pid;
	struct sigaction act;
    act.sa_handler = SIG_IGN;

    /* Fork od procesu rodzica */
    pid = fork();

    /* Obsłużenie błędu */
    if (pid < 0)
        exit(EXIT_FAILURE);

    /* Terminowanie rodzica */
    if (pid > 0)
        exit(EXIT_SUCCESS);

    /* Proces dziecko zostaje liderem sesji */
    if (setsid() < 0){
		sleep(1);
		if (setsid() < 0)
        	exit(EXIT_FAILURE);
		}

    /*Ignorowanie wszystkich możliwych sygnałów */
    for(int i = 1 ; i < 65 ; i++) {
        // 9 i 19 nie mogą być obsłużone, blokowane ani zignorowane                    
        // 32 i 33 nie istnieją                                                        
        if((i != SIGKILL) && (i != SIGSTOP) && (i != 32) && (i != 33)) {
            assert(sigaction(i, &act, NULL) == 0);
        }
    }

    /* Drugi fork */
    pid = fork();

    /* Obsługa błędu */
    if (pid < 0)
        exit(EXIT_FAILURE);

    /* Terminowanie rodzica */
    if (pid > 0)
        exit(EXIT_SUCCESS);

    /* Ustawienie nowych praw pliku */
    umask(0);

    /* Zmiana katalogu roboczego na root */
    chdir("/");

    /* Zamknięcie wszystkich otwartych deskryptorów pliku */
    int x;
    for (x = sysconf(_SC_OPEN_MAX); x>=0; x--)
    {
        close (x);
    }
	//printf("pid: %d\n", getpid());

    /* Otworzenie logu - w celach testowych */
    openlog ("log_ukryty_proces", LOG_PID, LOG_DAEMON);
	
}