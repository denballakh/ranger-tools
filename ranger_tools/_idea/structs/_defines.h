#define byte     uint8_t
#define word     uint16_t
#define dword    uint32_t

#define PTR      void*
#define UNK      dword
#define STR      byte*
#define WSTR     byte*

#define _gap_8   byte
#define _gap_16  word
#define _gap_32  dword
#define _gap     _gap_8

#define FUNC     void*

#ifndef HANDLE
    #define HANDLE dword
#endif
