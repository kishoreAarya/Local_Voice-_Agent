import json
import sqlite3
import time

DB_PATH = "agent_state.db"


def _conn():
    return sqlite3.connect(DB_PATH)


def init():
    with _conn() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS sessions(
            id INTEGER PRIMARY KEY, started REAL);
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY, session_id INTEGER, ts REAL,
            role TEXT, content TEXT);
        CREATE TABLE IF NOT EXISTS action_logs(
            id INTEGER PRIMARY KEY, session_id INTEGER, ts REAL,
            tool TEXT, params TEXT, result TEXT, ok INTEGER);
        CREATE TABLE IF NOT EXISTS calendar(
            id INTEGER PRIMARY KEY, ts REAL, title TEXT, datetime TEXT);
        """)


def new_session() -> int:
    with _conn() as c:
        return c.execute("INSERT INTO sessions(started) VALUES(?)",
                         (time.time(),)).lastrowid


def log_message(session_id, role, content):
    with _conn() as c:
        c.execute("INSERT INTO messages(session_id,ts,role,content) VALUES(?,?,?,?)",
                  (session_id, time.time(), role, content))


def log_action(session_id, tool, params, result, ok):
    with _conn() as c:
        c.execute("INSERT INTO action_logs(session_id,ts,tool,params,result,ok) "
                  "VALUES(?,?,?,?,?,?)",
                  (session_id, time.time(), tool, json.dumps(params),
                   str(result), int(ok)))


def add_event(title, dt):
    with _conn() as c:
        c.execute("INSERT INTO calendar(ts,title,datetime) VALUES(?,?,?)",
                  (time.time(), title, dt))
