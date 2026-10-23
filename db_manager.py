class DatabaseManager:
    def __init__(self):
        self.use_live_oracle = False
        self.conn = None
        self.history = []  # Local cache for UI Leaderboard display

       
import oracledb

class DatabaseManager:
    def __init__(self):
        self.use_live_oracle = False
        self.conn = None
        self.history = []

        try:
            # Replace 'your_password' with the password you set during installation
            # If you connected via SID 'xe', use 'localhost:1521/xe'
            # If you connected via Service Name 'XEPDB1', use 'localhost:1521/XEPDB1'
            self.conn = oracledb.connect(
                user="system",
                password="Pankaj@9097",
                dsn="localhost:1521/xe"
            )
            self.use_live_oracle = True
            print("[SUCCESS] Live connection to Oracle Database established.")
        except Exception as e:
            print(f"[INFO] Using PL/SQL Simulation Mode: {e}")

    def log_session(self, player_name, maze_size, steps, solve_time_ms):
        if self.use_live_oracle and self.conn:
            cursor = self.conn.cursor()
            eff_score = cursor.var(float)
            status = cursor.var(str)
            cursor.callproc("record_maze_run", [player_name, maze_size, steps, solve_time_ms, eff_score, status])
            score_val = eff_score.getvalue()
            cursor.close()
        else:
            # Mirrors the exact PL/SQL calc_efficiency formula for offline demos
            score_val = round(10000 / ((steps * 1.5) + (solve_time_ms * 10) + 1), 2)
            print(f"[PL/SQL EXEC] CALL record_maze_run('{player_name}', '{maze_size}', {steps}, {solve_time_ms:.3f}, :score, :status);")

        record = {
            "player": player_name,
            "size": maze_size,
            "steps": steps,
            "time_ms": round(solve_time_ms, 3),
            "score": score_val
        }
        self.history.append(record)
        self.history.sort(key=lambda x: x["score"], reverse=True)
        return record