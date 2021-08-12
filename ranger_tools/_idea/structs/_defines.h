#define __int8 char
#define __int16 short
#define __int32 int
#define __int64 long long

#define byte unsigned __int8
#define word unsigned __int16
#define dword unsigned __int32

#define PTR void*
#define UNK dword
#define STR byte*
#define WSTR byte*

#define _gap_8 byte
#define _gap_16 word
#define _gap_32 dword
#define _gap _gap_8
#define GAP(name, n) _gap name[n]

#define FUNC void*
