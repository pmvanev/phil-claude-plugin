# LLM Inference

Guidelines extracted from Modular's *LLM Inference Handbook* — <https://handbook.modular.com/>.

**No `paths` frontmatter, deliberately.** This is domain reference material for serving LLMs, not a standard that should fire on every Python file. LLM inference work has no clean glob — it spans serving code, deployment config, and benchmark scripts — and inventing one would be the speculative design the other rules warn against. Consult this rule when doing inference work; add a `paths` glob once a real project shows where those files actually live. `definitions.md` is the precedent for a manual-reference rule.

General acronyms stay in `definitions.md`. This rule owns inference-specific terms, metrics, and sizing math.

---

### Core Philosophy

> **"The best configuration is the one that meets the SLO of your workload rather than simply delivering the highest throughput or the lowest latency."**

There is no fastest configuration, only a configuration that satisfies a stated objective. Decide the SLO first; every number below is meaningless without it.

---

### The Two Phases

Every metric and every optimization hangs off one distinction:

| Phase | Work | Bound by | Metric that reflects it |
|---|---|---|---|
| **Prefill** | Process the input prompt | Compute | **TTFT** |
| **Decode** | Generate output tokens, one at a time | Memory bandwidth | **TPOT / ITL** |

Prefill is parallel over prompt tokens; decode is sequential. They have different bottlenecks, so a change that helps one often hurts the other. Name which phase you are optimizing before you touch anything.

---

### Metrics

**Latency**

| Metric | Definition | Formula |
|---|---|---|
| **TTFT** — time to first token | Delay before the model emits its first token; effectively the prefill time | — |
| **E2EL** — end-to-end latency | Submission to final token | — |
| **TPOT** — time per output token | Average gap between successive tokens | `(E2EL − TTFT) / (output tokens − 1)` |
| **ITL** — inter-token latency | The pause between two consecutive tokens | Mean ITL = TPOT for a single request |
| **Token generation time** | The steady-state decode phase alone | `E2EL − TTFT` |
| **Tail latency** | P90 / P95 / P99 — the worst cases that define an SLA | — |

ITL and TPOT diverge across multiple requests: **ITL is token-weighted** (long responses dominate it), **TPOT is request-weighted** (every request counts once). Pick the one that matches what you are claiming.

**Throughput**

| Metric | Use | Caution |
|---|---|---|
| **RPS** — requests/sec | Coarse capacity | Ignores work per request; short responses inflate it |
| **Input TPS** | Prompt-heavy work (summarization, RAG) | — |
| **Output TPS** | Generation-heavy work (chat) | — |
| **Goodput** | Requests/sec that complete **while meeting the SLO** | The only throughput number that maps to value |

**Report goodput, not throughput.** A server at high TPS that misses its latency target is producing responses nobody will wait for. Requests that violate the SLO are not capacity.

---

### Choose Metrics by Workload

| Workload | Optimize | Why |
|---|---|---|
| **Interactive chat** | TTFT first, then ITL/TPOT | Users judge the start, then the smoothness |
| **Long-form generation** | ITL/TPOT, then E2EL | After the first token, generation speed dominates |
| **Agentic / multi-step** | E2EL | Nothing downstream starts until the full response lands |
| **Batch processing** | TPS and cost per token | Individual latency does not matter |
| **SLO-constrained service** | Goodput | Only conforming requests create value |

A single configuration cannot serve interactive and batch workloads well. Separate them, or accept that one is being under-served.

---

### The Central Tradeoff

Batch size is the main dial, and it trades the two things you care about against each other:

| Direction | Effect |
|---|---|
| **Larger batches** | Higher aggregate TPS, better GPU utilization — and longer queueing delay, worse per-user TPOT |
| **Smaller batches** | Better per-user latency — and idle hardware you are paying for |

Past GPU saturation, performance degrades rather than plateaus. Find the knee empirically against your SLO; do not reason about it.

---

### Sizing GPU Memory

Estimate before you provision:

```
Memory (GB) ≈ P × (Q / 8) × (1 + Overhead)

P        = parameters, in billions
Q        = bits per parameter
Overhead = serving allowance, as a fraction
```

**Weights, by dtype:**

