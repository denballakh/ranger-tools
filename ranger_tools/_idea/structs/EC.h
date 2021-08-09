struct TBufEC {
    __cls* cls;
    int count;        // количество записанных байт
    int capacity;     // размер выделенной памяти
    int index;        // указатель доступа
    byte* data_p;     // указатель на данные
};

struct TFileEC {
    __cls* cls;
    int file_handler;
    int is_opened;
    int filename;
};

struct THashEC {
    __cls* cls;
};

struct TBlockParEC {
    __cls* cls;

    TBlockParElEC* first;
    TBlockParElEC* last;
    int cnt;
    int cnt_par;
    int cnt_block;
    bool sort;
    byte __gap_0;
    byte __gap_1;
    byte __gap_2;
    TBlockParElEC* array;
    int array_cnt;
};

struct TBlockParElEC {
    __cls* cls;

    TBlockParElEC* prev;
    TBlockParElEC* next;
    TBlockParElEC* parent;
    int tip;
    byte* name;
    byte* zn;
    byte* com;
    TBlockParEC* block;
    int fast_first;
    int fast_cnt;
};


struct TDataEC {
    __cls* cls;

    int _field_04;
    int _field_08;
    int _field_0C;
    int _field_10;
    int _field_14;
    int _field_18;
    int _field_1C;
    int _field_20;
    int _field_24;
    int _field_28;
};

struct TPackFileEC {
    __cls* cls;
};

struct TPackCollectionEC {
    __cls* cls;
    TPackCollectionEC* field_4;
    TPackCollectionEC* field_8;
    THashEC* field_C;
    int field_10;
    int field_14;
    int field_18;
    int field_1C;
};




enum TVarEC_type {
    TVarEC_type_unknown = 0x0,
    TVarEC_type_int = 0x1,
    TVarEC_type_dword = 0x2,
    TVarEC_type_float = 0x3,
    TVarEC_type_str = 0x4,
    TVarEC_type_externfun = 0x5,
    TVarEC_type_6 = 0x6,
    TVarEC_type_fun = 0x7,
    TVarEC_type_8 = 0x8,
    TVarEC_type_array = 0x9,
    TVarEC_type_ref = 0xA,
};

struct TVarEC {
    __cls* cls;
    byte* name;
    TVarEC_type type;
    int val_int;
    unsigned int val_dword;
    double val_float;
    byte* val_str;
    void* val_externfun;
    DWORD* val_libraryfun;
    TCodeEC* val_fun;
    TCodeEC* val_class;
    TVarArrayEC* val_array;
    TVarEC* val_ref;
};

struct TCodeEC {};

struct TVarArrayEC {
    __cls* cls;
    int count;
    void* item;
    void* index;
};

struct TCodeAnalyzerEC {
    __cls* cls;
    TCodeAnalyzerUnitEC* first_free;
    TCodeAnalyzerUnitEC* last_free;
    TCodeAnalyzerUnitEC* first;
    TCodeAnalyzerUnitEC* last;
};

struct TCodeAnalyzerUnitEC {
    __cls* cls;

    TCodeAnalyzerUnitEC* prev;
    TCodeAnalyzerUnitEC* next;

    int type;
    int sme;
    int len;
    byte* str;
};

struct TExpressionEC {
    __cls* cls;
};

