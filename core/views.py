import json
from collections import Counter
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from . import services as s
from .models import RequestLog

def _gateway(text):
    masked, n, types = s.mask_detail(text)
    reply = s.ask_llm(masked)
    RequestLog.objects.create(kind="gateway", prompt_masked=masked, response=reply, pii_count=n, pii_types=types)
    return masked, n, reply, types

def health(request):
    return JsonResponse({"status": "ok"})

def dashboard(request):
    c = Counter()
    for t in RequestLog.objects.values_list("pii_types", flat=True):
        c.update(t)
    mx = max(c.values(), default=1)
    types = [(k, v, round(100 * v / mx)) for k, v in c.most_common()]
    return render(request, "core/dashboard.html", {"types": types, "total": RequestLog.objects.count(),
        "pii": RequestLog.objects.aggregate(t=Sum("pii_count"))["t"] or 0, "logs": RequestLog.objects.all()[:10]})

def gateway(request):
    ctx = {}
    if request.method == "POST":
        text = request.POST.get("text", "")
        ctx["masked"], ctx["n"], ctx["reply"], _ = _gateway(text)
    return render(request, "core/gateway.html", ctx)

@csrf_exempt
def api_gateway(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    try:
        text = json.loads(request.body).get("text", "")
    except ValueError:
        return JsonResponse({"error": "invalid JSON"}, status=400)
    masked, n, reply, types = _gateway(text)
    return JsonResponse({"masked_prompt": masked, "pii_masked": n, "pii_types": types, "reply": reply})

def redteam(request):
    ctx = {}
    if request.method == "POST":
        ctx["results"], ctx["score"] = s.run_redteam()
    return render(request, "core/redteam.html", ctx)

def dpdp(request):
    ctx = {"questions": s.DPDP}
    if request.method == "POST":
        ctx["score"], ctx["level"], ctx["gaps"] = s.dpdp_report({k: request.POST.get(k) for k, _, _ in s.DPDP})
    return render(request, "core/dpdp.html", ctx)

def kagaz(request):
    ctx = {}
    if request.method == "POST":
        ctx["out"], ctx["n"], types = s.explain_document(request.POST.get("text", ""), request.POST.get("lang", "Hindi"))
        RequestLog.objects.create(kind="kagaz", prompt_masked=request.POST.get("text", "")[:300], response=ctx["out"], pii_count=ctx["n"], pii_types=types)
    return render(request, "core/kagaz.html", ctx)
