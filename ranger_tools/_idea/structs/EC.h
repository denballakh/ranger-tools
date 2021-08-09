struct TBufEC {
    __cls* cls;
    int count;        // количество записанных байт
    int capacity;     // размер выделенной памяти
    int index;        // указатель доступа
    byte* data_p;     // указатель на данные
};

struct TFileEC {
    __cls* cls;
    int field_4;
    int is_opened;
    int filename;
};

struct THashEC {
    __cls* cls;
};

struct TBlockParEC {
    __cls* cls;

    int _field_04;
    int _field_08;
    int _field_0C;
    int _field_10;
    int _field_14;
    int _field_18;
    int _field_1C;
    int _field_20;
};

struct TBlockParElEC {
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


struct TDataEC {
    __cls* cls;
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
    void* name;
    TVarEC_type type;
    int val_int;
    unsigned int val_dword;
    byte gap14[4];
    double val_float;
    int val_str;
    void* val_externfun;
    byte gap28[4];
    void* val_fun;
    void* val_class;
    void* val_array;
    TVarEC* val_ref;
};

struct TVarArrayEC {
    __cls* cls;
    int field_4;
    int field_8;
    int field_C;
    int field_10;
    int field_14;
    int field_18;
    int field_1C;
    int field_20;
    int field_24;
    int field_28;
    int field_2C;
};

struct TCodeAnalyzerEC {
    __cls* cls;
    TCodeAnalyzerEC* field_4;
    TCodeAnalyzerEC* field_8;
    int field_C;
    int field_10;
    int field_14;
    int field_18;
    int field_1C;
    int field_20;
};

struct TExpressionEC {
    __cls* cls;
};

