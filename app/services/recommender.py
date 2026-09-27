from .catalog import CATALOG
from .gemini import GeminiService
from .prompts import build_prompt

class Recommender:
    def __init__(self):
        self.gemini = GeminiService()

    def _fallback(self, planner, payload):
        budget = float(payload["budget"])
        items = CATALOG[planner]
        if planner == "party":
            guest = int(payload["guests"])
            per_guest = max(1, budget * 0.55 / guest)
            chosen = []
            for item in items:
                if item["category"] in {"Catering", "Decoration", "Venue"}:
                    x = dict(item)
                    if x["category"] == "Catering":
                        x["estimated_price"] = round(per_guest, 2)
                    chosen.append(x)
            allocations = {"Catering": budget * 0.55, "Decoration": budget * 0.15, "Venue": budget * 0.25, "Buffer": budget * 0.05}
            summary = f"A starter {payload['event_type']} plan for {guest} guests at {payload['venue']}."
        elif planner == "home":
            chosen = [dict(x) for x in items[:4]]
            allocations = {"Furniture": budget * .45, "Lighting": budget * .15, "Storage": budget * .20, "Decor": budget * .20}
            summary = "A balanced home setup prioritizing useful furniture, storage, lighting and decor."
        else:
            chosen = [dict(x) for x in items[:4]]
            allocations = {"Necklace": budget * .40, "Earrings": budget * .25, "Bracelet": budget * .20, "Buffer": budget * .15}
            summary = f"A {payload['style']} jewelry starter plan for {payload['occasion']}."
        total = round(sum(v for k, v in allocations.items() if k != "Buffer"), 2)
        for x in chosen:
            x["estimated_price"] = round(min(float(x["estimated_price"]), budget), 2)
        return {"planner": planner, "summary": summary, "budget": budget, "currency": payload["currency"], "allocated_total": total, "remaining_budget": round(max(0, budget-total), 2), "tips": ["Treat listed prices as estimates and verify the current seller price before purchase.", "Keep a small buffer for delivery, taxes, or unexpected costs."], "recommendations": chosen, "source": "fallback"}

    def recommend(self, planner, payload, image_bytes=None, mime_type=None):
        result = self.gemini.generate(build_prompt(planner, payload), image_bytes, mime_type)
        if result and isinstance(result.get("recommendations"), list):
            budget = float(payload["budget"])
            recs = []
            for r in result["recommendations"][:12]:
                try:
                    r["estimated_price"] = float(r.get("estimated_price", 0))
                    recs.append(r)
                except (TypeError, ValueError):
                    pass
            result["planner"] = planner
            result["budget"] = budget
            result["currency"] = payload["currency"]
            result["source"] = "gemini"
            result["allocated_total"] = float(result.get("allocated_total", sum(x["estimated_price"] for x in recs)))
            result["remaining_budget"] = round(max(0, budget-result["allocated_total"]), 2)
            result["tips"] = result.get("tips", [])
            result["recommendations"] = recs
            return result
        return self._fallback(planner, payload)
