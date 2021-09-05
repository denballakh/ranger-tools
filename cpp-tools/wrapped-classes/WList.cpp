/** @file */
class WList {
 public:
    TList* obj;

    static bool vmt_initialized;
    static void* vmt;

    WList(TList* obj): obj(obj) { this->init_vmt(); }
    WList(WList& other): obj(other.obj) {}
    WList(): obj(nullptr) {}

    WList& operator=(WList& other) { this->obj = other.obj; return *this; }
    WList& operator=(TList* other) { this->obj = other; return *this; }


    static TList*    (__fastcall *Create)      (void* cls, int8_t flag);
    static void      (__fastcall *Destroy)     (TList* obj, int8_t flag);
    static void      (__fastcall *Add)         (TList* list, uint32_t value);
    static void      (__fastcall *Clear)       (TList* list);
    static void      (__fastcall *Delete)      (TList* list, int32_t index);
    // static void      (__fastcall *Error)       (TList* list, int32_t, int32_t);
    // static void      (__fastcall *Error_0)     (TList* list, int32_t, int32_t);
    static void      (__fastcall *Exchange)    (TList* list, int32_t index1, int32_t index2);
    static void      (__fastcall *Expand)      (TList* list);
    static uint32_t  (__fastcall *First)       (TList* list);
    static uint32_t  (__fastcall *Get)         (TList* list, int32_t index);
    static void      (__fastcall *Grow)        (TList* list);
    static int32_t   (__fastcall *IndexOf)     (TList* list, uint32_t value);
    static void      (__fastcall *Insert)      (TList* list, int32_t index, uint32_t value);
    static uint32_t  (__fastcall *Last)        (TList* list);
    static void      (__fastcall *Put)         (TList* list, int32_t index, uint32_t value);
    static void      (__fastcall *Remove)      (TList* list, uint32_t value);
    static void      (__fastcall *SetCapacity) (TList* list, int32_t new_capacity);
    static void      (__fastcall *SetCount)    (TList* list, int32_t new_count);
    // static void      (__fastcall *Notify)      (TList* list);

    static void init_vmt(void* vmt) {
        if (vmt == nullptr) return;
        if (WList::vmt_initialized) return;

        // WObject::init_vmt(vmt->parent_class); // ПЕРЕДЕЛАТЬ

        WList::vmt_initialized = true;
        WList::vmt = vmt;
        // SET_VAR            (WList::Destroy    , vmt->destroy); // ПЕРЕДЕЛАТЬ
        SET_VAR            (WList::Create     , WObject::Create);

        SET_VAR_WITH_OFFSET(WList::Add        , WList::Destroy, 0xA9C - 0xA7C);
        SET_VAR_WITH_OFFSET(WList::Clear      , WList::Destroy, 0xAD0 - 0xA7C);
        SET_VAR_WITH_OFFSET(WList::Delete     , WList::Destroy, 0xAE8 - 0xA7C);
        // SET_VAR_WITH_OFFSET(WList::Error      , WList::Destroy, 0xB4C - 0xA7C);
        // SET_VAR_WITH_OFFSET(WList::Error_0    , WList::Destroy, 0xB84 - 0xA7C);
        SET_VAR_WITH_OFFSET(WList::Exchange   , WList::Destroy, 0xBD8 - 0xA7C);
        SET_VAR_WITH_OFFSET(WList::Expand     , WList::Destroy, 0xC28 - 0xA7C);
        SET_VAR_WITH_OFFSET(WList::First      , WList::Destroy, 0xC40 - 0xA7C);
        SET_VAR_WITH_OFFSET(WList::Get        , WList::Destroy, 0xC48 - 0xA7C);
        SET_VAR_WITH_OFFSET(WList::Grow       , WList::Destroy, 0xC70 - 0xA7C);
        SET_VAR_WITH_OFFSET(WList::IndexOf    , WList::Destroy, 0xCA4 - 0xA7C);
        SET_VAR_WITH_OFFSET(WList::Insert     , WList::Destroy, 0xCC4 - 0xA7C);
        SET_VAR_WITH_OFFSET(WList::Last       , WList::Destroy, 0xD30 - 0xA7C);
        SET_VAR_WITH_OFFSET(WList::Put        , WList::Destroy, 0xD3C - 0xA7C);
        SET_VAR_WITH_OFFSET(WList::Remove     , WList::Destroy, 0xD8C - 0xA7C);
        SET_VAR_WITH_OFFSET(WList::SetCapacity, WList::Destroy, 0xDAC - 0xA7C);
        SET_VAR_WITH_OFFSET(WList::SetCount   , WList::Destroy, 0xDE8 - 0xA7C);
        // SET_VAR_WITH_OFFSET(WList::Notify     , WList::Destroy, 0xE58 - 0xA7C);
    }
    void init_vmt() {
        if (this->obj == nullptr) return;
        WList::init_vmt(this->obj->cls);
    }

    static WList& create() { WList* x = new WList(WList::Create(WList::vmt, 1)); return *x; }
    void destroy() { WList::Destroy(this->obj, 1); this->obj = nullptr; }

    void        add(uint32_t value)                 {        WList::Add         (this->obj, value); }
    void        clear()                             {        WList::Clear       (this->obj); }
    void        del(int32_t index)                  {        WList::Delete      (this->obj, index); }
    void        exchange(int32_t i1, int32_t i2)    {        WList::Exchange    (this->obj, i1, i2); }
    void        expand()                            {        WList::Expand      (this->obj); }
    uint32_t    first()                             { return WList::First       (this->obj); }
    uint32_t    get(int32_t index)                  { return WList::Get         (this->obj, index); }
    void        grow()                              {        WList::Grow        (this->obj); }
    int32_t     index_of(uint32_t value)            { return WList::IndexOf     (this->obj, value); }
    void        insert(int32_t i, uint32_t v)       {        WList::Insert      (this->obj, i, v); }
    uint32_t    last()                              { return WList::Last        (this->obj); }
    void        put(int32_t i, uint32_t v)          {        WList::Put         (this->obj, i, v); }
    void        remove(uint32_t value)              {        WList::Remove      (this->obj, value); }
    void        set_capacity(int32_t new_value)     {        WList::SetCapacity (this->obj, new_value); }
    void        set_count(int32_t new_value)        {        WList::SetCount    (this->obj, new_value); }


    uint32_t& operator[](int32_t index) {
        if (index >= 0)
            return this->obj->items[index];
        else
            return this->obj->items[this->obj->count + index];
    }
    int32_t count() { return this->obj->count; }
};

void(__fastcall *WList::Destroy)(TList*,int8_t) = nullptr;
