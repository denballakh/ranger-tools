#define __int8 char
#define __int16 short
#define __int32 int
#define __int64 long long

#define byte unsigned __int8
#define word unsigned __int16
#define dword unsigned __int32
#define PTR void*
#define UNK int

struct __cls {
  char* type_name_0;
  int   zeros[7];
  char* type_name;
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



struct _pair_int {
  int x;
  int y;
};

struct _pair_float {
  float x;
  float y;
};