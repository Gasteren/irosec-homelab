# 🎓 Lessons Learned

This page documents mistakes, unexpected issues, and things that didn't go as planned in the irosec homelab — along with how they were resolved.

This section is intentionally honest. Real engineers break things. Documenting the process of diagnosing and fixing problems is often more valuable than documenting things that worked first time.

---

## 📚 Log

| Date | What Happened | Root Cause | Resolution |
|---|---|---|---|
| Mar 2026 | Wiki.js documentation site needed to be publicly accessible with a proper domain and SSL | Running on a bare IP and port with no HTTPS made it unsuitable for sharing with recruiters or LinkedIn | Deployed Nginx Proxy Manager as a reverse proxy, configured Let's Encrypt SSL via DNS challenge, pointed wiki.irosec.com at the container |
| Dec 2025 | IDS/IPS was generating false positives on legitimate game traffic | Online Games signature in the Protocol Vulnerabilities category flagged normal gaming traffic as suspicious | Disabled the Online Games rule specifically, keeping all 11 remaining Protocol Vulnerability rules active — detection coverage maintained for all non-gaming traffic. See [full write-up](https://wiki.irosec.com/en/lessons-learned/World_of_Warcraft_In-Game_Voice_Chat_Blocked_by_IDS_IPS)|
| Ongoing | IDS/IPS alerts exist only in the Unifi controller with no external log correlation | No SIEM deployed yet to aggregate logs from the DMP, Nginx Proxy Manager, Vaultwarden, and other services | Known gap — Wazuh deployment planned to centralise log collection and enable cross-service correlation |

---

## 🔓 Known Gaps & Open Items

These are known security or architectural weaknesses in the current setup that are actively being worked on:

**Unifi IDS logs are not forwarded to a SIEM** — Currently all IDS/IPS alerts live only in the Unifi controller and are not correlated with logs from other sources. A compromised device on the network could generate alerts that go unnoticed without active monitoring of the Unifi dashboard. Wazuh deployment will address this.

**No centralised log management** — Each service (Nginx Proxy Manager, Plex, Wiki.js, Vaultwarden etc.) generates its own logs with no aggregation. There is currently no way to correlate events across services — for example, matching a failed Vaultwarden login with a suspicious source IP seen in the Nginx access log. Wazuh with agent-based log collection is the planned solution.

## ✍ Write-ups

About | Link |
|---|---|---|---|
| IDS/IPS was generating false positives on legitimate game traffic | [Full write-up](https://wiki.irosec.com/en/lessons-learned/World_of_Warcraft_In-Game_Voice_Chat_Blocked_by_IDS_IPS)

---

*The best homelabs are the ones that break regularly — because that's where the real learning happens.*
