# Filter Configuration

## config.json FILTER (Fetch Stage)

Configure **time** and **include** filters in `config.json` to control which emails are fetched from Gmail:

```json
"FILTER": {
    "TIME_RANGE": null,
    "INCLUDE_LABEL": null,
    "INCLUDE_SENDERS": null
}
```

| Field | Description |
|-------|-------------|
| **TIME_RANGE** | `"7d"` / `"30d"` / `"1m"` / `null`. `null` = no limit |
| **INCLUDE_LABEL** | Only fetch emails with this label, e.g. `"important"` |
| **INCLUDE_SENDERS** | Only fetch emails from these senders |

## Dashboard Filters (Display Stage)

**Exclude** filters (promotions, social, updates, keywords) are in the Dashboard header. Use the UI to filter:

- **Date**: All / 7 days / 30 days
- **Exclude**: Check "Promotions", "Social", "Updates", "Keywords" to filter in real time

No config changes or re-run needed.
