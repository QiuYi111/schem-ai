# Lightpanda Notes

This file summarizes the official Lightpanda README and installation docs for this repository.

## Source

- GitHub README: https://github.com/lightpanda-io/browser
- Installation docs: https://lightpanda.io/docs/open-source/installation
- Retrieved: 2026-03-15

## What It Is

Lightpanda is a headless browser built for automation and AI-agent workflows. The official README positions it as a lightweight browser for JavaScript execution, DOM interaction, and CDP-compatible automation.

## Modes We Care About

1. `fetch`
   Use for one-shot page retrieval and DOM dumping when we want quick HTML output without a long-lived browser session.

   Example:

   ```sh
   ./.tools/bin/lightpanda fetch --dump https://example.com
   ```

2. `serve`
   Use when a CDP client or browser automation stack needs a persistent browser endpoint.

   Example:

   ```sh
   ./.tools/bin/lightpanda serve --host 127.0.0.1 --port 9222
   ```

## Agent Guidance

Use `fetch --dump` first when the goal is:

- quick DOM inspection
- text extraction after JavaScript execution
- validating whether a page is reachable and script-rendered

Use `serve` only when the task needs a long-lived browser session, multiple pages, or a CDP client such as Puppeteer.

Prefer keeping the host bound to `127.0.0.1` for local usage.

## Telemetry

The official README says telemetry is enabled by default. Disable it for local agent workflows with:

```sh
export LIGHTPANDA_DISABLE_TELEMETRY=true
```

## Install Notes For This Repo

Our bootstrap script installs the macOS aarch64 nightly binary into `.tools/bin/lightpanda`.

If the upstream release path changes, update `LIGHTPANDA_URL` in `scripts/bootstrap.py`.

## Constraints

- The project is still beta and coverage is incomplete.
- Some sites may fail or behave differently from Chromium-based browsers.
- Prefer Lightpanda for lightweight page execution, not as a full browser replacement.
