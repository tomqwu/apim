import http from "k6/http";
import { check } from "k6";

export const options = {
  vus: 2,
  duration: "10s",
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<500"],
  },
};

const base = __ENV.BASE_URL || "http://localhost:8000";
const key = __ENV.API_KEY || "api-platform-poc-key";

export default function () {
  const response = http.get(`${base}/v1/accounts/synthetic-001`, {
    headers: { apikey: key },
  });
  check(response, {
    "status is 200": (r) => r.status === 200,
    "response is synthetic": (r) => r.json("synthetic") === true,
    "correlation returned": (r) => Boolean(r.headers["X-Correlation-Id"]),
  });
}
