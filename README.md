# irosec Starlight wiki

Static portfolio/documentation site replacing Wiki.js, built with
[Astro Starlight](https://starlight.astro.build).

## Local dev

```bash
npm install
npm run dev
```

Serves at http://localhost:4321 by default.

## Migrating content from Wiki.js

1. Export Wiki.js pages to Markdown:
   - Admin panel: Admin -> Utilities -> Export, or
   - `wikijs-cli export ./wikijs-export`
2. Run the migration script to inject Starlight frontmatter and strip
   duplicate H1s:

   ```bash
   python3 migrate.py ./wikijs-export ./src/content/docs
   ```

3. Review the output for Wiki.js-specific shortcodes/admonitions - these
   don't auto-convert. Starlight's equivalent is:

   ```md
   :::note
   Some note text.
   :::

   :::caution
   Some warning text.
   :::

   :::danger
   Some critical warning.
   :::
   ```

4. Update the `sidebar` section in `astro.config.mjs` to match your actual
   top-level folders (or leave `autogenerate` pointed at the right
   directories - it builds the nav from the folder tree automatically).
5. Delete or repurpose `src/content/docs/index.md` and
   `src/content/docs/guides/example.md` once real content is in place.

## Build & run with Docker

```bash
docker compose build
docker compose up -d
```

Site is served on host port 8092 (adjust in `docker-compose.yml` if that's
taken on dockerserver).

## Nginx Proxy Manager

Same pattern as your other irosec.com subdomains:

- Domain: `wiki.irosec.com`
- Forward hostname/IP: `192.168.178.233` (dockerserver)
- Forward port: `8092`
- Scheme: `http`
- SSL: request/attach the existing Cloudflare-issued cert or a new Let's
  Encrypt cert, force SSL + HTTP/2 as usual

## Updating content later

Because this is a static build, every content change needs a rebuild:

```bash
docker compose build && docker compose up -d
```

If you want this automated on `git push`, add a GitHub Action to the repo
that either (a) builds the image and pushes it to GHCR, with Watchtower
picking it up, or (b) SSHes into dockerserver and runs the two commands
above.
