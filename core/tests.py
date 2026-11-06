from django.test import TestCase
from .services import mask_pii, dpdp_report

class Tests(TestCase):
    def test_mask(self):
        t, n = mask_pii("Mail a@b.com PAN ABCDE1234F phone 9876543210 aadhaar 1234 5678 9012")
        self.assertEqual(n, 4)
        self.assertNotIn("9876543210", t)
    def test_dpdp(self):
        self.assertEqual(dpdp_report({k: "yes" for k in ["consent","notice","purpose","rights","security","breach","children","grievance"]})[0], 100)
    def test_api(self):
        r = self.client.post("/api/gateway/", data='{"text": "PAN ABCDE1234F"}', content_type="application/json").json()
        self.assertEqual(r["pii_types"], {"PAN": 1})
        self.assertEqual(self.client.get("/health/").json()["status"], "ok")
    def test_pages(self):
        for u in ["/", "/gateway/", "/redteam/", "/dpdp/", "/kagaz/"]:
            self.assertEqual(self.client.get(u).status_code, 200)
        self.assertEqual(self.client.post("/redteam/").context["score"], 100)
