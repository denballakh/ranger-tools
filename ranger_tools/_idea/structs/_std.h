struct __cls {
  PTR   _00;
  int   _04;
  int   _08;
  int   _0C;
  int   _10;
  int   _14;
  int   _18;
  int   _1C;
  STR   type_name;
  int   type_size;
  void* parent_class;
  void* safe_call_exception;
  void* after_construction;
  void* before_destruction;
  void* dispatch;
  void* default_handler;
  void* new_instance;
  void* free_instance;
  void* destroy;
  void* methods[100];
};


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
    PTR* items;      // указатель на массив
    int count;        // количество элементов
    int capacity;     // размер выделенной памяти (в элементах)
};




// используется лишь в паре мест:

// struct TObjectList {
//     TList _;
//     UNK _10; // указатель на VMT класса итемов?
// };

// struct TOrderedList {
//     __cls* cls;
//     TList* list;
// };

// struct TStack {
//     TOrderedList _;
// };

// struct TMenuItemStack {
//     TStack _;
// };

