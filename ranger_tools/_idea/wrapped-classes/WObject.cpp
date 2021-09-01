class WObject {
 public:
    TObject* obj;

    static bool vmt_initialized;
    static __cls* vmt;

    WObject(TObject* obj): obj(obj) { this->init_vmt(); }
    WObject(WObject& other): obj(other.obj) {}
    WObject(): obj(nullptr) {}

    WObject& operator=(WObject& other) { this->obj = other.obj; return *this; }
    WObject& operator=(TObject* other) { this->obj = other; return *this; }


    static TObject* (__fastcall *Create)(__cls* cls, int8_t flag);
    static void     (__fastcall *Destroy)(TObject* obj, int8_t flag);

    static void init_vmt(__cls* vmt) {
        WObject::vmt_initialized = true;
        WObject::vmt = vmt;
        SET_VAR            (WObject::Destroy, vmt->destroy);
        SET_VAR_WITH_OFFSET(WObject::Create,  WObject::Destroy, 0xFA8 - 0xFC8);
    }
    void init_vmt() { if (this->obj != nullptr) WObject::init_vmt(this->obj->cls); }

};

bool WObject::vmt_initialized = false;
