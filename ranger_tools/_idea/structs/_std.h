/** @file */
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

// #ifdef NOT_IDA
// template <class T = uint32_t>
// struct TList<T> {
//     __cls* cls;

//     T* items;       // указатель на массив
//     int count;      // количество элементов
//     int capacity;   // размер выделенной памяти (в элементах)
// };

// template <class T = uint32_t>
// struct TObjectList<T>: public TList<T> {
//     PTR _10;  // указатель на VMT класса итемов?
// };

// #else

struct TObject {
    __cls* cls;
};

struct TList {
    __cls* cls;

    uint32_t* items;   ///< указатель на массив
    int count;         ///< количество элементов
    int capacity;      ///< размер выделенной памяти (в элементах)
};


struct TObjectList: public TList {
    PTR _10;           ///< указатель на VMT класса итемов?
};

// #endif
