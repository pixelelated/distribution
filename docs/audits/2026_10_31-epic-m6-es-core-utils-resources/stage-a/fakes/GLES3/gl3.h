/* T36 (#683) S0: a stand-in for <GLES3/gl3.h>, declarations only (no real header on this
   host). Constants get distinct values so a switch over GL enums has no duplicate case. */
#ifndef T36_FAKE_GLES3_GL3_H
#define T36_FAKE_GLES3_GL3_H
#include <cstdint>
typedef unsigned int GLenum; typedef unsigned char GLboolean; typedef unsigned int GLbitfield;
typedef signed char GLbyte; typedef short GLshort; typedef int GLint; typedef int GLsizei;
typedef unsigned char GLubyte; typedef unsigned short GLushort; typedef unsigned int GLuint;
typedef float GLfloat; typedef float GLclampf; typedef double GLdouble; typedef void GLvoid;
typedef char GLchar; typedef std::intptr_t GLintptr; typedef std::ptrdiff_t GLsizeiptr;
typedef std::int64_t GLint64; typedef std::uint64_t GLuint64; typedef struct __GLsync* GLsync;
#ifndef GL_ACTIVE_UNIFORMS
#define GL_ACTIVE_UNIFORMS 0x1001
#endif
#ifndef GL_ALPHA
#define GL_ALPHA 0x1002
#endif
#ifndef GL_ALREADY_SIGNALED
#define GL_ALREADY_SIGNALED 0x1003
#endif
#ifndef GL_ALWAYS
#define GL_ALWAYS 0x1004
#endif
#ifndef GL_ARB_
#define GL_ARB_ 0x1005
#endif
#ifndef GL_ARRAY_BUFFER
#define GL_ARRAY_BUFFER 0x1006
#endif
#ifndef GL_BLEND
#define GL_BLEND 0x1007
#endif
#ifndef GL_BOOL
#define GL_BOOL 0x1008
#endif
#ifndef GL_CHECK_ERROR
#define GL_CHECK_ERROR 0x1009
#endif
#ifndef GL_CLAMP_TO_EDGE
#define GL_CLAMP_TO_EDGE 0x100a
#endif
#ifndef GL_COLOR_ATTACHMENT0
#define GL_COLOR_ATTACHMENT0 0x100b
#endif
#ifndef GL_COLOR_BUFFER_BIT
#define GL_COLOR_BUFFER_BIT 0x100c
#endif
#ifndef GL_COMPILE_STATUS
#define GL_COMPILE_STATUS 0x100d
#endif
#ifndef GL_CONDITION_SATISFIED
#define GL_CONDITION_SATISFIED 0x100e
#endif
#ifndef GL_DEPTH
#define GL_DEPTH 0x100f
#endif
#ifndef GL_DEPTH_TEST
#define GL_DEPTH_TEST 0x1010
#endif
#ifndef GL_DRAW_FRAMEBUFFER
#define GL_DRAW_FRAMEBUFFER 0x1011
#endif
#ifndef GL_DST_ALPHA
#define GL_DST_ALPHA 0x1012
#endif
#ifndef GL_DST_COLOR
#define GL_DST_COLOR 0x1013
#endif
#ifndef GL_ELEMENT_ARRAY_BUFFER
#define GL_ELEMENT_ARRAY_BUFFER 0x1014
#endif
#ifndef GL_EQUAL
#define GL_EQUAL 0x1015
#endif
#ifndef GL_ES
#define GL_ES 0x1016
#endif
#ifndef GL_EXTENSIONS
#define GL_EXTENSIONS 0x1017
#endif
#ifndef GL_FALSE
#define GL_FALSE 0x1018
#endif
#ifndef GL_FLOAT
#define GL_FLOAT 0x1019
#endif
#ifndef GL_FLOAT_VEC2
#define GL_FLOAT_VEC2 0x101a
#endif
#ifndef GL_FLOAT_VEC4
#define GL_FLOAT_VEC4 0x101b
#endif
#ifndef GL_FRAGMENT_SHADER
#define GL_FRAGMENT_SHADER 0x101c
#endif
#ifndef GL_FRAMEBUFFER
#define GL_FRAMEBUFFER 0x101d
#endif
#ifndef GL_FRAMEBUFFER_COMPLETE
#define GL_FRAMEBUFFER_COMPLETE 0x101e
#endif
#ifndef GL_GPU_MEMORY_INFO_TOTAL_AVAILABLE_MEMORY_NVX
#define GL_GPU_MEMORY_INFO_TOTAL_AVAILABLE_MEMORY_NVX 0x101f
#endif
#ifndef GL_GPU_MEM_INFO_CURRENT_AVAILABLE_MEM_NVX
#define GL_GPU_MEM_INFO_CURRENT_AVAILABLE_MEM_NVX 0x1020
#endif
#ifndef GL_INFO_LOG_LENGTH
#define GL_INFO_LOG_LENGTH 0x1021
#endif
#ifndef GL_INT
#define GL_INT 0x1022
#endif
#ifndef GL_INVALID_OPERATION
#define GL_INVALID_OPERATION 0x1023
#endif
#ifndef GL_INVALID_VALUE
#define GL_INVALID_VALUE 0x1024
#endif
#ifndef GL_KEEP
#define GL_KEEP 0x1025
#endif
#ifndef GL_KHR_
#define GL_KHR_ 0x1026
#endif
#ifndef GL_LINEAR
#define GL_LINEAR 0x1027
#endif
#ifndef GL_LINEAR_MIPMAP_LINEAR
#define GL_LINEAR_MIPMAP_LINEAR 0x1028
#endif
#ifndef GL_LINES
#define GL_LINES 0x1029
#endif
#ifndef GL_LINK_STATUS
#define GL_LINK_STATUS 0x102a
#endif
#ifndef GL_LUMINANCE_ALPHA
#define GL_LUMINANCE_ALPHA 0x102b
#endif
#ifndef GL_MAJOR_VERSION
#define GL_MAJOR_VERSION 0x102c
#endif
#ifndef GL_MAP_INVALIDATE_BUFFER_BIT
#define GL_MAP_INVALIDATE_BUFFER_BIT 0x102d
#endif
#ifndef GL_MAP_WRITE_BIT
#define GL_MAP_WRITE_BIT 0x102e
#endif
#ifndef GL_MINOR_VERSION
#define GL_MINOR_VERSION 0x102f
#endif
#ifndef GL_NEAREST
#define GL_NEAREST 0x1030
#endif
#ifndef GL_NOTEQUAL
#define GL_NOTEQUAL 0x1031
#endif
#ifndef GL_NO_ERROR
#define GL_NO_ERROR 0x1032
#endif
#ifndef GL_NUM_EXTENSIONS
#define GL_NUM_EXTENSIONS 0x1033
#endif
#ifndef GL_NVX_
#define GL_NVX_ 0x1034
#endif
#ifndef GL_ONE
#define GL_ONE 0x1035
#endif
#ifndef GL_ONE_MINUS_DST_ALPHA
#define GL_ONE_MINUS_DST_ALPHA 0x1036
#endif
#ifndef GL_ONE_MINUS_DST_COLOR
#define GL_ONE_MINUS_DST_COLOR 0x1037
#endif
#ifndef GL_ONE_MINUS_SRC_ALPHA
#define GL_ONE_MINUS_SRC_ALPHA 0x1038
#endif
#ifndef GL_ONE_MINUS_SRC_COLOR
#define GL_ONE_MINUS_SRC_COLOR 0x1039
#endif
#ifndef GL_PACK_ALIGNMENT
#define GL_PACK_ALIGNMENT 0x103a
#endif
#ifndef GL_PIXEL_UNPACK_BUFFER
#define GL_PIXEL_UNPACK_BUFFER 0x103b
#endif
#ifndef GL_R8
#define GL_R8 0x103c
#endif
#ifndef GL_READ_FRAMEBUFFER
#define GL_READ_FRAMEBUFFER 0x103d
#endif
#ifndef GL_RED
#define GL_RED 0x103e
#endif
#ifndef GL_RENDERER
#define GL_RENDERER 0x103f
#endif
#ifndef GL_REPEAT
#define GL_REPEAT 0x1040
#endif
#ifndef GL_REPLACE
#define GL_REPLACE 0x1041
#endif
#ifndef GL_RGBA
#define GL_RGBA 0x1042
#endif
#ifndef GL_RGBA8
#define GL_RGBA8 0x1043
#endif
#ifndef GL_SCISSOR_TEST
#define GL_SCISSOR_TEST 0x1044
#endif
#ifndef GL_SHADING_LANGUAGE_VERSION
#define GL_SHADING_LANGUAGE_VERSION 0x1045
#endif
#ifndef GL_SRC_ALPHA
#define GL_SRC_ALPHA 0x1046
#endif
#ifndef GL_SRC_COLOR
#define GL_SRC_COLOR 0x1047
#endif
#ifndef GL_STATIC_DRAW
#define GL_STATIC_DRAW 0x1048
#endif
#ifndef GL_STENCIL
#define GL_STENCIL 0x1049
#endif
#ifndef GL_STENCIL_BUFFER_BIT
#define GL_STENCIL_BUFFER_BIT 0x104a
#endif
#ifndef GL_STENCIL_TEST
#define GL_STENCIL_TEST 0x104b
#endif
#ifndef GL_STREAM_DRAW
#define GL_STREAM_DRAW 0x104c
#endif
#ifndef GL_SYNC_GPU_COMMANDS_COMPLETE
#define GL_SYNC_GPU_COMMANDS_COMPLETE 0x104d
#endif
#ifndef GL_TEXTURE0
#define GL_TEXTURE0 0x104e
#endif
#ifndef GL_TEXTURE_2D
#define GL_TEXTURE_2D 0x104f
#endif
#ifndef GL_TEXTURE_MAG_FILTER
#define GL_TEXTURE_MAG_FILTER 0x1050
#endif
#ifndef GL_TEXTURE_MIN_FILTER
#define GL_TEXTURE_MIN_FILTER 0x1051
#endif
#ifndef GL_TEXTURE_WRAP_S
#define GL_TEXTURE_WRAP_S 0x1052
#endif
#ifndef GL_TEXTURE_WRAP_T
#define GL_TEXTURE_WRAP_T 0x1053
#endif
#ifndef GL_TRIANGLES
#define GL_TRIANGLES 0x1054
#endif
#ifndef GL_TRIANGLE_FAN
#define GL_TRIANGLE_FAN 0x1055
#endif
#ifndef GL_TRIANGLE_STRIP
#define GL_TRIANGLE_STRIP 0x1056
#endif
#ifndef GL_TRUE
#define GL_TRUE 0x1057
#endif
#ifndef GL_UNPACK_ALIGNMENT
#define GL_UNPACK_ALIGNMENT 0x1058
#endif
#ifndef GL_UNSIGNED_BYTE
#define GL_UNSIGNED_BYTE 0x1059
#endif
#ifndef GL_UNSIGNED_SHORT
#define GL_UNSIGNED_SHORT 0x105a
#endif
#ifndef GL_VENDOR
#define GL_VENDOR 0x105b
#endif
#ifndef GL_VERSION
#define GL_VERSION 0x105c
#endif
#ifndef GL_VERTEX_SHADER
#define GL_VERTEX_SHADER 0x105d
#endif
#ifndef GL_WAIT_FAILED
#define GL_WAIT_FAILED 0x105e
#endif
#ifndef GL_ZERO
#define GL_ZERO 0x105f
#endif
GLuint glActiveTexture(...);
GLuint glAttachShader(...);
GLuint glBindBuffer(...);
GLuint glBindFramebuffer(...);
GLuint glBindTexture(...);
GLuint glBindVertexArray(...);
GLuint glBlendFunc(...);
GLuint glBlitFramebuffer(...);
GLuint glBufferData(...);
GLuint glBufferSubData(...);
GLuint glCapabilities(...);
GLenum glCheckFramebufferStatus(...);
GLuint glClear(...);
GLuint glClearColor(...);
GLuint glClearStencil(...);
GLenum glClientWaitSync(...);
GLuint glColorMask(...);
GLuint glCompileShader(...);
GLuint glCreateProgram(...);
GLuint glCreateShader(...);
GLuint glDeleteBuffers(...);
GLuint glDeleteFramebuffers(...);
GLuint glDeleteProgram(...);
GLuint glDeleteShader(...);
GLuint glDeleteSync(...);
GLuint glDeleteTextures(...);
GLuint glDeleteVertexArrays(...);
GLuint glDisable(...);
GLuint glDisableVertexAttribArray(...);
GLuint glDrawArrays(...);
GLuint glDrawElements(...);
GLuint glEnable(...);
GLuint glEnableVertexAttribArray(...);
GLsync glFenceSync(...);
GLuint glFlush(...);
GLuint glFramebufferTexture2D(...);
GLuint glGenBuffers(...);
GLuint glGenFramebuffers(...);
GLuint glGenTextures(...);
GLuint glGenVertexArrays(...);
GLuint glGenerateMipmap(...);
GLuint glGetActiveUniform(...);
GLint glGetAttribLocation(...);
GLenum glGetError(...);
GLuint glGetIntegerv(...);
GLuint glGetProgramInfoLog(...);
GLuint glGetProgramiv(...);
GLuint glGetShaderInfoLog(...);
GLuint glGetShaderiv(...);
const GLubyte* glGetString(...);
const GLubyte* glGetStringi(...);
GLint glGetUniformLocation(...);
GLuint glInvalidateFramebuffer(...);
GLuint glLinkProgram(...);
void* glMapBufferRange(...);
GLuint glPixelStorei(...);
GLuint glScissor(...);
GLuint glShaderSource(...);
GLuint glStencilFunc(...);
GLuint glStencilOp(...);
GLuint glTexImage2D(...);
GLuint glTexParameteri(...);
GLuint glTexStorage2D(...);
GLuint glTexSubImage2D(...);
GLuint glUniform1f(...);
GLuint glUniform1i(...);
GLuint glUniform2f(...);
GLuint glUniform4f(...);
GLuint glUniformMatrix4fv(...);
GLuint glUnmapBuffer(...);
GLuint glUseProgram(...);
GLuint glVertexAttribPointer(...);
GLuint glViewport(...);
#endif
