#include <stdlib.h>
#include <stdio.h>

void *simple_malloc(size_t size) ;


int main(void){
    int i;
    int x;
    int *addr, *tmp;

    /* intデータ４つ分のメモリを確保 */
    addr = (int*)simple_malloc(sizeof(int) * 4);
    printf("addr = %p\n", addr);
    if (addr == NULL) {
        printf("malloc error\n");
        return -1;
    }

    for (i = 0; i < 4; i++) {
        /* 添字演算子を用いたアクセス */
        addr[i] = i * 1024;
    }

    tmp = addr;
    for (i = 0; i < 4; i++) {
        /* 間接演算子を用いたアクセス */
        x = *addr;
        printf("%d : %d\n", i, x);

        /* アドレス値を加算 */
        addr++;
    }

    free(tmp);

    return 0;
}