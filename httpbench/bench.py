import time, threading, urllib.request
from dataclasses import dataclass, field

@dataclass
class Result:
    total: int = 0
    success: int = 0
    failed: int = 0
    latencies: list = field(default_factory=list)

    @property
    def avg_ms(self):
        return sum(self.latencies) / len(self.latencies) * 1000 if self.latencies else 0

    @property
    def p95_ms(self):
        if not self.latencies:
            return 0
        s = sorted(self.latencies)
        return s[int(len(s) * 0.95)] * 1000

def _worker(url, count, result, lock):
    for _ in range(count):
        t0 = time.perf_counter()
        try:
            req = urllib.request.urlopen(url, timeout=10)
            req.read()
            elapsed = time.perf_counter() - t0
            with lock:
                result.success += 1
                result.latencies.append(elapsed)
        except Exception:
            with lock:
                result.failed += 1
        with lock:
            result.total += 1

def run_bench(url, concurrency=10, requests_per_worker=50):
    result = Result()
    lock = threading.Lock()
    threads = []
    for _ in range(concurrency):
        t = threading.Thread(target=_worker, args=(url, requests_per_worker, result, lock))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    return result

if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
    print(f"Benchmarking {url} ...")
    r = run_bench(url, concurrency=10, requests_per_worker=20)
    print(f"Total: {r.total} | OK: {r.success} | Fail: {r.failed}")
    print(f"Avg: {r.avg_ms:.1f}ms | P95: {r.p95_ms:.1f}ms")
