#include <stdio.h>
#include <stdlib.h>
#include <ft2build.h>
#include FT_FREETYPE_H
int main(int argc,char**argv){
 FT_Library lib; FT_Face face;
 if(argc!=3 || FT_Init_FreeType(&lib) || FT_New_Face(lib,argv[1],0,&face) || FT_Set_Pixel_Sizes(face,0,atoi(argv[2])))return 2;
 for(unsigned cp=32;cp<9000;cp++){
  unsigned gi=FT_Get_Char_Index(face,cp); if(!gi)continue;
  if(FT_Load_Char(face,cp,FT_LOAD_RENDER))return 3;
  printf("%u %.3f %u\n",cp,face->glyph->metrics.horiAdvance/64.0,face->glyph->bitmap.rows);
 }
 FT_Done_Face(face);FT_Done_FreeType(lib);return 0;
}
