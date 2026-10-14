# Prepared only. Reuse the exact attempt03 whole-library/include contract.
cmake_minimum_required(VERSION 3.13)
project(pix574_md5_target C CXX)
set(PIX574_SANITIZE ON CACHE BOOL "Required whole-library instrumentation" FORCE)
set(PIX574_READER_PROBE OFF CACHE BOOL "Already accepted reader suite is separate" FORCE)
if(NOT IS_DIRECTORY "${SEALED_PACKET}/cmake-all-direct-contracts")
  message(FATAL_ERROR "Exact sealed7180 packet is required")
endif()
add_subdirectory("${SEALED_PACKET}/cmake-all-direct-contracts" controls)
add_executable(pix574-md5-alignment "${MD5_CONTROL_SOURCE}")
target_include_directories(pix574-md5-alignment PRIVATE
  "$<TARGET_PROPERTY:libcheevos,INCLUDE_DIRECTORIES>")
target_compile_definitions(pix574-md5-alignment PRIVATE
  "$<TARGET_PROPERTY:libcheevos,COMPILE_DEFINITIONS>")
# Reuse the sealed direct consumer's inherited sanitizer flags and explicit
# legacy feature options. Never link another MD5 implementation or whole-archive.
get_target_property(pix574_direct_options pix574-wii-partition-probe COMPILE_OPTIONS)
if(NOT pix574_direct_options)
  message(FATAL_ERROR "Missing sealed direct-source feature/sanitizer contract")
endif()
target_compile_options(pix574-md5-alignment PRIVATE ${pix574_direct_options})
target_link_options(pix574-md5-alignment PRIVATE -fsanitize=address,undefined)
target_link_libraries(pix574-md5-alignment PRIVATE libcheevos m)
