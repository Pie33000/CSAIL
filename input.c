struct Client{
    int z;
    int h;
};
void test1(int z){
    int x = 5;
    int y = 4;
    x = y+5;
}

void test2(){
    int x;
    int y = 0;
    float z = -2;
    double h = -5;

    h = z - x;
}

void test3(){
    int *p;
    int x = 2;
    p = &x;
}

int test4(float z){
    float x = 2;
    int h = 2;
    x = 2 + z;
    return h;

}

void test5(){
    double tab[10];
    tab[0] = 1;
}

void test6(){
    int x = 0;
}

int main(){
    return 0;
}
