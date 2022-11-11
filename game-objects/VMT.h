/** @file */

// typedef void* VMT;

struct VMT_helper {
    void* _;
    void* intf_table;
    void* auto_table;
    void* init_table;
    void* type_info;
    void* field_table;
    void* method_table;
    void* dynamic_table;
    uint8_t* class_name;
    uint32_t instance_size;
    VMT_helper* parent;
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


typedef VMT_helper* VMT;
