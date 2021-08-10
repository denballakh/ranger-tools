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
}; // d01c

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

// struct TThreadEC {
//     __cls* cls;
//     UNK handle;
//     int thread_id;
//     int priority;
//     bool terminate;
//     bool end_destroy;
// };

/*
TThreadEC - 2c
    TFileStreamEC - 58
    TGAIFileThreadGI - 30
    TSaver - 44
    TScriptThread - 2c
    TThreadGameLoad - 30
    TCacheLoader - 38
    TfFilmLoader - 2c
    TThreadCalc - 30
    TThreadCreateNewGame - 4c
    TMusicUnit - 54
    TMusicControl - 44
    TSteamCallbacksThread - 2c
*/

struct TThreadEC {
    __cls* cls;
    _gap _004;
    _gap _005;
    _gap _006;
    _gap _007;
    _gap _008;
    _gap _009;
    _gap _00A;
    _gap _00B;
    _gap _00C;
    _gap _00D;
    _gap _00E;
    _gap _00F;
    _gap _010;
    _gap _011;
    _gap _012;
    _gap _013;
    _gap _014;
    _gap _015;
    _gap _016;
    _gap _017;
    _gap _018;
    _gap _019;
    _gap _01A;
    _gap _01B;
    _gap _01C;
    _gap _01D;
    _gap _01E;
    _gap _01F;
    _gap _020;
    _gap _021;
    _gap _022;
    _gap _023;
    _gap _024;
    _gap _025;
    _gap _026;
    _gap _027;
    _gap _028;
    _gap _029;
    _gap _02A;
    _gap _02B;
};


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

