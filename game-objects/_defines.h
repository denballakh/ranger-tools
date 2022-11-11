/** @file */
#define byte     uint8_t
#define word     uint16_t
#define dword    uint32_t

#define PTR      void*
#define UNK      dword
// #define STR      char*
#define STR      wchar_t*
#define WSTR     wchar_t*

#define _gap_8   byte
#define _gap_16  word
#define _gap_32  dword
#define _gap     _gap_8

#define FUNC     void*

#ifndef NOT_IDA
    #define HANDLE_ HANDLE
#else
    #define HANDLE_ dword
#endif

