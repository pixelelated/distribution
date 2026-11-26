"""Single host and guest time budget for the isolated #1433 ordinary exit."""

NS = 10**9
MAX_KEYS = 5
REVIEW = 40
APPROVAL_ARRIVAL = 2
SHOT = 2
GUARD_AFTER_FRAME = 3
KEY = 6
RETIRE_MARGIN = 5
# Review arrival and inter-key guard each get two seconds in the plan.
PER_ACTION = 2*SHOT + REVIEW + APPROVAL_ARRIVAL + GUARD_AFTER_FRAME + KEY + 2
FIRST_GUARD = 50
MENU = 360
APPROVAL_RESERVE = SHOT + GUARD_AFTER_FRAME + KEY + RETIRE_MARGIN
ARM_SETUP = 245
STARTUP = 55
POST_EXIT = 125
DETACH = 10
OBSERVER = STARTUP + MENU + POST_EXIT + DETACH
EDGE_DRAIN = 2
GUEST_RETURN = 35
SERIAL_RESERVE = 20
ARM_SERIAL = ARM_SETUP + STARTUP + MENU + POST_EXIT + GUEST_RETURN + SERIAL_RESERVE
ARCHIVE = 260
PREFLIGHT = 170
STAGING = 45
BOOT_RESERVE = 190
WITNESS_STAGE = 16
WORKER_MAX = 1625
RETIREMENT_FROM_SLOT_END = 160
ARM_AND_ARCHIVE = ARM_SERIAL + ARCHIVE
WORK = STAGING + PREFLIGHT + ARM_AND_ARCHIVE

GUARD_INTERVAL = 1
GUARD_ROWS = MENU // GUARD_INTERVAL + 1
GUARD_LINE = 2048  # includes the prefix and line ending
SERIAL_CAP = 900*1024  # host worker inherits a 1 MiB regular-file limit


def guest_window(arm_start, observer_start, menu_start):
    if not (arm_start <= observer_start <= arm_start + ARM_SETUP*NS and
            observer_start <= menu_start <= observer_start + STARTUP*NS):
        raise ValueError("armed setup or emulator readiness exceeded its reserved budget")
    end = menu_start + MENU*NS
    return {
        "arm_start_ns": arm_start, "observer_start_ns": observer_start,
        "menu_start_ns": menu_start, "menu_until_ns": end,
        "edge_until_ns": end + EDGE_DRAIN*NS,
        "archive_until_ns": end + POST_EXIT*NS,
        "observer_until_ns": observer_start + OBSERVER*NS,
    }


def validate_window(row):
    expected = guest_window(row["arm_start_ns"], row["observer_start_ns"], row["menu_start_ns"])
    if any(row[key] != value for key,value in expected.items()):
        raise ValueError("guest menu window differs from the shared budget")


def after_exit(window, retired):
    if not window["menu_start_ns"] <= retired < window["menu_until_ns"]:
        raise ValueError("actual emulator retirement outside the visible-menu deadline")
    return retired + POST_EXIT*NS


def approval_cutoff(issued, guest_menu_end_on_host):
    return min(issued+REVIEW*NS, guest_menu_end_on_host-(APPROVAL_RESERVE+APPROVAL_ARRIVAL)*NS)


def arm_cutoff(now, work_deadline):
    end = now+ARM_SERIAL
    if end+ARCHIVE > work_deadline:
        raise ValueError("independent export budget unavailable before arming")
    return end

def work_remaining(now, worker_start, activation_deadline):
    return min(WORKER_MAX-(now-worker_start), activation_deadline-now-RETIREMENT_FROM_SLOT_END)
