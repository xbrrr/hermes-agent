# Subconscious Upgrade Specification v1.0 (2026-05-22)

**Context:** Mikhail asked to upgrade Hermes' local Subconscious memory provider with three features: metrics/observability, natural forgetting (TTL), and conflict detection. This reference captures the design from session 20260522.

**Target files:**
- `plugins/memory/subconscious/store.py`
- `plugins/memory/subconscious/consolidate.py`
- `plugins/memory/subconscious/__init__.py`
- `tests/plugins/memory/test_subconscious_provider.py`

**Implementation:** Delegated to Bud/OpenClaw via shaw, branch `subconscious-supermind`.

---

## 1. Metrics & Observability

### DB table: `metrics_snapshots`

```sql
CREATE TABLE IF NOT EXISTS metrics_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_date TEXT NOT NULL UNIQUE,
    total_memories INTEGER DEFAULT 0,
    working_count INTEGER DEFAULT 0,
    episodic_count INTEGER DEFAULT 0,
    semantic_count INTEGER DEFAULT 0,
    procedural_count INTEGER DEFAULT 0,
    edge_count INTEGER DEFAULT 0,
    duplicate_groups INTEGER DEFAULT 0,
    avg_confidence REAL DEFAULT 0.0,
    recall_precision_at_5 REAL DEFAULT 0.0,
    stale_memory_count INTEGER DEFAULT 0,
    conflict_count INTEGER DEFAULT 0,
    autonomy_violations INTEGER DEFAULT 0,
    created_at TEXT NOT NULL
);
```

### Store method: `capture_metrics_snapshot()`

Daily snapshot capturing:
- Layer counts (working, episodic, semantic, procedural)
- Edge count, duplicate groups
- Average confidence across all memories
- Stale memory count (working items >21 days old)
- Conflict count (from `detected_conflicts` table)

Returns dict with all metrics. Inserts into `metrics_snapshots` with `ON CONFLICT` upsert.

### New action: `metrics`

Add to `_TOOL_SCHEMA` enum: `"metrics"`

Handler returns snapshot JSON.

---

## 2. Natural Forgetting

### Auto-set TTL in `consolidate.py`

**New rule:**
- `working`: 7 days (was 14)
- `procedural`: 90 days (new)
- `semantic`: None (eternal — policies/rules)
- `episodic`: None (eternal — facts)

Update line 147 in `consolidate.py`:
```python
ttl_days=7 if layer == "working" else (90 if layer == "procedural" else None),
```

### Store method: `expire_stale_memories()`

Deletes memories where:
```sql
ttl_days IS NOT NULL AND julianday('now') - julianday(created_at) > ttl_days
```

Edges cascade automatically via FK.

Returns:
```json
{
  "success": true,
  "expired_count": N,
  "expired_ids": [...]
}
```

### New action: `expire`

Add to enum: `"expire"`

Handler calls `expire_stale_memories()` and returns result.

---

## 3. Conflict Detection

### DB table: `detected_conflicts`

```sql
CREATE TABLE IF NOT EXISTS detected_conflicts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    memory_id_1 INTEGER NOT NULL,
    memory_id_2 INTEGER NOT NULL,
    conflict_type TEXT NOT NULL,
    severity TEXT NOT NULL CHECK(severity IN ('low','medium','high')),
    detected_at TEXT NOT NULL,
    resolved BOOLEAN DEFAULT 0,
    UNIQUE(memory_id_1, memory_id_2, conflict_type),
    FOREIGN KEY(memory_id_1) REFERENCES memories(id) ON DELETE CASCADE,
    FOREIGN KEY(memory_id_2) REFERENCES memories(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_conflicts_resolved ON detected_conflicts(resolved);
```

### Store method: `detect_conflicts()`

Scans `semantic` + `procedural` layers for contradictory rules using negation pairs:

```python
negations = {
    "must": "must not",
    "always": "never",
    "should": "should not",
    "requires": "prohibits",
    "allowed": "blocked",
    "executes": "coordinates only",
    "implements": "delegates",
}
```

Returns:
```json
{
  "success": true,
  "conflicts_found": N,
  "conflicts": [
    {
      "memory_id_1": 123,
      "memory_id_2": 456,
      "conflict_type": "must_vs_must not",
      "severity": "high"
    }
  ]
}
```

### New action: `conflicts`

Add to enum: `"conflicts"`

Handler calls `detect_conflicts()` and returns result.

### Update `status()`

Add `conflict_count` to status output:

```python
conflict_count = int(self._conn.execute(
    "SELECT COUNT(*) AS n FROM detected_conflicts WHERE resolved = 0"
).fetchone()["n"])
```

Return in `status()` dict.

---

## 4. Integration into `consolidate.py`

At end of `run_consolidation()`, after `store.finish_run()`:

```python
if not dry_run:
    # Capture daily metrics
    store.capture_metrics_snapshot()
    
    # Expire stale memories
    expire_result = store.expire_stale_memories()
    stats["expired"] = expire_result.get("expired_count", 0)
    
    # Detect conflicts
    conflict_result = store.detect_conflicts()
    stats["conflicts_detected"] = conflict_result.get("conflicts_found", 0)
    
    store.finish_run(run_key, status="completed", stats=stats)
```

---

## 5. Schema Migration

Add to `SubconsciousStore._init_db()` after existing schema:

