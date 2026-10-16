import os
from mcstatus import JavaServer

INPUT_FILE = "server.txt"
OUTPUT_FILE = "ping.txt"
TIMEOUT = 5

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"'{INPUT_FILE}' not found!")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        servers = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    results = []
    for addr in servers:
        try:
            server = JavaServer.lookup(addr, timeout=TIMEOUT)
            status = server.status()
            online = status.players.online
            maxp = status.players.max
            motd = status.description
            # MOTD ممکنه dict باشه (برای سرورهای جدید)
            if isinstance(motd, dict):
                motd = motd.get("text", "") or str(motd)
            motd = str(motd).replace("\n", " ").strip()
            results.append(f"{addr} - Online - {online}/{maxp} players - \"{motd}\"")
            print(f"[OK] {addr} -> {online}/{maxp}")
        except Exception as e:
            results.append(f"{addr} - Offline")
            print(f"[FAIL] {addr} -> {e}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(results) + "\n")

    print(f"\nSaved {len(results)} results to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
