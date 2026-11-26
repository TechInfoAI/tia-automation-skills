#!/usr/bin/env python3
"""Explain a 5-field cron expression and list its next run times.

Usage:
    python3 cron_check.py "0 9 * * 1-5" [--tz Asia/Dhaka] [--next 5] [--json]

Fields: minute hour day-of-month month day-of-week.
Supports *, lists (1,15), ranges (1-5), steps (*/15, 0-30/10), month names
(JAN-DEC), weekday names (SUN-SAT) and 7 as Sunday. Like standard cron, when
both day-of-month and day-of-week are restricted, a time matches if EITHER does.

Standard library only. Python 3.9+ (uses zoneinfo for time zones).
"""
import json
import sys
from datetime import datetime, timedelta

try:
    from zoneinfo import ZoneInfo
except ImportError:  # Python < 3.9
    ZoneInfo = None

MONTHS = {m: i for i, m in enumerate(["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"], 1)}
DAYS = {d: i for i, d in enumerate(["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"])}
DAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August",
               "September", "October", "November", "December"]
FIELDS = [("minute", 0, 59, {}), ("hour", 0, 23, {}), ("day-of-month", 1, 31, {}),
          ("month", 1, 12, MONTHS), ("day-of-week", 0, 7, DAYS)]
ALIASES = {"@yearly": "0 0 1 1 *", "@annually": "0 0 1 1 *", "@monthly": "0 0 1 * *",
           "@weekly": "0 0 * * 0", "@daily": "0 0 * * *", "@midnight": "0 0 * * *", "@hourly": "0 * * * *"}


class CronError(ValueError):
    pass


def parse_value(tok, names, lo, hi, field):
    t = tok.upper()
    if t in names:
        return names[t]
    if not t.isdigit():
        raise CronError(f"'{tok}' is not a valid value for {field}")
    v = int(t)
    if not lo <= v <= hi:
        raise CronError(f"{v} is out of range for {field} ({lo}-{hi})")
    return v


def parse_field(text, field, lo, hi, names):
    values = set()
    for part in text.split(","):
        if not part:
            raise CronError(f"empty list item in {field}")
        step = 1
        if "/" in part:
            part, s = part.split("/", 1)
            if not s.isdigit() or int(s) == 0:
                raise CronError(f"bad step '/{s}' in {field}")
            step = int(s)
        if part == "*":
            start, end = lo, hi
        elif "-" in part:
            a, b = part.split("-", 1)
            start, end = parse_value(a, names, lo, hi, field), parse_value(b, names, lo, hi, field)
            if start > end:
                raise CronError(f"range {a}-{b} runs backwards in {field}")
        else:
            start = parse_value(part, names, lo, hi, field)
            end = hi if step > 1 else start
        values.update(range(start, end + 1, step))
    return values


def parse(expr):
    expr = ALIASES.get(expr.strip().lower(), expr.strip())
    parts = expr.split()
    if len(parts) != 5:
        raise CronError(f"expected 5 fields (minute hour day-of-month month day-of-week), got {len(parts)}. "
                        "If your tool uses a 6-field cron with seconds, drop the first field to check it here.")
    sets = {}
    for (field, lo, hi, names), text in zip(FIELDS, parts):
        sets[field] = parse_field(text, field, lo, hi, names)
    if 7 in sets["day-of-week"]:
        sets["day-of-week"].discard(7)
        sets["day-of-week"].add(0)
    sets["_dom_star"] = parts[2] == "*"
    sets["_dow_star"] = parts[4] == "*"
    sets["_expr"] = expr
    return sets


def matches(s, dt):
    if dt.minute not in s["minute"] or dt.hour not in s["hour"] or dt.month not in s["month"]:
        return False
    dom_ok = dt.day in s["day-of-month"]
    dow_ok = (dt.isoweekday() % 7) in s["day-of-week"]
    if s["_dom_star"] and s["_dow_star"]:
        return True
    if s["_dom_star"]:
        return dow_ok
    if s["_dow_star"]:
        return dom_ok
    return dom_ok or dow_ok


def next_runs(s, start, count, tz):
    runs = []
    dt = start.replace(second=0, microsecond=0) + timedelta(minutes=1)
    limit = dt + timedelta(days=366 * 4)
    while len(runs) < count and dt < limit:
        if dt.month not in s["month"]:
            # jump to the first day of next month
            dt = (dt.replace(day=1, hour=0, minute=0) + timedelta(days=32)).replace(day=1)
            continue
        if dt.hour not in s["hour"]:
            dt = dt.replace(minute=0) + timedelta(hours=1)
            continue
        if matches(s, dt):
            local = dt.replace(tzinfo=tz) if tz else dt
            runs.append(local)
        dt += timedelta(minutes=1)
    return runs


