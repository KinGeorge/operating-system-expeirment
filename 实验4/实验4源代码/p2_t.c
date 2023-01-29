#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

//因为pthread 库非Linux 默认库，
// 编译时使用 g++ *.c -l pthread
static int tickets = 10;
bool flag[2] = {false, false};

void * print1(void* args)
{
	while(flag[1]);
    flag[0]=true;
    while(tickets>0)
    {
        tickets--;
        printf("remain tickets: %d\n", tickets);
    }
    flag[0]=false;
}

void* print2(void * args)
{
    while(flag[0]);
    flag[1]=true;
    while(tickets>0)
   {
        sleep(1);
        tickets--;
        printf("remain tickets: %d\n", tickets);
    }
    flag[1]=false;
}


int main()
{
    pthread_t thread1, thread2;
    //创建线程
    pthread_create(&thread1, NULL, print1, NULL);
    pthread_create(&thread2, NULL, print2, NULL);
    //等待线程执行结束
    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    printf("The End...\n");
}