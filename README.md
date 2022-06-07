**Important:** This repo was **deprecated** in favor of https://git.leon.wtf/leon/new-cfupdater !!!

# Usage

## Configuration via config.env
Fill in the `CF_EMAIL` (Cloudflare account E-Mail) and `CF_TOKEN` (Cloudflare Global API Key) fields.

Fill `ZONES_TO_UPDATE` and `HOSTS_TO_UPDATE` with comma seperated Cloudflare Zones and Hosts you want to have updated. (examples are given in `config.env`)

Set `WITH_IPV6` to 1 if you wish to update AAAA-Records as well.

## Run
Execute `docker run -d --name cfupdater --restart always --network host --env-file ./config.env registry.git.leon.wtf/leon/cfupdater:latest` in the same directory as `config.env`.

To view logs, execute `docker logs -f cfupdater`.