def join_words(items):
    items = list(items)
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def describe_set(values, lo, hi, label_fn=str):
    vals = sorted(values)
    if vals == list(range(lo, hi + 1)):
        return None
    if len(vals) > 2:
        diffs = {b - a for a, b in zip(vals, vals[1:])}
        if len(diffs) == 1:
            d = diffs.pop()
            if d == 1:
                return f"{label_fn(vals[0])} to {label_fn(vals[-1])}"
            return f"every {d} from {label_fn(vals[0])} to {label_fn(vals[-1])}"
    return join_words(label_fn(v) for v in vals)


def describe(s):
    mins, hours = sorted(s["minute"]), sorted(s["hour"])
    step_from_zero = (len(mins) > 1 and mins[0] == 0 and len({b - a for a, b in zip(mins, mins[1:])}) == 1
                      and 60 % (mins[1] - mins[0]) == 0 and mins[-1] + (mins[1] - mins[0]) == 60)
    h = describe_set(s["hour"], 0, 23, lambda v: f"{v:02d}:00")
    if len(mins) == 1 and len(hours) <= 4:
        time_part = "at " + join_words(f"{hh:02d}:{mins[0]:02d}" for hh in hours)
    elif len(mins) == 1:
        time_part = f"at minute {mins[0]} of every hour" + (f" from {h}" if h and " to " in h else (f" in hours {h}" if h else ""))
    elif step_from_zero or len(mins) == 60:
        time_part = "every minute" if len(mins) == 60 else f"every {mins[1] - mins[0]} minutes"
        if h is not None:
            time_part += f" during hours {h}"
    else:
        m = describe_set(s["minute"], 0, 59)
        time_part = "every minute" if m is None else f"at minute {m}"
        if h is not None:
            time_part += f", during hours {h}"
    day_bits = []
    dom = describe_set(s["day-of-month"], 1, 31)
    dow = describe_set(s["day-of-week"], 0, 6, lambda v: DAY_NAMES[v])
    if dom and dow:
        day_bits.append(f"on day {dom} of the month or on {dow}")
    elif dom:
        day_bits.append(f"on day {dom} of the month")
    elif dow:
        day_bits.append(f"on {dow}")
    mon = describe_set(s["month"], 1, 12, lambda v: MONTH_NAMES[v - 1])
    if mon:
        day_bits.append(f"in {mon}")
    return " ".join([time_part] + day_bits) if day_bits else time_part + ", every day"


def main(argv):
    args = argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if args else 2
    expr = args[0]
    tz_name, count, as_json = None, 5, False
    i = 1
    while i < len(args):
        if args[i] == "--tz" and i + 1 < len(args):
            tz_name = args[i + 1]
            i += 2
        elif args[i] == "--next" and i + 1 < len(args):
            count = max(1, min(50, int(args[i + 1])))
            i += 2
        elif args[i] == "--json":
            as_json = True
            i += 1
        else:
            print(f"Unknown option: {args[i]}", file=sys.stderr)
            return 2
    tz = None
    if tz_name:
        if ZoneInfo is None:
            print("--tz needs Python 3.9+ (zoneinfo).", file=sys.stderr)
            return 2
        try:
            tz = ZoneInfo(tz_name)
        except Exception:
            print(f"Unknown time zone: {tz_name}", file=sys.stderr)
            return 2
    try:
        s = parse(expr)
    except CronError as e:
        print(f"Invalid cron: {e}", file=sys.stderr)
        return 1
    now = datetime.now(tz).replace(tzinfo=None) if tz else datetime.now()
    runs = next_runs(s, now, count, tz)
    text = describe(s)
    zone = tz_name or "server local time"
    if as_json:
        print(json.dumps({"expression": s["_expr"], "description": text, "timezone": zone,
                          "next_runs": [r.isoformat() for r in runs]}, indent=2))
    else:
        print(f"Cron: {s['_expr']}")
        print(f"Means: runs {text} ({zone}).")
        print(f"Next {len(runs)} runs:")
        for r in runs:
            print("  " + r.strftime("%a %Y-%m-%d %H:%M"))
        if not runs:
            print("  none found in the next 4 years (check day-of-month and month, e.g. 31 in February)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
