---
name: api-and-webhooks
description: Connect any app to an automation through its API or webhooks, including auth, pagination, rate limits, retries and webhook security. Use when the user needs an HTTP request step, wants to call an API that has no built-in node, receive webhooks, verify a webhook signature, or fix 401, 403, 404 or 429 errors in a workflow.
---

# APIs and Webhooks

Most "missing integrations" are one HTTP request away. Read the API docs, then build the call so it keeps working when data grows or the API has a bad day.

## Calling an API

1. Find in the API docs: base URL, endpoint, method, auth type, required headers, body format, rate limit.
2. Pick the auth pattern:

| Auth type | How it is sent |
|---|---|
| API key | Header such as `Authorization: Bearer <key>` or `X-API-Key: <key>`, or a query parameter if the docs say so |
| Basic auth | Username and password, sent as a Base64 `Authorization: Basic` header |
| OAuth2 | Use the tool's OAuth2 credential type; the callback URL must match exactly |

3. Store the secret in the tool's credential store, never in the URL or body text of the flow.
4. Send JSON with `Content-Type: application/json` unless the docs ask for form data.

## Pagination

- Check which style the API uses: page number, offset and limit, a cursor or "next" token, or a `Link` header.
- Use the tool's built-in pagination when it has one (n8n's HTTP Request node does). Otherwise loop until the next cursor is empty.
- Always set a maximum number of pages as a safety stop.

## Rate limits and retries

- Respect the documented limit. Batch items and add a short wait between batches.
- On `429` or `5xx`, retry with a growing delay (for example 2, 4, 8 seconds), and honor a `Retry-After` header if present.
- Do not retry `400`, `401`, `403` or `404`; they need a fix, not another attempt.

| Error | Usual cause |
|---|---|
| 401 | Missing or expired key or token |
| 403 | Key is valid but lacks the permission or scope |
| 404 | Wrong URL, ID or API version |
| 422 | Body fields missing or in the wrong format |
| 429 | Too many requests |

## Receiving webhooks

- Give each webhook a long, random path, and add header auth or basic auth when the sender supports it.
- If the sender signs requests (Stripe, GitHub, Shopify and others), verify the signature with the shared secret before using the data. This usually needs the raw request body.
- Answer fast with a `200`, then do slow work after, or the sender may retry and create duplicates.
- Make processing idempotent: store the event ID and skip IDs you have already handled.
- Use the test URL while building and the production URL once the flow is live.

## Deliver

The exact request (method, URL, headers with placeholders, body), the pagination and retry settings, and one sample response showing the fields the next step will use.
