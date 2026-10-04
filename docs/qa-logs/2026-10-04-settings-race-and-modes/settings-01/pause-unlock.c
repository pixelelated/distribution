#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <stdatomic.h>

/* Test-only interposer: never alter unlink's return value or production files.
 * Pause the installed ES after its first two settings-lock releases, outside
 * the lock. Every other program/path is untouched. Each pause is bounded. */
int unlink(const char *path)
{
    static int (*real_unlink)(const char *);
    static _Atomic unsigned calls;
    if (!real_unlink) real_unlink = dlsym(RTLD_NEXT, "unlink");
    if (!real_unlink) _exit(120);
    int rc = real_unlink(path), saved = errno;
    const char *enabled = getenv("PIXELELATED_SETTINGS_RACE");
    if (rc == 0 && enabled && !strcmp(enabled, "owned-qa-320") &&
        !strcmp(path, "/tmp/.system.cfg.lock")) {
        char exe[PATH_MAX];
        ssize_t n = readlink("/proc/self/exe", exe, sizeof(exe)-1);
        if (n > 0) {
            exe[n] = 0;
            if (!strcmp(exe, "/usr/bin/emulationstation")) {
                unsigned step = atomic_fetch_add(&calls, 1) + 1;
                if (step <= 2) {
                    char ready[128], release[128], text[128];
                    snprintf(ready, sizeof(ready), "/tmp/pixelelated-settings-race/ready-%u", step);
                    snprintf(release, sizeof(release), "/tmp/pixelelated-settings-race/release-%u", step);
                    int fd = open(ready, O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW, 0600);
                    if (fd < 0) _exit(121);
                    int len = snprintf(text, sizeof(text), "%ld %u\n", (long)getpid(), step);
                    if (write(fd, text, len) != len || close(fd)) _exit(122);
                    struct timespec start, now, delay = {0, 10000000};
                    clock_gettime(CLOCK_MONOTONIC, &start);
                    while (access(release, F_OK)) {
                        clock_gettime(CLOCK_MONOTONIC, &now);
                        if (now.tv_sec - start.tv_sec >= 120) _exit(123);
                        nanosleep(&delay, NULL);
                    }
                }
            }
        }
    }
    errno = saved;
    return rc;
}
