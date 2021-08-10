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


struct VMT_TEquipmentWithActCode {

};

struct VMT_TArtefact {
    PTR   _00;
    int   zeros[7];
    STR   type_name; // "TArtefact"
    int   type_size; // = 0x78
    VMT_TEquipmentWithActCode* parent_class;
    void* safe_call_exception;
    void* after_construction;
    void* before_destruction;
    void* dispatch;
    void* default_handler;
    void* new_instance;
    void* free_instance;
    void* destroy;
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