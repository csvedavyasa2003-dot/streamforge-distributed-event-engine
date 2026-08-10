"""
state_store.py

So here's the idea behind this file.

Every time a truck sends a temperature reading, your consumer hands it
off to record_reading() down below. That function tucks it away into
a little database file (truck_state.db) that gets created automatically
the first time you run this. Think of it like a notebook where every
reading gets written down with a timestamp.

Later, whenever anyone needs to ask "hey, what's truck 1001's average
temperature been over the last 5 minutes?" - they just call one of the
functions here and get an answer, without you having to keep everything
in memory yourself.

Why SQLite? Because it's just one file, nothing to install or configure,
and Python already knows how to talk to it out of the box. No servers,
no passwords, no setup headaches.

You really only need to touch three functions from your consumer code:
record_reading(), get_rolling_average(), and get_active_alerts(). The
rest is just the wiring that makes those work.
"""

import sqlite3
import time
from pathlib import Path


# ---------------------------------------------------------------------
# A few knobs you can turn if the team decides on different numbers
# ---------------------------------------------------------------------

# This is where the database file will live - same folder as this script.
DB_PATH = Path(__file__).parent / "truck_state.db"

# We only care about the last 5 minutes of data per truck (300 seconds).
# Anything older just gets cleaned out automatically.
WINDOW_SECONDS = 300

# Cross this temperature and it counts as an alert. Double check this
# number with the team before the demo - 35 was just a starting guess.
ALERT_THRESHOLD = 35.0

# If 30 seconds go by with no new reading, we start wondering if the
# consumer crashed. Used for the worker health check.
HEARTBEAT_TIMEOUT_SECONDS = 30


# ---------------------------------------------------------------------
# Opening a connection to the database
# ---------------------------------------------------------------------
def get_connection():
    """
    Just opens the database file so we can read from or write to it -
    basically the "unlock the notebook" step before anything else.
    """
    connection = sqlite3.connect(DB_PATH, timeout=5)

    # This line is what lets your consumer write new readings at the
    # same time someone else (like Aravind's API) is reading from it,
    # without the two stepping on each other's toes.
    connection.execute("PRAGMA journal_mode=WAL;")

    return connection


# ---------------------------------------------------------------------
# Setting up the database the first time (safe to run every time -
# it won't erase anything that's already there)
# ---------------------------------------------------------------------
def init_db():
    """
    Gets two tables ready:

    1. "readings" - every single event we've received, one row each
    2. "worker_heartbeat" - one row that just tracks "am I still alive,
       and when did I last do something"
    """
    connection = get_connection()

    # Where every temperature reading actually gets stored
    connection.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            truck_id TEXT,
            temperature REAL,
            timestamp REAL
        )
    """)

    # This just makes lookups faster later on - not something you need
    # to worry about, it's a behind-the-scenes optimization
    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_truck_ts ON readings(truck_id, timestamp)
    """)

    # A single row that tracks whether the consumer is still running
    connection.execute("""
        CREATE TABLE IF NOT EXISTS worker_heartbeat (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            last_seen REAL,
            total_events INTEGER
        )
    """)

    # Make sure that heartbeat row actually exists (starts at zero
    # the very first time this runs)
    connection.execute("""
        INSERT OR IGNORE INTO worker_heartbeat (id, last_seen, total_events)
        VALUES (1, 0, 0)
    """)

    connection.commit()
    connection.close()


# ---------------------------------------------------------------------
# Saving a new reading - call this once per event
# ---------------------------------------------------------------------
def record_reading(truck_id, temperature, timestamp=None):
    """
    Drop this into your consumer's loop, right after you've parsed a
    new event off Kafka.

    Example:
        state_store.record_reading("1001", 32.5)
    """
    # If nobody passed in a timestamp, just use right now
    if timestamp is None:
        timestamp = time.time()

    connection = get_connection()

    # Write the reading down
    connection.execute(
        "INSERT INTO readings (truck_id, temperature, timestamp) VALUES (?, ?, ?)",
        (truck_id, temperature, timestamp)
    )

    # Let the heartbeat know we're still alive and kicking
    connection.execute(
        "UPDATE worker_heartbeat SET last_seen = ?, total_events = total_events + 1 WHERE id = 1",
        (time.time(),)
    )

    # Housekeeping: clear out anything older than our 5-minute window
    # for this truck, so the file doesn't just keep growing forever
    oldest_allowed_time = timestamp - WINDOW_SECONDS
    connection.execute(
        "DELETE FROM readings WHERE truck_id = ? AND timestamp < ?",
        (truck_id, oldest_allowed_time)
    )

    connection.commit()
    connection.close()