```python
# Add new tables for metrics and conflicts
self._conn.executescript("""
CREATE TABLE IF NOT EXISTS metrics_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_date TEXT NOT NULL UNIQUE,
    total_memories INTEGER DEFAULT 0,
    working_count INTEGER DEFAULT 0,
    episodic_count INTEGER DEFAULT 0,
    semantic_count INTEGER DEFAULT 0,
    procedural_count INTEGER DEFAULT 0,
    edge_count INTEGER DEFAULT 0,
    duplicate_groups INTEGER DEFAULT 0,
    avg_confidence REAL DEFAULT 0.0,
    recall_precision_at_5 REAL DEFAULT 0.0,
    stale_memory_count INTEGER DEFAULT 0,
    conflict_count INTEGER DEFAULT 0,
    autonomy_violations INTEGER DEFAULT 0,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS detected_conflicts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    memory_id_1 INTEGER NOT NULL,
    memory_id_2 INTEGER NOT NULL,
    conflict_type TEXT NOT NULL,
    severity TEXT NOT NULL CHECK(severity IN ('low','medium','high')),
    detected_at TEXT NOT NULL,
    resolved BOOLEAN DEFAULT 0,
    UNIQUE(memory_id_1, memory_id_2, conflict_type),
    FOREIGN KEY(memory_id_1) REFERENCES memories(id) ON DELETE CASCADE,
    FOREIGN KEY(memory_id_2) REFERENCES memories(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_conflicts_resolved ON detected_conflicts(resolved);
""")
self._conn.commit()
```

---

## 6. Tests

### Unit test: `tests/plugins/memory/test_subconscious_metrics.py`

```python
import pytest
from pathlib import Path
from plugins.memory.subconscious.store import SubconsciousStore

def test_metrics_snapshot(tmp_path):
    store = SubconsciousStore(tmp_path / "test.db")
    store.add_memory("semantic", "Test rule", tags=["test"], confidence=0.8)
    snapshot = store.capture_metrics_snapshot()
    assert snapshot["total_memories"] == 1
    assert snapshot["semantic_count"] == 1
    assert snapshot["avg_confidence"] > 0

def test_expire_stale_memories(tmp_path):
    store = SubconsciousStore(tmp_path / "test.db")
    # Add working memory with 1-day TTL
    store.add_memory("working", "Old task", ttl_days=1, confidence=0.5)
    # Manually backdate it
    store._conn.execute("UPDATE memories SET created_at = datetime('now', '-2 days')")
    store._conn.commit()
    result = store.expire_stale_memories()
    assert result["expired_count"] == 1

def test_conflict_detection(tmp_path):
    store = SubconsciousStore(tmp_path / "test.db")
    store.add_memory("semantic", "Hermes must execute in topic 1347", confidence=0.9)
    store.add_memory("semantic", "Hermes must not execute in topic 1347", confidence=0.9)
    result = store.detect_conflicts()
    assert result["conflicts_found"] >= 1
    assert any(c["conflict_type"] == "must_vs_must not" for c in result["conflicts"])
```

### Integration test: extend `test_subconscious_provider.py`

```python
def test_new_actions(provider_with_session):
    provider, session_id = provider_with_session
    
    # Metrics
    result = provider.handle_tool_call("subconscious", {"action": "metrics"})
    data = json.loads(result)
    assert data["success"]
    assert "total_memories" in data
    
    # Expire
    result = provider.handle_tool_call("subconscious", {"action": "expire"})
    data = json.loads(result)
    assert data["success"]
    
    # Conflicts
    result = provider.handle_tool_call("subconscious", {"action": "conflicts"})
    data = json.loads(result)
    assert data["success"]
```

---

## 7. Acceptance Criteria

✅ **Metrics:**
- `subconscious(action="metrics")` returns daily snapshot
- DB table `metrics_snapshots` captures baseline for trend analysis

✅ **Forgetting:**
- `working` TTL = 7 days
- `procedural` TTL = 90 days
- `subconscious(action="expire")` clears stale records
- Daily consolidation auto-expires

✅ **Conflicts:**
- `subconscious(action="conflicts")` detects contradictions in semantic/procedural
- `detected_conflicts` table stores findings
- `status()` shows `conflict_count`

✅ **Tests:**
- All unit tests pass
- Integration test coverage for new actions
- No regressions in existing consolidate/search

---

## 8. Rollout Plan

1. Bud implements via shaw in branch `subconscious-supermind`
2. Hermes reviews PR
3. Mikhail approves
4. Merge to main
5. Run first metrics snapshot manually: `subconscious(action="metrics")`
6. Monitor for 3 days
7. Weekly report includes new metrics baseline

---

## Design Notes

**Why these three features?**
- **Metrics** — without baseline tracking, we can't measure if interventions (forgetting, conflict resolution, recall tuning) actually improve the system
- **Forgetting** — working memory bloat was visible (34 items), procedural reflections accumulate over time; TTL prevents unbounded growth
- **Conflict detection** — semantic contradictions (e.g. "Hermes must execute" vs "Hermes must not execute" in same topic) silently degrade recall quality

**Why these TTL values?**
- `working`: 7 days (was 14) — tighter expiry for transient task state
- `procedural`: 90 days — reflections/workflows decay slower than active tasks but shouldn't be eternal
- `semantic`/`episodic`: None — policies and facts are durable by design

**Conflict detection limitations:**
Simple keyword negation pairs. Will miss:
- Paraphrased contradictions ("Hermes implements" vs "Bud executes")
- Multi-hop contradictions across >2 memories
- Context-dependent rules (same action allowed in one topic, blocked in another)

Future: LLM-based semantic conflict detection, but start deterministic/fast.

**Metrics we're NOT capturing yet:**
- `recall_precision_at_5` — requires ground-truth queries + manual labeling
- `autonomy_violations` — needs incident taxonomy first
- Recall latency — not a bottleneck yet (SQLite FTS5 is fast <1000 records)

These can be added incrementally after baseline is established.

---

**Session reference:** 20260522_130800 (Mikhail: "прогони все cons тесты и анализы" → "делай" upgrade cycle)
