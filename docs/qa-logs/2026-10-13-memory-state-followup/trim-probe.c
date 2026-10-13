#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <fcntl.h>
#include <malloc.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
static int (*real_system)(const char *);
static long long ns(void) {struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t);return (long long)t.tv_sec*1000000000+t.tv_nsec;}
struct memory_sample { unsigned long pss, anon; };
static unsigned long parse_metric(char *buf, const char *key) {
 char *p=strstr(buf,key),*end=NULL;
 if(!p)_exit(117);
 errno=0;unsigned long value=strtoul(p+strlen(key),&end,10);
 if(errno||end==p+strlen(key)||strncmp(end," kB",3))_exit(117);
 return value;
}
static struct memory_sample memory(void) {
 char buf[8192];int f=open("/proc/self/smaps_rollup",O_RDONLY|O_CLOEXEC);
 if(f<0)_exit(117);
 ssize_t n=read(f,buf,sizeof(buf)-1);int error=errno;close(f);errno=error;
 if(n<=0||n==(ssize_t)sizeof(buf)-1)_exit(117);
 buf[n]=0;
 return (struct memory_sample){parse_metric(buf,"\nPss:"),parse_metric(buf,"\nPss_Anon:")};
}
__attribute__((constructor)) static void init(void) {
 const char *pre=getenv("LD_PRELOAD");
 if(!pre||strcmp(pre,"/storage/qa570trim/trim-probe.so"))_exit(124);
 unsetenv("LD_PRELOAD");
 real_system=dlsym(RTLD_NEXT,"system");if(!real_system)_exit(123);
 char exe[512];ssize_t n=readlink("/proc/self/exe",exe,sizeof(exe)-1);if(n<0)_exit(122);exe[n]=0;
 if(strcmp(exe,"/usr/bin/emulationstation"))_exit(121);
}
int system(const char *cmd) {
 int saved=errno;
 if(cmd && !strcmp(cmd,"/usr/bin/cloud_oauth wait")) {
  char mode=0;int f=open("/storage/qa570trim/mode",O_RDONLY|O_CLOEXEC|O_NOFOLLOW);
  if(f<0||read(f,&mode,1)!=1)_exit(120);
  close(f);if(mode!='0'&&mode!='1')_exit(119);
  struct memory_sample before=memory();struct mallinfo2 b=mallinfo2();
  long long t0=ns();int rc=mode=='1'?malloc_trim(0):0;long long t1=ns();
  struct mallinfo2 a=mallinfo2();struct memory_sample after=memory();
  char line[2048];int n=snprintf(line,sizeof(line),"{\"pid\":%ld,\"mode\":%c,\"mono_ns\":%lld,\"duration_ns\":%lld,\"trim_return\":%d,\"pss_before_kib\":%lu,\"pss_after_kib\":%lu,\"anon_before_kib\":%lu,\"anon_after_kib\":%lu,\"arena_before\":%zu,\"arena_after\":%zu,\"used_before\":%zu,\"used_after\":%zu,\"free_before\":%zu,\"free_after\":%zu}\n",(long)getpid(),mode,t0,t1-t0,rc,before.pss,after.pss,before.anon,after.anon,b.arena,a.arena,b.uordblks,a.uordblks,b.fordblks,a.fordblks);
  f=open("/storage/qa570trim/probe.jsonl",O_WRONLY|O_CREAT|O_APPEND|O_CLOEXEC|O_NOFOLLOW,0600);if(f<0||n<0||(size_t)n>=sizeof(line)||write(f,line,n)!=n)_exit(118);
  close(f);
 }
 errno=saved;return real_system(cmd);
}
