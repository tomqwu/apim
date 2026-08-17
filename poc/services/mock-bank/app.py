#!/usr/bin/env python3
import json
import os
import re
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse


class Handler(BaseHTTPRequestHandler):
    server_version = "synthetic-bank/1.0"

    def log_message(self, fmt, *args):
        print(json.dumps({"event": "access", "client": self.client_address[0], "message": fmt % args}))

    def send_json(self, status, body):
        encoded = json.dumps(body, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length > 65536:
            raise ValueError("payload too large")
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw)

    def base(self):
        return {
            "synthetic": True,
            "correlationId": self.headers.get("X-Correlation-ID"),
            "gatewayMarker": self.headers.get("X-API-Platform-Gateway"),
        }

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/health":
            return self.send_json(200, {"status": "ok", "synthetic": True})
        match = re.fullmatch(r"/v1/accounts/([A-Za-z0-9-]{1,64})", path)
        if match:
            return self.send_json(200, self.base() | {"accountId": match.group(1), "currency": "CAD", "status": "ACTIVE", "balance": 1250.42})
        match = re.fullmatch(r"/v1/customers/([A-Za-z0-9-]{1,64})", path)
        if match:
            return self.send_json(200, self.base() | {"customerId": match.group(1), "displayName": "Synthetic Customer", "segment": "PERSONAL"})
        if path == "/v1/transactions":
            return self.send_json(200, self.base() | {"items": [{"transactionId": "txn-synthetic-1", "amount": 42.50, "currency": "CAD", "kind": "DEBIT"}]})
        return self.send_json(404, self.base() | {"error": "not_found"})

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            body = self.read_json()
        except (ValueError, json.JSONDecodeError) as exc:
            return self.send_json(400, self.base() | {"error": "invalid_request", "detail": str(exc)})
        if path == "/v1/payments":
            return self.send_json(200, self.base() | {"paymentId": "pay-" + uuid.uuid4().hex[:12], "status": "ACCEPTED", "received": body})
        if path == "/v1/transfers":
            return self.send_json(200, self.base() | {"transferId": "trf-" + uuid.uuid4().hex[:12], "status": "ACCEPTED", "received": body})
        if path == "/v1/beneficiaries":
            return self.send_json(200, self.base() | {"beneficiaryId": "ben-" + uuid.uuid4().hex[:12], "status": "CREATED", "received": body})
        return self.send_json(404, self.base() | {"error": "not_found"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
