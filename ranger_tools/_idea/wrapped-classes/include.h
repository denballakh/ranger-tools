/** @file */
#ifndef RANGER_TOOLS_WRAPPED_CLASSES_INCLUDE_H_
#define RANGER_TOOLS_WRAPPED_CLASSES_INCLUDE_H_

#include "../structs/include.h"

#define SET_VAR(lhs, expr)                   *(uint32_t*)&lhs = (uint32_t)(expr);
#define SET_VAR_WITH_OFFSET(lhs, rhs, offset) *(int8_t**)&lhs = (int8_t*)&rhs + (offset);

#include "WObject.cpp"
#include "WList.cpp"

#endif  // RANGER_TOOLS_WRAPPED_CLASSES_INCLUDE_H_