| Precision | Bytes/param | 7B model |
|---|---|---|
| FP32 | 4 | ~28 GB |
| FP16 / BF16 | 2 | ~14 GB |
| FP8 / INT8 | 1 | ~7 GB |
| INT4 / FP4 | 0.5 | ~3.5 GB |

**Overhead is not a rounding error.** The KV cache is usually the largest runtime cost, and it scales with sequence length **and** concurrent requests. Reserve **10–30%** for KV cache, activation buffers, workspace, and framework allocations — and treat that band as a floor, not an answer: long-context workloads need substantially more.

**Fitting is not serving.** If the weights barely fit, you are left with short contexts, small batches, and low concurrency. A model that loads is not a model that serves. Size for max context × target concurrency, not for the weights.

---

### Optimization Techniques

Match the technique to the bottleneck you measured.

| Technique | What it does | Reach for it when |
|---|---|---|
| **Continuous batching** | Admits and retires requests mid-flight instead of in fixed groups | Almost always — static batching wastes the GPU on ragged request lengths |
| **PagedAttention** | Block-based KV cache storage | KV fragmentation limits concurrency |
| **Prefix caching** | Reuses KV cache for shared prompt prefixes | Requests share a system prompt or long common context |
| **KV cache offloading** | Moves KV cache to host or other storage | GPU memory, not compute, is the ceiling |
| **Speculative decoding** | A draft model proposes, the target model verifies | Decode-bound and latency-sensitive; costs extra memory and complexity |
| **Chunked / disaggregated prefill-decode** | Separates the two phases across resources | Prefill spikes are hurting decode latency for others |
| **Inference routing** | Routes on cache locality, queue depth, worker state | Multiple workers with uneven cache or load |
| **Tensor / pipeline / expert / hybrid parallelism** | Splits the model across devices | The model does not fit, or single-device latency is insufficient |
| **Offline batch inference** | Drops latency constraints entirely | No user is waiting |

---

### Operations

- **Observe end to end** — metrics, logs, and events across the whole inference path, not just GPU utilization. Utilization can be high while goodput is zero.
- **Scale on the right signal** — queue depth and SLO attainment lead demand; GPU utilization lags it.
- **Account for chained models** — multi-model pipelines buy specialization and control at the cost of added latency and operational complexity. Budget the latency before adding the hop.
- **Distribute deliberately** — multi-GPU, multi-node, multi-region, and multi-cloud each buy availability or locality and each add failure modes.
- **Price the build** — in-house inference infrastructure carries real build and maintenance cost. Count it against the managed alternative honestly.

---

### Checklist

- [ ] What is the SLO, in explicit numbers?
- [ ] Which phase dominates this workload — prefill or decode?
- [ ] Which metric does the workload actually care about, and am I reporting that one?
- [ ] Am I reporting goodput, or throughput that ignores SLO violations?
- [ ] Am I reporting tail latency (P95/P99), or only a mean?
- [ ] Does the memory estimate include KV cache at **max context × target concurrency**?
- [ ] Do the benchmark's input and output token distributions match production?
- [ ] Do shared prompt prefixes make prefix caching applicable?
- [ ] Are interactive and batch traffic sharing one configuration?

---

### Anti-Patterns to Avoid

| Anti-pattern | Fix |
|---|---|
| **Throughput theatre** — maximizing TPS while missing latency targets | Measure goodput against a stated SLO |
| **Mean-only reporting** — a good average hiding a bad P99 | Report tail latencies; SLAs live there |
| **Sizing by weights** — provisioning for parameters and forgetting KV cache | Size for max context × concurrency, plus headroom |
| **One config for every workload** — chat and batch on the same settings | Separate them, or state which one is under-served |
| **Big batches for interactive traffic** | Batch size trades TPS against TTFT and TPOT — pick per workload |
| **Unrealistic benchmarks** — short prompts and short outputs | Match production token distributions or the numbers mean nothing |
| **Optimizing before measuring** — reaching for speculative decoding or parallelism first | Identify the bound phase, then pick the matching technique |
| **Utilization as health** — a busy GPU treated as a working service | Watch SLO attainment and queue depth |

---

### The Mantra

> **State the SLO. Find the bound phase. Measure goodput and tails. Size for the KV cache, not the weights. Then optimize the thing that is actually limiting you.**
