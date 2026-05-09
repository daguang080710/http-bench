# http-bench

Lightweight HTTP benchmark tool with concurrent requests.

## Features
- Thread-based concurrency
- Latency statistics (avg, p95)
- Simple API and CLI

## Usage
```bash
python -m httpbench http://example.com
```

```python
from httpbench import run_bench
r = run_bench("http://localhost:8080", concurrency=20)
print(f"P95: {r.p95_ms:.1f}ms")
```

## License
MIT
