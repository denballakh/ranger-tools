struct __cls {
    FUNC*     methods_p;              // указатель на указатель на первый метод в списке методов ( == &methods)
    uint32_t  _04;                    // служебные числа, обычно равны нулю, не знаю за что отвечают
    uint32_t  _08;
    uint32_t  _0C;
    uint32_t  _10;
    uint32_t  _14;
    uint32_t  _18;
    uint32_t  _1C;
    STR       type_name;              // имя класса
    uint32_t  type_size;              // размер экземпляра класса
    __cls*    parent_class;           // указатель на родительский класс ( == 0, если класс примитивный, обычно == VMT_TObject)
    FUNC      safe_call_exception;
    FUNC      after_construction;     // исполняется после конструктора
    FUNC      before_destruction;     // исполняется перед деструктором
    FUNC      dispatch;               // ?
    FUNC      default_handler;        // ?
    FUNC      new_instance;           // ?
    FUNC      free_instance;          // ?
    FUNC      destroy;                // деструктор
    FUNC      methods[100];           // список методов, у разных классов разное количество методов
};

struct VMT_TList {
    FUNC*     methods;
    uint32_t  _04[7];
    STR       type_name;
    uint32_t  type_size;
    __cls*    parent_class;
    FUNC      safe_call_exception;
    FUNC      after_construction;
    FUNC      before_destruction;
    FUNC      dispatch;
    FUNC      default_handler;
    FUNC      new_instance;
    FUNC      free_instance;
    FUNC      destroy;
    void      (__fastcall *grow)(TList*);
    void      (__fastcall *notify)();
    void      (__fastcall *clear)(TList*);
    void      (__fastcall *error)(TList*, int, int);
};


struct VMT_TEquipmentWithActCode {};


struct VMT_TArtefact {
    FUNC*     methods;
    uint32_t  _04[7];
    STR   type_name;  // "TArtefact"
    int   type_size;  // = 0x78
    VMT_TEquipmentWithActCode* parent_class;
    FUNC safe_call_exception;
    FUNC after_construction;
    FUNC before_destruction;
    FUNC dispatch;
    FUNC default_handler;
    FUNC new_instance;
    FUNC free_instance;
    FUNC destroy;
    void (__fastcall *sub_7D1E38)(TArtefact *, int, int);
    void (__fastcall *sub_7EA15C)(TArtefact *, int, int);
    void (__fastcall *sub_7D0A28)(TArtefact *, int, int);
    void (__fastcall *sub_7D0A38)(TArtefact *, int, int);
    void (__fastcall *sub_7D262C)(TArtefact *, int, int);
    void (__fastcall *sub_7D2B24)(TArtefact *, int, int);
    void (__fastcall *sub_7EACC8)(TArtefact *, int, int);
    void (__fastcall *sub_7D4634)(TArtefact *, int, int);
    void (__fastcall *sub_7EAD88)(TArtefact *, int, int);
    void (__fastcall *sub_7EAF40)(TArtefact *, int, int);
    void (__fastcall *sub_7EABC0)(TArtefact *, int, int);
    void (__fastcall *sub_7D2E20)(TArtefact *, int, int);
    void (__fastcall *sub_7D2E98)(TArtefact *, int, int);
    void (__fastcall *sub_7D48C0)(TArtefact *, int, int);
    void (__fastcall *sub_7D48D0)(TArtefact *, int, int);
    void (__fastcall *sub_7D49AC)(TArtefact *, int, int);
    void (__fastcall *sub_7D4C54)(TArtefact *, int, int);
    void (__fastcall *sub_7D4D88)(TArtefact *, int, int);
    void (__fastcall *sub_7D2588)(TArtefact *, int, int);
    void (__fastcall *sub_7EA1A4)(TArtefact *, int, int);
};


struct VMT_TThreadEC {
    void (__fastcall * methods)(TThreadEC *); // метод TThreadEC.Process()
    int   _04;
    int zeros[7];
    STR   type_name;
    unsigned int   type_size;
    FUNC  parent_class;
    FUNC  safe_call_exception;
    FUNC  after_construction;
    FUNC  before_destruction;
    FUNC  dispatch;
    FUNC  default_handler;
    FUNC  new_instance;
    FUNC  free_instance;
    FUNC  destroy;
    FUNC  process;
};
