/** @file */

class WObject {
 public:
    TObject* obj;

    static bool vmt_initialized;
    static VMT vmt;

    WObject(TObject* obj): obj(obj) { this->init_vmt(); }
    WObject(WObject& other): obj(other.obj) {}
    WObject(): obj(nullptr) {}

    WObject& operator=(WObject& other) { this->obj = other.obj; return *this; }
    WObject& operator=(TObject* other) { this->obj = other; return *this; }


    static TObject* (__fastcall *Create)(VMT cls, int8_t flag);
    static void     (__fastcall *Destroy)(TObject* obj, int8_t flag);

    static void init_vmt(VMT vmt) {
        if (vmt == nullptr) return;
        if (WObject::vmt_initialized) return;

        WObject::vmt_initialized = true;
        WObject::vmt = vmt;
        // SET_VAR            (WObject::Destroy, vmt->destroy);
        SET_VAR_WITH_OFFSET(WObject::Create,  WObject::Destroy, 0xFA8 - 0xFC8);
    }
    void init_vmt() {
        if (this->obj == nullptr) return;
        WObject::init_vmt(this->obj->cls);
    }

    static WObject& create() { WObject* x = new WObject(WObject::Create(WObject::vmt, 1)); return *x; }
    void destroy() { WObject::Destroy(this->obj, 1); this->obj = nullptr; }
};
