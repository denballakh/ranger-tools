/** @file */

#pragma once
#include "../structs/include.h"

#define SET_VAR(lhs, rhs)                     *(int8_t**)&lhs = (int8_t*)rhs;
#define SET_VAR_WITH_OFFSET(lhs, rhs, offset) *(int8_t**)&lhs = (int8_t*)rhs + (offset);

#define DelphiFunction(ret_type, func_name, ...) \
    __attribute__((regparm(3))) \
    ret_type (__stdcall *func_name)(__VA_ARGS__)


#include "ClassTools.cpp"
#include "WBaseClass.cpp"
#include "WObject.cpp"
#include "WList.cpp"

