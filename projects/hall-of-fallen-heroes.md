# Project: Hall of Fallen Heroes

**Status:** ✅ Completed

---

## Objective

World of Warcraft has a mechanic where you can see the gravestones of other players where they died inside Delves. In my guild, whenever someone died in a particularly embarrassing or memorable way, we'd take a screenshot and share it in Discord. It worked, but it was messy, screenshots scattered across chat, no overview, no history.

The goal was to build something better: a self-hosted memorial wall where guild members can upload their death screenshots and have them displayed in a proper hall of fame. Complete with gear snapshots showing exactly what they were wearing when they died, Blizzard-verified character data, and a shared overview everyone in the guild can browse.

Beyond building the application, the project included a full security investigation after deployment, identifying and remediating a critical vulnerability, and completing a 13-point security audit against the live public application.

---

## Environment

| Component | Detail |
|---|---|
| Hosting | Docker container on Ubuntu 22.04 VM (Proxmox) |
| Container Management | Portainer |
| Reverse Proxy | Nginx Proxy Manager |
| CDN / DNS | Cloudflare |
| Public URL | memoria.irosec.com |
| Database | SQLite via better-sqlite3 |
| Runtime | Node.js / Express |
| OCR | Tesseract.js |
| External API | Blizzard Profile API (OAuth client credentials) |

---

## Steps

**1. Designed the application architecture** — Planned a server-side Node.js application with SQLite for persistence, Tesseract.js for screenshot OCR, and Blizzard's OAuth API for character data verification.

**2. Built the upload pipeline** — Created a multi-file batch upload queue with per-file delve picker, screenshot preview with zoom-on-hover, and server-side password authentication via a `/auth/upload` endpoint. Upload credentials stored in environment variables, never in client-side source.

**3. Implemented OCR with error correction** — Integrated Tesseract.js to extract character names and death details from in-game screenshots. Built a custom `fixOcrText()` correction layer to handle common OCR misreads from WoW's in-game font, including realm-aware name splitting for hyphenated realm names like `Epicozmonk-Skullcrusher`.

**4. Integrated Blizzard API** — Connected to the Blizzard Profile API using OAuth client credentials to fetch verified character data, gear snapshots, and avatars. Implemented server-side avatar caching and localStorage portrait caching with a 7-day TTL to reduce repeat API calls.

**5. Built gear snapshot storage** — Gear is captured and stored as JSON in the database at upload time via a `gear_snapshot` column, served via a `/hall/:id/gear` endpoint. This eliminates repeat Blizzard API calls on every page load and preserves the exact gear state at time of death.

**6. Added Wowhead integration** — Integrated Wowhead native item tooltips via `data-wowhead` attributes so item icons in gear snapshots display rich tooltips on hover, matching the standard WoW community experience.

**7. Deployed to homelab infrastructure** — Containerised the application using Docker Compose following established irosec patterns: configs and databases stored on the mainraid mount, media on the UNAS Pro NFS share. Environment variables managed via Portainer's UI env loader. Exposed publicly via Nginx Proxy Manager with SSL termination through Cloudflare.

**8. Added admin functionality** — Implemented admin-only delete functionality for moderation, with sensitive operations protected behind server-side authentication separate from the upload password.

