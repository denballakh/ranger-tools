/** @file */

class WBaseClass {
 public:
    TObject* obj;

    static bool vmt_initialized;
    static VMT vmt;

    WBaseClass(TObject* obj): obj(obj) { this->init_vmt(); }
    WBaseClass(WBaseClass& other): obj(other.obj) {}
    WBaseClass(): obj(nullptr) {}

    WBaseClass& operator=(WBaseClass& other) { this->obj = other.obj; return *this; }
    WBaseClass& operator=(TObject* other) { this->obj = other; return *this; }


    static TObject* (__fastcall *Create)(VMT cls, int8_t flag);
    static void     (__fastcall *Destroy)(TObject* obj, int8_t flag);

    static void init_vmt(VMT vmt) {
        if (vmt == nullptr) return;
        if (WBaseClass::vmt_initialized) return;

        WBaseClass::vmt_initialized = true;
        WBaseClass::vmt = vmt;
        // SET_VAR            (WBaseClass::Destroy, vmt->destroy);
        SET_VAR_WITH_OFFSET(WBaseClass::Create,  WBaseClass::Destroy, 0xFA8 - 0xFC8);
    }
    void init_vmt() {
        if (this->obj == nullptr) return;
        WBaseClass::init_vmt(this->obj->cls);
    }

    static WBaseClass& create() { WBaseClass* x = new WBaseClass(WBaseClass::Create(WBaseClass::vmt, 1)); return *x; }
    void destroy() { WBaseClass::Destroy(this->obj, 1); this->obj = nullptr; }
};
