# Agentic Stack Local TODO Format and Requirements

**Purpose:** Document the user-validated format and design constraints for the Agentic Stack local TODO system (`~/.agentic-stack/local-todo.md` and daily reminder script).

**Last updated:** 2026-05-23

---

## User Requirements (explicit corrections from 2026-05-23 session)

### 1. Unified numbering with stable unique IDs

**User directive:**  
*"Не дели список на два разных, потому что сложно указывать на номерацию. На конкретной задачу должна иметь улибо идишник... по которому можно сказать, пока что выполнено."*

**Translation:**  
Do not split the list with separate numbering systems; it makes referencing tasks difficult. Each task must have a unique ID (or any label) by which you can unambiguously refer to it and say "this one is done."

**Implementation:**
- Every task section in `local-todo.md` has an `ID:` field immediately after the heading (e.g., `ID: backup-001`)
- The reminder script (`agentic_stack_todo_reminder.py`) displays the ID instead of sequential numbering: `[backup-001] [P1] Task title — status`
- IDs are stable across sessions and do not change when tasks move between sections or priority changes
- Format pattern: `<topic>-<nnn>` (e.g., `backup-001`, `telegram-integration-003`, `server-doctor-002`)

### 2. Task naming clarity to avoid topic confusion

**User directive:**  
*"И архивист бэкап, я бы не называла архивист, потому что аналогия стопика в архивист кажется, что это одна и та же самая задача. Я бы это просто был назвал бэкап."*

**Translation:**  
Do not name tasks with topic-like names that could be confused with Telegram topics or other infrastructure components. For example, "Archivist backup" could be confused with the Archivist topic itself; just call it "Backup."

**Principle:**  
Task titles should describe the work, not reuse infrastructure component names unless the task *is* setting up that component.

### 3. Completed tasks moved to Done section

Tasks marked completed (`Status: completed`) should be moved from `## Open` to `## Done` with:
- `Completed:` date field
- `Outcome:` summary of what was achieved (concise bullet list)
- Original `Owner:` and `ID:` preserved for traceability

### 4. Reminder script format

The daily reminder script (`~/.hermes/scripts/agentic_stack_todo_reminder.py`) must:

- Parse the `ID:` field from task bodies (added to `FIELD_NAMES` and `BLOCK_BOUNDARY_FIELDS`)
- Display tasks with ID prefix: `[backup-001] [P1] Task title — status`
- Show maximum 3 focus items with full detail
- Show backlog items (up to 7) with one-line format including ID: `[server-doctor-002] [P2] Title — status; следующий шаг: ...`
- Run at 07:00 MSK (21:00 Pacific) via cronjob `59e7544595e8`
- Deliver to Mikhail DM only (`telegram:Mikhail`)

---

## File Structure

### `local-todo.md` task format

```markdown
### Task Title Here

ID: unique-id-001
Status: pending
Priority: P1
Lane: Next
Owner: Name — role
Review: YYYY-MM-DD HH:MM MSK
Timebox: time estimate
Due: optional hard deadline

Outcome:
- Expected results
- Deliverables

Next action:
- Single concrete next step

Blocker:
- Optional blocking issue

Decision needed:
- Optional decision from owner
```

### Reminder script key logic

```python
FIELD_NAMES = ['ID', 'Status', 'Priority', ...]
BLOCK_BOUNDARY_FIELDS = ['ID', 'Status', 'Priority', ...]

item = {
    'id': parse_field(body, 'ID') or 'no-id',
    'title': title,
    'priority': priority,
    ...
}

title = f"[{item['id']}] [{item['priority']}] {item['title']} — {status_ru}"
```

---

## Quality Rules

1. **ID stability:** IDs are chosen once when a task is created and never change.
2. **ID uniqueness:** No two tasks (Open or Done) share the same ID.
3. **Avoid topic name collision:** Task titles should not reuse infrastructure component/topic names unless the task is about that component.
4. **Completed tasks migrated:** Tasks marked `Status: completed` must be moved to `## Done` with outcome summary.
5. **Single source of truth:** The markdown file is the source; the reminder script is read-only display.

---

## Integration Points

- **Cronjob:** `59e7544595e8` runs the reminder script daily at 07:00 MSK → Mikhail DM
- **Source file:** `/Users/xbr/.agentic-stack/local-todo.md`
- **Reminder script:** `/Users/xbr/.hermes/scripts/agentic_stack_todo_reminder.py`
- **Delivery:** Telegram only, concise Russian output, max 3 focus items with detail + backlog list

---

## Maintenance Notes

- When adding new tasks, assign a unique ID immediately after the heading.
- Use descriptive work-focused titles, not infrastructure component names.
- Update `Updated:` timestamp in file header when making changes.
- Test reminder script after format changes: `python3 ~/.hermes/scripts/agentic_stack_todo_reminder.py`
