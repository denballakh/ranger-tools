
struct _pair_byte {
    byte x;
    byte y;
};

struct _pair_int {
    int x;
    int y;
};

struct _pair_float {
    float x;
    float y;
};

struct _pair_double {
    double x;
    double y;
};

struct TList {
    __cls* cls;

    PTR* items;     // указатель на массив
    int count;      // количество элементов
    int capacity;   // размер выделенной памяти (в элементах)
};


struct TObjectList: public TList {
    PTR _10; // указатель на VMT класса итемов?
};

