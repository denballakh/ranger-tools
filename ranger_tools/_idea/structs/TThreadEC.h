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
    VMT_TThreadEC* cls;

    int (__fastcall *** _04)(_DWORD);
    HANDLE thread;
    _gap _0C;
    _gap _0D;
    _gap _0E;
    _gap _0F;
    byte priority;
    bool terminated;
    _gap _12;
    _gap _13;
    HANDLE _14;
    byte _18;
    _gap _19;
    _gap _1A;
    _gap _1B;
    HANDLE _1C;
    HANDLE _20;
    HANDLE _24;
    PTR _28;
};


struct TSaver {
    TThreadEC;
    _gap_32 _2C;
    TBufEC* _30;
    TBufEC* _34;
    TBufEC* _38;
    TBufEC* _3C;
    TBufEC* _40;
};

