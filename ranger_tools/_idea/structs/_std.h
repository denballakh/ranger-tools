struct TList {
  __cls* cls;
  int* data_p;      // указатель на массив
  int count;        // количество элементов
  int capacity;     // размер выделенной памяти (в элементах)
};

struct TStack {
  __cls* cls;
  TList* list;
};

struct TObjectList {};