# ---------------------------------------------------------------------
# Asking questions about the data - these just read, nothing changes
# ---------------------------------------------------------------------

def get_rolling_average(truck_id):
    """
    What's this one truck's average temperature been over the last
    5 minutes? Comes back as None if we don't have any recent data yet.
    """
    cutoff_time = time.time() - WINDOW_SECONDS

    connection = get_connection()
    result = connection.execute(
        "SELECT AVG(temperature) FROM readings WHERE truck_id = ? AND timestamp >= ?",
        (truck_id, cutoff_time)
    ).fetchone()
    connection.close()

    average_temperature = result[0]  # None if nothing recent came in
    return average_temperature


def get_all_rolling_averages():
    """
    Same idea, but for every truck at once. Comes back as a dictionary,
    something like {"1001": 28.4, "1002": 31.1, ...}
    """
    cutoff_time = time.time() - WINDOW_SECONDS

    connection = get_connection()
    rows = connection.execute(
        "SELECT truck_id, AVG(temperature) FROM readings WHERE timestamp >= ? GROUP BY truck_id",
        (cutoff_time,)
    ).fetchall()
    connection.close()

    # Just reshaping the rows into a dictionary so it's easier to use
    averages_by_truck = {}
    for truck_id, average_temperature in rows:
        averages_by_truck[truck_id] = average_temperature

    return averages_by_truck


def get_highest_lowest(truck_id):
    """
    Highest and lowest temps for one truck in the last 5 minutes.
    Comes back like: {"highest": 38.2, "lowest": 22.1}
    """
    cutoff_time = time.time() - WINDOW_SECONDS

    connection = get_connection()
    result = connection.execute(
        "SELECT MAX(temperature), MIN(temperature) FROM readings WHERE truck_id = ? AND timestamp >= ?",
        (truck_id, cutoff_time)
    ).fetchone()
    connection.close()

    highest, lowest = result
    return {"highest": highest, "lowest": lowest}


def get_worker_status():
    """
    Basically a health check - is the consumer still running, or has
    it gone quiet for too long?
    """
    connection = get_connection()
    result = connection.execute(
        "SELECT last_seen, total_events FROM worker_heartbeat WHERE id = 1"
    ).fetchone()
    connection.close()

    last_seen, total_events = result

    # Hasn't processed a single event yet
    if not last_seen:
        return {"status": "unknown", "last_seen": None, "total_events": 0}

    seconds_since_last_event = time.time() - last_seen

    if seconds_since_last_event <= HEARTBEAT_TIMEOUT_SECONDS:
        status = "healthy"
    else:
        status = "stale"  # been quiet too long - might have crashed

    return {
        "status": status,
        "last_seen": last_seen,
        "seconds_since_heartbeat": round(seconds_since_last_event, 2),
        "total_events": total_events,
    }


def get_active_alerts():
    """
    Which trucks are currently running hot? Looks at each truck's most
    recent reading and flags the ones over threshold. Comes back as a
    list like:
    [{"truck_id": "1001", "temperature": 38.2, "threshold": 35.0, "timestamp": ...}, ...]
    """
    cutoff_time = time.time() - WINDOW_SECONDS

    connection = get_connection()

    # For each truck, grab its most recent reading, then keep only the
    # ones where that reading is over the threshold
    rows = connection.execute("""
        SELECT r.truck_id, r.temperature, r.timestamp
        FROM readings r
        INNER JOIN (
            SELECT truck_id, MAX(timestamp) AS most_recent_time
            FROM readings
            WHERE timestamp >= ?
            GROUP BY truck_id
        ) latest
        ON r.truck_id = latest.truck_id AND r.timestamp = latest.most_recent_time
        WHERE r.temperature > ?
    """, (cutoff_time, ALERT_THRESHOLD)).fetchall()

    connection.close()

    alerts = []
    for truck_id, temperature, timestamp in rows:
        alerts.append({
            "truck_id": truck_id,
            "temperature": temperature,
            "threshold": ALERT_THRESHOLD,
            "timestamp": timestamp,
        })

    return alerts


# ---------------------------------------------------------------------
# Runs automatically the moment this file gets imported, so the
# database is always ready before anything tries to use it
# ---------------------------------------------------------------------
init_db()
