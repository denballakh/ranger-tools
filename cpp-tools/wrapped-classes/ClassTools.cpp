
int vmtSelfPtr           = -76;
int vmtIntfTable         = -72;
int vmtAutoTable         = -68;
int vmtInitTable         = -64;
int vmtTypeInfo          = -60;
int vmtFieldTable        = -56;
int vmtMethodTable       = -52;
int vmtDynamicTable      = -48;
int vmtClassName         = -44;
int vmtInstanceSize      = -40;
int vmtParent            = -36;
int vmtSafeCallException = -32;
int vmtAfterConstruction = -28;
int vmtBeforeDestruction = -24;
int vmtDispatch          = -20;
int vmtDefaultHandler    = -16;
int vmtNewInstance       = -12;
int vmtFreeInstance      = -8;
int vmtDestroy           = -4;

void* SelfPtr            (VMT vmt) { return *(void**)((uint8_t*)vmt + vmtSelfPtr); }
void* IntfTable          (VMT vmt) { return *(void**)((uint8_t*)vmt + vmtIntfTable); }
void* AutoTable          (VMT vmt) { return *(void**)((uint8_t*)vmt + vmtAutoTable); }
void* InitTable          (VMT vmt) { return *(void**)((uint8_t*)vmt + vmtInitTable); }
void* TypeInfo           (VMT vmt) { return *(void**)((uint8_t*)vmt + vmtTypeInfo); }
void* FieldTable         (VMT vmt) { return *(void**)((uint8_t*)vmt + vmtFieldTable); }
void* MethodTable        (VMT vmt) { return *(void**)((uint8_t*)vmt + vmtMethodTable); }
void* DynamicTable       (VMT vmt) { return *(void**)((uint8_t*)vmt + vmtDynamicTable); }
char* ClassName          (VMT vmt) {
    int len = *(uint8_t*)((uint8_t*)vmt + vmtClassName);
    char* src_str = (char*)(*(uint8_t**)((uint8_t*)vmt + vmtClassName) + 1);
    char* copy_str = new char[len + 1];
    for (int i = 0; i < len; i++)
        copy_str[i] = src_str[i];
    copy_str[len] = 0;
    return copy_str;
}
uint32_t InstanceSize (VMT vmt) { return *(uint32_t*)((uint8_t*)vmt + vmtInstanceSize); }
VMT   Parent             (VMT vmt) { return *(VMT  *)((uint8_t*)vmt + vmtParent); }
void* SafeCallException  (VMT vmt) { return *(void**)((uint8_t*)vmt + vmtSafeCallException); }
void* AfterConstruction  (VMT vmt) { return *(void**)((uint8_t*)vmt + vmtAfterConstruction); }
void* BeforeDestruction  (VMT vmt) { return *(void**)((uint8_t*)vmt + vmtBeforeDestruction); }
void* Dispatch           (VMT vmt) { return *(void**)((uint8_t*)vmt + vmtDispatch); }
void* DefaultHandler     (VMT vmt) { return *(void**)((uint8_t*)vmt + vmtDefaultHandler); }
void* NewInstance        (VMT vmt) { return *(void**)((uint8_t*)vmt + vmtNewInstance); }
void* FreeInstance       (VMT vmt) { return *(void**)((uint8_t*)vmt + vmtFreeInstance); }
void* Destroy            (VMT vmt) { return *(void**)((uint8_t*)vmt + vmtDestroy); }
void* Method  (VMT vmt, int index) { return *(void**)((uint8_t*)vmt + 4 * index); }