![Homepage](http://img.irosec.com/u/VzyZig.png)
![Image Upload](http://img.irosec.com/u/mgxj9h.png)
![Equipment](http://img.irosec.com/u/gnKyRC.png)

---

## Security Investigation & Hardening

Once the application was stable and being used by the guild, the decision was made to add it to the irosec portfolio and document it on the wiki. Before doing that, a proper security review was conducted — because pointing recruiters at a publicly exposed application with known vulnerabilities would be worse than not sharing it at all.

The review immediately identified a critical issue.

### Vulnerability — Password Exposed in Client-Side Source

**Severity:** High
**Type:** Sensitive Data Exposure / Broken Authentication

The initial implementation stored the upload password as a hardcoded constant directly in the frontend JavaScript:

```javascript
const UPLOAD_PW = 'password123'; // example — actual value redacted
```

Any visitor could read the full password in plain text via `Ctrl+U` (view source) or browser DevTools — no hacking required. The upload endpoint was effectively unprotected.

### Fix Applied

Authentication was moved entirely server-side:

- **Removed the password from client-side source** — JS no longer contains any password value
- **Server-side validation on `/analyze`** — password sent as `X-Upload-Password` header, validated against an environment variable:

```javascript
const uploadPw = req.headers["x-upload-password"] || "";
if (uploadPw !== UPLOAD_PASSWORD) {
  return res.status(401).json({ error: "unauthorized" });
}
```

- **Password stored as environment variable** — in a `.env` file with `chmod 600` permissions, loaded via Portainer's environment variable UI. Never appears in any source file.
- **Admin-only delete** — delete buttons removed from the public site entirely, only accessible via `/admin` with a separate admin password stored as its own environment variable.

### Before vs After

| Aspect | Before | After |
|---|---|---|
| Password location | Hardcoded in JS source — public | Environment variable — server only |
| Password visibility | Anyone with `Ctrl+U` | Nobody — never leaves the server |
| Upload auth | Client-side string compare | Server-side header validation |
| Delete access | Any upload user | Admin endpoint only |
| Password rotation | Requires code change + redeploy | Change env var, restart container |

---

### Full Security Audit — 29 March 2026

With the critical vulnerability patched, a full 13-point security audit was run against the live application before adding it to the portfolio. The goal was to verify the application was hardened to a standard appropriate for a publicly accessible self-hosted service.

The audit covered authentication, rate limiting, injection protection, security headers, SSRF, and sensitive data exposure.

**The first audit run did not pass.** Several gaps were identified that required dedicated fixes before the application was considered portfolio-ready.

### Fixes Applied After First Audit

| Fix | Details |
|---|---|
| Rate limiting | `/auth/upload` max 10/min per IP, `/analyze` max 20/min per IP |
| File size limit | 25MB max per upload, rejects oversized files before OCR processing |
| SSRF protection | `/proxy/image-url` blocks private IPs (192.168.x.x, 10.x.x.x, 169.254.x.x, localhost) |
| Auth on DELETE | `/hall/:id` now requires upload or admin password |
| Auth on setcreds | `/blizzard/setcreds` now requires admin password |
| Security headers | Added X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Referrer-Policy |
| Info disclosure | Removed `_source` field from gear API responses |

After applying all fixes the audit was re-run. **All 13 checks passed on the second run.**

| Check | Result | Details |
|---|---|---|
| Rate limiting `/auth/upload` | ✅ | 429 after 10 attempts/min per IP |
| Rate limiting `/analyze` | ✅ | 429 after 20 uploads/min per IP |
| Auth on `DELETE /hall/:id` | ✅ | 401 without password |
| Auth on `/blizzard/setcreds` | ✅ | 401 without admin password |
| SSRF protection | ✅ | 400 on private/internal IPs |
| `X-Content-Type-Options` | ✅ | nosniff |
| `X-Frame-Options` | ✅ | SAMEORIGIN |
| `X-XSS-Protection` | ✅ | 1; mode=block |
| `Referrer-Policy` | ✅ | strict-origin-when-cross-origin |
| SQL injection | ✅ | Parameterized queries throughout |
| File size limit | ✅ | 25MB max |
| Password in JS source | ✅ | Not present |
| Sensitive info disclosure | ✅ | `_source` field removed from API |

**Audit conclusion:** The site is well-hardened for a public homelab project. The main remaining risk noted was the Cloudflare layer — Always Use HTTPS and SSL/TLS mode set to Full (strict) ensures password headers are encrypted in transit.

---

## Results

- Fully functional public web application live at memoria.irosec.com
- Complete upload pipeline with OCR, Blizzard API verification, and gear snapshot capture
- Self-hosted end-to-end — database, media storage, and application all on homelab infrastructure
- Critical authentication vulnerability identified, investigated, and fully remediated
- 13-point security audit completed with all checks passing
- Demonstrates full-stack development, API integration, OCR processing, Docker deployment, and applied security engineering in a single project

---

## Lessons Learned

Environment variable handling in Portainer requires a different approach than standard Docker Compose — since Portainer runs in its own container it cannot access host filesystem paths for `env_file` references. The reliable pattern is loading variables directly through Portainer's UI.

The OCR correction layer required iterative tuning based on real screenshot submissions. WoW's in-game font produces consistent misreads that can be anticipated and corrected, but this only becomes clear once real data flows through the system, OCR pipelines always need a feedback loop built in from the start.

Storing gear snapshots at upload time rather than fetching on demand was the right architectural decision. Blizzard's API has rate limits and gear changes over time — a snapshot preserves the exact state at the moment of death, which is both more accurate and more meaningful for a memorial application.

The security investigation reinforced a core principle: **client-side code is always public**. Any secret stored in JavaScript source is not a secret. Authentication logic must always live on the server. Conducting a structured security audit before sharing an application publicly — even a personal project — is a habit worth keeping.
