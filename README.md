# Big models on an AMD AI 395 (Strix Halo)

**English** ｜ [繁體中文](README.zh-TW.md)

Measured numbers and version traps for running large mixture-of-experts models on a
**Ryzen AI Max+ PRO 395** desktop — the chip also sold as **Strix Halo**, **AI 395**,
**gfx1151**, with **Radeon 8060S** graphics and **128 GB of unified memory**.

Two engines, two models, one box, nothing else running. Everything below was measured
on the machine, not estimated.

![What you can run, and how fast](docs/overview.png)

## The short version

A 284-billion-parameter model answers at **13.5 to 15.4 tokens a second** on this box.
A 125-billion-parameter one answers at **39 to 41**. Both hold 32,000 tokens of context
with no measurable slowdown, and both run entirely offline.

That is faster than most people read. It is enough to use one of these as a personal
AI engine: chat, drafting, coding help, asking long documents, or behind your own
application through an ordinary chat endpoint. No subscription, no per-token bill,
nothing leaving the machine.

## The box

| | |
|---|---|
| CPU | AMD Ryzen AI Max+ PRO 395, 32 threads, AVX-512 |
| GPU | Radeon 8060S, RDNA 3.5, `gfx1151`, 40 CU |
| Memory | 128 GB LPDDR5X unified — 96 GiB BIOS carve-out plus 31 GB visible to the OS |
| GTT pool | 15.6 GiB with no boot parameters |
| OS | Ubuntu 24.04.4, kernel 6.17.0-35-generic |
| Driver | amdgpu 6.16.6 (DKMS), ROCm 7.1.1 from the distribution packages |

## DwarfStar with DeepSeek-V4-Flash

