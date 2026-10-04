#include <cstdio>
#include <vector>
#include <algorithm>
#define NANOSVG_IMPLEMENTATION
#include "nanosvg.h"
#define NANOSVGRAST_IMPLEMENTATION
#include "nanosvgrast.h"
int main(int argc,char**argv) {
 if(argc!=3)return 2;
 NSVGimage*im=nsvgParseFromFile(argv[1],"px",96);if(!im)return 1;
 float scale=600/im->width;int w=600,h=int(im->height*scale);
 std::vector<unsigned char>px(w*h*4);
 NSVGrasterizer*r=nsvgCreateRasterizer();nsvgRasterize(r,im,0,0,scale,px.data(),w,h,w*4);
 FILE*f=fopen(argv[2],"wb");if(!f)return 1;fprintf(f,"P6\n%d %d\n255\n",w,h);
 for(int i=0;i<w*h;i++)for(int c=0;c<3;c++){unsigned a=px[4*i+3];fputc((px[4*i+c]*a+32*(255-a))/255,f);}
 fclose(f);nsvgDeleteRasterizer(r);nsvgDelete(im);return 0;
}
