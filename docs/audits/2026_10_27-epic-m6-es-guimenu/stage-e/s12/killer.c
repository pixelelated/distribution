/* T26 (#673) S12, from T21's stage-B killer.c (#668; copied by git show at
 * 4df674cc82), with stdio's fopen, fwrite and fclose counted as well: glibc's
 * stdio opens and writes through internal calls a preloaded open/write never
 * sees, so without them no kill could land inside writeAllText.
 *
 * T21 (#668) stage B: kill a writer at every step (D-CLOUD-078's test).
 *
 * LD_PRELOAD'd into state-fixture. Counts the file-system calls a writer
 * makes -- open, write, fsync, fchmod, close, rename, link, unlink -- and
 * with KILL_AT=N sends the process SIGKILL just before the Nth, so nothing
 * of that call or after it happens. Without KILL_AT it only counts, and
 * prints "ops=<n>" to stderr at exit, which is how a sweep knows its range.
 *
 *   gcc -shared -fPIC -O0 -o killer.so killer.c -ldl
 */
#define _GNU_SOURCE
#include <dlfcn.h>
#include <fcntl.h>
#include <signal.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>

static long ops = 0;
static long killAt = -1;

static void step(void)
{
	if (killAt < 0)
	{
		const char* e = getenv("KILL_AT");
		killAt = e ? atol(e) : 0;
	}
	ops++;
	if (killAt > 0 && ops == killAt)
		kill(getpid(), SIGKILL);
}

__attribute__((destructor)) static void report(void)
{
	char line[64];
	int n = snprintf(line, sizeof line, "ops=%ld\n", ops);
	syscall(SYS_write, 2, line, (size_t) n);
}

#define NEXT(name) static __typeof__(name)* real; if (!real) real = (__typeof__(name)*) dlsym(RTLD_NEXT, #name)

int open(const char* path, int flags, ...)
{
	NEXT(open);
	mode_t mode = 0;
	if (flags & O_CREAT) { va_list ap; va_start(ap, flags); mode = va_arg(ap, mode_t); va_end(ap); }
	step();
	return real(path, flags, mode);
}

int open64(const char* path, int flags, ...)
{
	NEXT(open64);
	mode_t mode = 0;
	if (flags & O_CREAT) { va_list ap; va_start(ap, flags); mode = va_arg(ap, mode_t); va_end(ap); }
	step();
	return real(path, flags, mode);
}

ssize_t write(int fd, const void* buf, size_t n) { NEXT(write); step(); return real(fd, buf, n); }
int fsync(int fd) { NEXT(fsync); step(); return real(fd); }
int fchmod(int fd, mode_t mode) { NEXT(fchmod); step(); return real(fd, mode); }
int close(int fd) { NEXT(close); step(); return real(fd); }
int rename(const char* a, const char* b) { NEXT(rename); step(); return real(a, b); }
int link(const char* a, const char* b) { NEXT(link); step(); return real(a, b); }
int unlink(const char* p) { NEXT(unlink); step(); return real(p); }
FILE* fopen(const char* p, const char* m) { NEXT(fopen); step(); return real(p, m); }
FILE* fopen64(const char* p, const char* m) { NEXT(fopen64); step(); return real(p, m); }
size_t fwrite(const void* b, size_t s, size_t n, FILE* f) { NEXT(fwrite); step(); return real(b, s, n, f); }
int fclose(FILE* f) { NEXT(fclose); step(); return real(f); }