[`antirez/ds4`](https://github.com/antirez/ds4), model
`DeepSeek-V4-Flash-IQ2XXS-w2Q2K-AProjQ8-SExpQ8-OutQ8-chat-v2-imatrix-0731.gguf`, 81 GB.

```
make strix-halo
./download_model.sh ds4f-q2
./ds4-server --rocm --host 0.0.0.0 --port 8081 --cors
```

Memory plan it reports at ctx 32768:
`KV 0.78 GiB (raw 0.36 + compressed 0.42) + buffers 0.25 GiB + resident model 80.76 GiB
= 81.79 GiB planned`. It maps 80.76 GiB of tensor spans in **17.7 seconds**.

`ds4-bench --rocm` across context frontiers:

| context | prefill tok/s | decode tok/s | KV bytes |
|--------:|--------------:|-------------:|---------:|
| 2,048 | 142.30 | 15.40 | 52,184,460 |
| 4,096 | 166.64 | 14.44 | 80,373,132 |
| 8,192 | 163.97 | 14.25 | 136,750,476 |
| 16,384 | 158.86 | 14.02 | 249,505,164 |
| 24,576 | 154.34 | 13.78 | 362,259,852 |
| 32,768 | 150.11 | 13.52 | — |

Decode falls 12% from 2K to 32K. Prefill is flat.

**One patch was needed to build.** `rocm/ds4_rocm_deepseek4_vision.cuh` calls `rsqrtf()`
from host code; HIP declares it `__device__` only, so the ROCm build fails where the CUDA
one succeeds. Fixed in [antirez/ds4#1193](https://github.com/antirez/ds4/pull/1193).

## Strata with Qwen3.8-Flash-Next

[`Niko1221/Strata`](https://github.com/Niko1221/Strata) 0.1.40, model
`Qwen3.8-Flash-Next UD-IQ4_XS`, 88 GB, with the engine built against the system ROCm.

| | one request at a time | two in parallel |
|---|---|---|
| decode | 39.0 to 40.9 tok/s | 30.4 tok/s each |
| prefill (6,786-token prompt) | 343 to 367 tok/s | — |
| load from cold | 80 s | 80 s |

With `--expert-cache 16384` it holds 23,550 expert blobs in VRAM, reports a **99.6% hit
rate** and `no file reads` — nothing streams from disk during generation.

## Why both of these fit at all

Neither engine is doing anything secret. Both exploit the same three published ideas,
and it is worth naming them so you can look them up:

**Mixed precision by tensor role.** The hot path — attention projections, shared experts,
the output head — stays at 8 bit. The routed experts, which are most of the file and are
touched rarely, drop to 2 bits. DeepSeek's filename spells the recipe out:
`IQ2XXS-w2Q2K-AProjQ8-SExpQ8-OutQ8`.

**Expert caching.** A mixture-of-experts model fires only a few of its experts per token,
so you cache the popular ones in fast memory and read the rest on demand.

**Speculative decoding.** A small draft head proposes several tokens and the main model
verifies them in one pass. Strata reported 68% of drafts accepted on our prompts.

## Four things that cost us time

**The newest ROCm is not the right ROCm.** The DwarfStar and Strata docs both point at
AMD's TheRock builds. ROCm 7.14.1 from TheRock is incompatible with this kernel's
amdgpu 6.16.6: `hipMalloc` succeeds, `hipGetDeviceCount` and `hipMemGetInfo` succeed, and
then `hipMemcpy` host-to-device returns `invalid argument` for a 1 MiB copy. Same machine,
same GPU, same program, system ROCm 7.1.1: no error.

Checking that the GPU is detected proves nothing. Run [`hip_memcpy_check.c`](hip_memcpy_check.c)
before you blame your model, your quantization, or your build flags.

**Sharing the box costs 4.5x.** The same engine, same settings, measured twice: 8.7 tok/s
while another model's worker held 41 GiB of VRAM and 23 GB of RAM, and **39.0 tok/s**
with the machine to itself. Expert cache hit rate went from 85.1% to 99.6% at the same
time. On this chip memory bandwidth is the constraint, not capacity — so a benchmark
taken on a shared box is not a benchmark. Ours are all exclusive.

**amdgpu is a DKMS module with no kernel ceiling.** `dkms.conf` has `AUTOINSTALL="yes"`
and no `BUILD_EXCLUSIVE_KERNEL`, so installing a newer kernel makes it attempt a build
against it; if that build fails nothing stops you rebooting into a system with no GPU.
That is why `amdgpu-install` holds the HWE kernel packages. Before upgrading, install
only the headers and run `dkms build` as a dry run — do not install the kernel image first.

**The gfx1151 fast paths made no measurable difference here.** Strata enables 18
architecture-specific switches by default. We measured all of them on, each group alone,
and all off: decode stayed between 8.7 and 8.9 tok/s in every case, and the all-off arm
was marginally the fastest. We also hit `unspecified launch failure` intermittently —
same configuration passing once and failing once, with the reported layer number moving
— so single-run experiments cannot attribute it to any switch. The same signature appears
under llama.cpp on this chip, so it is not specific to either engine.

## How you would actually use it

![From a bare box to a conversation](docs/userflow.png)

## Reproducing this

`hip_memcpy_check.c` is the compatibility test. `docs/make_arch.py` and `docs/make_flow.py`
generate the two diagrams. The engine benchmarks are the engines' own: `ds4-bench --rocm
--chat-prompt-file <a prompt of at least 32768 tokens>`, and for Strata the per-request
timings its server logs.

## Credits

The engines are other people's work and both are MIT licensed:
[DwarfStar](https://github.com/antirez/ds4) by Salvatore Sanfilippo, and
[Strata](https://github.com/Niko1221/Strata). The models are
[DeepSeek](https://huggingface.co/deepseek-ai) and [Qwen](https://huggingface.co/Qwen),
also MIT. This repository contributes measurements, a compatibility map and one upstream
patch — not a technique.

Published by [xCloudinfo Corp. Limited（云碩科技股份有限公司）](https://hf.co/xCloudinfo)
under CC BY 4.0. Corrections and numbers from other Strix Halo boxes are welcome; open an
issue with your ROCm version, kernel, carve-out size and the engine's own benchmark output.
