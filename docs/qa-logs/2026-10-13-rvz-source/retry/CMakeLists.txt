# UNRUN. Configure/build only after coordinator allocates a compiler/sysroot.
cmake_minimum_required(VERSION 3.10)
project(pix574_retry_control CXX)
if(NOT EXISTS "${ES_SOURCE}/es-app/src/GameCubeRvzHashRetry.h")
    message(FATAL_ERROR "Set ES_SOURCE to the exact approved retry candidate")
endif()
add_executable(pix574-retry-control eligibility-control.cpp
    "${ES_SOURCE}/es-app/src/CheevosIndex.cpp"
    "${ES_SOURCE}/es-core/src/utils/StringUtil.cpp")
target_include_directories(pix574-retry-control PRIVATE
    "${ES_SOURCE}/es-app/src" "${ES_SOURCE}/es-core/src")
set_target_properties(pix574-retry-control PROPERTIES
    CXX_STANDARD 17 CXX_STANDARD_REQUIRED ON)
