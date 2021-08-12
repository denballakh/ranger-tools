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

struct TBlockParEC {
    __cls* cls;

    TBlockParElEC* first;
    TBlockParElEC* last;
    int cnt;
    int cnt_par;
    int cnt_block;
    bool sort;
    _gap _1D;
    _gap _1E;
    _gap _1F;
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


struct TDataElEC {
    __cls* cls;

    _gap_32 _04;
    _gap_32 _08;
    _gap_32 _0C;
    _gap_32 _10;
    _gap_32 _14;
    _gap_32 _18;
    _gap_32 _1C;
    _gap_32 _20;
};


struct TDataEC {
    __cls* cls;

    _gap_32 _04;
    _gap_32 _08;
    _gap_32 _0C;
    _gap_32 _10;
    _gap_32 _14;
    _gap_32 _18;
    _gap_32 _1C;
    _gap_32 _20;
    _gap_32 _24;
    _gap_32 _28;
};

struct TPackFileEC {
    __cls* cls;

    //...
};//210

struct TPackCollectionEC {
    __cls* cls;

    TPackCollectionEC* field_4;
    TPackCollectionEC* field_8;
    THashEC* field_C;
    int field_10;
    int field_14;
    int field_18;
    int field_1C;
};//214

// struct TThreadEC {
//     __cls* cls;
//     UNK handle;
//     int thread_id;
//     int priority;
//     bool terminate;
//     bool end_destroy;
// };


struct TBlockMemUnitEC {
    __cls* cls;

    TBlockMemUnitEC* prev;
    TBlockMemUnitEC* next;
    TBufEC* buf;
    int maxsize;
    int size;
};

struct TBlockMemEC {
    __cls* cls;

    TBlockMemUnitEC* first;
    TBlockMemUnitEC* last;
    int block_size_default;
    bool alloc_clear;
    byte __gap[3];
};


struct TStringsElEC {
    __cls* cls;

    TStringsElEC* prev;
    TStringsElEC* next;
    WSTR str;
};

struct TStringsEC {
    __cls* cls;

    TStringsElEC* first;
    TStringsElEC* last;
    TStringsElEC* ptr;
};


enum TVarEC_type {
    TVarEC_type_unknown     = 0x0,
    TVarEC_type_int         = 0x1,
    TVarEC_type_dword       = 0x2,
    TVarEC_type_float       = 0x3,
    TVarEC_type_str         = 0x4,
    TVarEC_type_externfun   = 0x5,
    TVarEC_type_libraryfun  = 0x6,
    TVarEC_type_fun         = 0x7,
    TVarEC_type_class       = 0x8,
    TVarEC_type_array       = 0x9,
    TVarEC_type_ref         = 0xA,
};

struct TVarEC {
    __cls*          cls;

    byte*           name;
    TVarEC_type     type;
    int             val_int;
    unsigned int    val_dword;
    double          val_float;
    byte*           val_str;
    void*           val_externfun;
    DWORD*          val_libraryfun;
    TCodeEC*        val_fun;
    TCodeEC*        val_class;
    TVarArrayEC*    val_array;
    TVarEC*         val_ref;
};

struct TVarArrayEC {
    __cls* cls;

    int count;
    TVarEC* item;
    void* index;
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

struct TCodeAnalyzerEC {
    __cls* cls;

    TCodeAnalyzerUnitEC* first_free;
    TCodeAnalyzerUnitEC* last_free;
    TCodeAnalyzerUnitEC* first;
    TCodeAnalyzerUnitEC* last;
};


struct TExpressionEC {
    __cls* cls;

    int var_count;
    PTR var;
    int instr_count;
    PTR instr;
    bool instr_extern;
    byte __gap[3];
    int ret;
};

struct TExpressionInstrEC {
    __cls* cls;

    int type;
    int count;
    int* index;
};

struct TExpressionVarEC {
    __cls* cls;

    int type;
    byte* str;
    byte** path;
    TVarEC* var;
};




// struct THashEC {
//     __cls* cls;
// }; // d01c
