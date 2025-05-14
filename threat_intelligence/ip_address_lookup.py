import sys
import socket
import requests
import json

ABUSEIPDB_API_KEY = "YOUR_API_KEY"  # Replace this with your real API key
ABUSEIPDB_API_URL = "https://api.abuseipdb.com/api/v2/check"

def is_valid_ip(ip: str) -> bool:
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def lookup_ip(ip: str, max_age_days: int = 30) -> dict:
    headers = {
        "Key": ABUSEIPDB_API_KEY,
        "Accept": "application/json"
    }
    try:
        response = requests.get(
            ABUSEIPDB_API_URL,
            headers=headers,
            params={"ipAddress": ip, "maxAgeInDays": max_age_days}
        )
        response.raise_for_status()
        data = response.json()["data"]

        return {
            "ip": data["ipAddress"],
            "abuse_score": data["abuseConfidenceScore"],
            "country": data.get("countryCode", "N/A"),
            "isp": data.get("isp", "N/A"),
            "domain": data.get("domain", "N/A"),
            "total_reports": data["totalReports"],
            "last_reported_at": data.get("lastReportedAt", "Never"),
            "whitelisted": data["isWhitelisted"]
        }
    except requests.RequestException as e:
        return {"ip": ip, "error": str(e)}

def main():
    ips = sys.argv[1:]
    if not ips:
        print("Usage: python threatintel.py <IP1> <IP2> ...")
        sys.exit(1)

    for ip in ips:
        if not is_valid_ip(ip):
            print(f"[!] Invalid IP address: {ip}")
            continue

        result = lookup_ip(ip)
        print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()
