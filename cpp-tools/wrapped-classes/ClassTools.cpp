struct VMT_helper {
    void* self_ptr;
    void* intf_table;
    void* auto_table;
    void* init_table;
    void* type_info;
    void* field_table;
    void* method_table;
    void* dynamic_table;
    uint8_t* class_name;
    uint32_t instance_size;
    VMT parent;
    void* safe_call_exception;
    void* after_construction;
    void* before_destruction;
    void* dispatch;
    void* default_handler;
    void* new_instance;
    void* free_instance;
    void* destroy;
    void* methods[];
};

constexpr int vmt_base_offset = -offsetof(VMT_helper, methods); // == -76 == -sizeof(VMT_helper)

VMT_helper* vmt_struct(VMT vmt) { return (VMT_helper*)((uint8_t*)vmt + vmt_base_offset); }

void* SelfPtr            (VMT vmt) { return vmt_struct(vmt)->self_ptr; }
void* IntfTable          (VMT vmt) { return vmt_struct(vmt)->intf_table; }
void* AutoTable          (VMT vmt) { return vmt_struct(vmt)->auto_table; }
void* InitTable          (VMT vmt) { return vmt_struct(vmt)->init_table; }
void* TypeInfo           (VMT vmt) { return vmt_struct(vmt)->type_info; }
void* FieldTable         (VMT vmt) { return vmt_struct(vmt)->field_table; }
void* MethodTable        (VMT vmt) { return vmt_struct(vmt)->method_table; }
void* DynamicTable       (VMT vmt) { return vmt_struct(vmt)->dynamic_table; }
void* SafeCallException  (VMT vmt) { return vmt_struct(vmt)->safe_call_exception; }
void* AfterConstruction  (VMT vmt) { return vmt_struct(vmt)->after_construction; }
void* BeforeDestruction  (VMT vmt) { return vmt_struct(vmt)->before_destruction; }
void* Dispatch           (VMT vmt) { return vmt_struct(vmt)->dispatch; }
void* DefaultHandler     (VMT vmt) { return vmt_struct(vmt)->default_handler; }
void* NewInstance        (VMT vmt) { return vmt_struct(vmt)->new_instance; }
void* FreeInstance       (VMT vmt) { return vmt_struct(vmt)->free_instance; }
void* Destroy            (VMT vmt) { return vmt_struct(vmt)->destroy; }

uint32_t InstanceSize    (VMT vmt) { return vmt_struct(vmt)->instance_size; }
VMT   Parent             (VMT vmt) { return vmt_struct(vmt)->parent; }
void* Method  (VMT vmt, int index) { return vmt_struct(vmt)->methods[index]; }

std::string ClassName    (VMT vmt) {
    int len = *vmt_struct(vmt)->class_name;
    char* src_str = (char*)(vmt_struct(vmt)->class_name + 1);
    char* copy_str = new char[len + 1];
    for (int i = 0; i < len; i++)
        copy_str[i] = src_str[i];
    copy_str[len] = 0;
    return std::string(copy_str);
}



std::unordered_map<std::string, VMT> vmts;

void add_class(VMT vmt) {
    if (vmt == nullptr) return;
    vmts[ClassName(vmt)] = vmt;
    add_class(Parent(vmt));
}

