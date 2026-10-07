/* Does this ROCm userspace actually work with this kernel?
 *
 *   hipcc --offload-arch=gfx1151 hip_memcpy_check.c -o hip_memcpy_check
 *   ./hip_memcpy_check
 *
 * hipGetDeviceCount and hipMemGetInfo succeeding proves nothing: a mismatched
 * ROCm userspace reports the GPU correctly and still cannot move a byte onto
 * it. The host-to-device copy is the test that actually fails.
 */
#include <hip/hip_runtime.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n = 0;
    hipError_t e = hipGetDeviceCount(&n);
    printf("hipGetDeviceCount : %-20s (devices: %d)\n", hipGetErrorString(e), n);

    size_t fr = 0, tt = 0;
    e = hipMemGetInfo(&fr, &tt);
    printf("hipMemGetInfo     : %-20s free %.2f GiB of %.2f GiB\n",
           hipGetErrorString(e), fr / 1073741824.0, tt / 1073741824.0);

    void *dev = NULL;
    e = hipMalloc(&dev, 1ull << 30);
    printf("hipMalloc 1 GiB   : %s\n", hipGetErrorString(e));
    if (e != hipSuccess) return 1;

    char *host = malloc(1 << 20);
    if (!host) return 1;
    e = hipMemcpy(dev, host, 1 << 20, hipMemcpyHostToDevice);
    printf("hipMemcpy 1 MiB   : %s   <-- the one that matters\n",
           hipGetErrorString(e));

    hipFree(dev);
    free(host);
    return e == hipSuccess ? 0 : 1;
}
