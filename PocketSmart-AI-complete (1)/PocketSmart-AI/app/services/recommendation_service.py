import json
from app.services.catalog import catalog_for, public_item
from app.services.gemini_service import generate

def prompt(kind, data, catalog):
    return (
        "You are PocketSmart AI. Create budget-aware recommendations. "
        "Use ONLY the supplied catalog. Never claim prices are live. "
        "Return JSON with summary, allocations object, and recommendations array. "
        "Each recommendation must contain title, category, platform, price, reason, url.\n"
        f"Planner: {kind}\nRequest: {json.dumps(data)}\nCatalog: {json.dumps(catalog)}"
    )

def fallback(kind, data, catalog):
    budget = float(data["budget"])
    if kind == "home":
        alloc = {"lighting": budget*.20, "fan": budget*.15, "furniture": budget*.35, "dining": budget*.20, "decor": budget*.10}
        summary = f"Home plan for {data['style']} style across {len(data['rooms'])} room type(s)."
    elif kind == "party":
        alloc = {"catering": budget*.55, "decoration": budget*.20, "entertainment": budget*.15, "accommodation": budget*.10}
        summary = f"{data['event_type']} plan for {data['guest_count']} guest(s), prioritizing food."
    else:
        alloc = {"necklace": budget*.45, "earrings": budget*.30, "bracelet": budget*.15, "reserve": budget*.10}
        summary = f"Jewelry ideas for {data['occasion']} in {data['style']} style."
    recs = [public_item(x) for x in catalog if x["price"] <= budget][:5]
    return {"summary":summary, "allocations":{k:round(v,2) for k,v in alloc.items()}, "recommendations":recs}

def build(kind, data, image_bytes=None, mime_type=None):
    catalog = catalog_for(kind)
    ai = generate(prompt(kind, data, catalog), image_bytes, mime_type)
    result = ai if ai and isinstance(ai.get("recommendations"), list) else fallback(kind, data, catalog)
    return {
      "planner_type": kind,
      "budget": float(data["budget"]),
      "allocated_total": round(sum(float(v) for v in result.get("allocations",{}).values()),2),
      "summary": result.get("summary",""),
      "allocations": result.get("allocations",{}),
      "recommendations": result.get("recommendations",[]),
      "source_mode": "gemini" if ai else "mock"
    }
