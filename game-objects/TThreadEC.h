/** @file */
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
    VMT cls;

    int (__fastcall *** _04)(dword);
    HANDLE_ thread;
    _gap_32 _0C;
    byte priority;
    bool terminated;
    _gap _12;
    _gap _13;
    HANDLE_ _14;
    byte _18;
    _gap _19;
    _gap _1A;
    _gap _1B;
    HANDLE_ _1C;
    HANDLE_ _20;
    HANDLE_ _24;
    PTR _28;
};


struct TSaver: public TThreadEC {
    _gap_32 _2C;
    TBufEC* _30;
    TBufEC* _34;
    TBufEC* _38;
    TBufEC* _3C;
    TBufEC* _40;
};

