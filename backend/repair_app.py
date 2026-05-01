#!/usr/bin/env python3
import re, sys, hashlib, os, textwrap

SRC = "app.py.DISABLED"
OUT = "app.py"

code = open(SRC, "r", encoding="utf-8").read()

# 0) Normalize weird linewrap artifacts
code = code.replace("\r\n", "\n")

# 1) Collapse duplicate import blocks (exact duplicates)
seen_blocks = set()
lines = code.split("\n")
out_lines = []
block = []
in_import_block = False

def flush_block():
    global out_lines, block, seen_blocks
    if not block:
        return
    btxt = "\n".join(block).strip()
    h = hashlib.sha256(btxt.encode()).hexdigest()
    if h not in seen_blocks:
        out_lines.extend(block)
        seen_blocks.add(h)
    block = []

for i, ln in enumerate(lines):
    if re.match(r"^\s*(from\s+\S+\s+import\s+\S+|import\s+\S+)", ln):
        if not in_import_block:
            in_import_block = True
            block = []
        block.append(ln)
    else:
        if in_import_block:
            flush_block()
            in_import_block = False
        out_lines.append(ln)
if in_import_block:
    flush_block()

code = "\n".join(out_lines)

# 2) Drop exact duplicate lines that occur back-to-back (common after merges)
dedup_lines = []
for ln in code.split("\n"):
    if not dedup_lines or dedup_lines[-1] != ln:
        dedup_lines.append(ln)
code = "\n".join(dedup_lines)

# 3) Keep only the first definition per Flask route path (avoid overrides)
route_pat = re.compile(r'@app\.route\(\s*[\'"]([^\'"]+)[\'"][^)]*\)\s*\ndef\s+([A-Za-z_]\w*)\s*\(', re.S)
kept_paths = set()
result = []
i = 0
lines = code.split("\n")
while i < len(lines):
    ln = lines[i]
    if ln.strip().startswith("@app.route("):
        # look ahead for the def line and capture the function block
        block_start = i
        m = route_pat.match("\n".join(lines[i:i+3]))
        if m:
            path = m.group(1)
            # capture until next decorator or EOF
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("@app.route("):
                # stop at top-level def that isn't connected to this decorator
                if lines[j].startswith("def ") and (j == i+1):
                    break
                j += 1
            # crude function block capture until next decorator or blank line + decorator
            # safer: extend until next @app.route or end
            k = j
            while k < len(lines):
                if lines[k].strip().startswith("@app.route("):
                    break
                k += 1
            block = lines[block_start:k]
            if path not in kept_paths:
                result.extend(block)
                kept_paths.add(path)
            # skip consumed block
            i = k
            continue
    result.append(ln)
    i += 1
code = "\n".join(result)

# 4) Fix research cache mismatch: code was checking .pkl but opening .json
code = code.replace(
    "os.path.exists(os.path.join(\"data\", \"research_cache.pkl\"))",
    "os.path.exists(os.path.join(\"data\", \"research_cache.json\"))"
)

# 5) Guard duplicate learning route registration
code = code.replace(
    "from routes import register_learning_routes\n    success = register_learning_routes(app)",
    "from routes import register_learning_routes\n    if not getattr(app, '_learning_routes_registered', False):\n        success = register_learning_routes(app)\n        app._learning_routes_registered = bool(success)\n    else:\n        success = True"
)

# 6) Make ai_control robust (optional engines + JSON fallback) if a brittle version exists
if 'def ai_control():' in code and 'render_template("ai_control.html"' in code and "try:" not in code.split("def ai_control():",1)[1][:200]:
    ai_control_safe = textwrap.dedent('''
    @app.route("/ai_control")
    def ai_control():
        """AI Control Center for managing autonomous learning"""
        if "name" not in session:
            return redirect(url_for("index"))

        learning_engine = None
        code_engine = None
        try:
            from ai_learning_engine import get_self_improvement_engine
            learning_engine = get_self_improvement_engine()
        except Exception as e:
            logging.warning(f"ai_control: learning engine unavailable: {e}")
        try:
            from self_modifying_code import get_self_modifying_code_engine
            code_engine = get_self_modifying_code_engine()
        except Exception as e:
            logging.warning(f"ai_control: self-modifying engine unavailable: {e}")

        learning_active = bool(getattr(learning_engine, "learning_active", False))
        auto_mode_active = bool(getattr(code_engine, "auto_mode_active", False))

        recent_improvements, recent_modifications = [], []

        # Improvements
        try:
            stats = getattr(getattr(learning_engine, "model_optimizer", None), "interaction_stats", {}) or {}
            for key, s in (stats.get("intents", {}) or {}).items():
                cnt = int(s.get("count", 0) or 0)
                if cnt > 5:
                    conf = 0
                    if cnt > 0 and s.get("confidence_sum") is not None:
                        try:
                            conf = round((float(s.get("confidence_sum", 0.0)) / cnt) * 100)
                        except Exception:
                            conf = 0
                    recent_improvements.append({
                        "description": f"Improved recognition for '{key}' intent",
                        "details": f"Based on {cnt} interactions with {int(s.get('success', 0) or 0)} successes",
                        "confidence": conf,
                        "timestamp": s.get("last_used", "Unknown"),
                    })
        except Exception as e:
            logging.warning(f"ai_control: improvements build failed: {e}")

        # Modifications
        try:
            mods = getattr(getattr(code_engine, "code_modifier", None), "modifications", []) or []
            for m in mods[-5:]:
                recent_modifications.append({
                    "file_path": m.get("file_path", "Unknown"),
                    "status": "applied" if m.get("applied", False) else "pending",
                    "description": (m.get("description", "") or "").split("\\n")[0],
                    "timestamp": m.get("timestamp", "Unknown"),
                    "diff": m.get("diff", ""),
                })
        except Exception as e:
            logging.warning(f"ai_control: modifications read failed: {e}")

        research_status = {"last_update": None, "articles_count": 0}
        try:
            cache_path = os.path.join("data", "research_cache.json")
            if os.path.exists(cache_path):
                import json
                with open(cache_path, "r", encoding="utf-8") as f:
                    cache = json.load(f)
                research_status["last_update"] = cache.get("timestamp")
                research_status["articles_count"] = len(cache.get("articles", []))
        except Exception as e:
            logging.warning(f"ai_control: research status failed: {e}")

        # Basic stats
        interactions_count = 0
        try:
            stats = getattr(getattr(learning_engine, "model_optimizer", None), "interaction_stats", {}) or {}
            for section in stats.values():
                if isinstance(section, dict):
                    interactions_count += sum(int((v or {}).get("count", 0) or 0) for v in section.values())
        except Exception:
            pass

        ctx = {
            "learning_active": learning_active,
            "auto_mode_active": auto_mode_active,
            "recent_improvements": recent_improvements,
            "recent_modifications": recent_modifications,
            "learning_actions": ([
                "Analyzing user interaction patterns",
                "Optimizing intent classification weights",
                "Processing emotional context correlations",
                "Updating multimodal recognition models",
            ] if learning_active else []),
            "last_optimization": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "interactions_count": interactions_count,
            "pending_modifications_count": sum(1 for m in recent_modifications if m.get("status") == "pending"),
            "applied_modifications_count": sum(1 for m in recent_modifications if m.get("status") == "applied"),
            "learning_progress": min(95, int(interactions_count / 10) + 30) if interactions_count else 30,
            "confidence_score": 75, "intent_recognition": 82, "emotion_processing": 68, "self_repair": 54,
            "research_status": research_status,
        }
        try:
            return render_template("ai_control.html", **ctx)
        except Exception as e:
            logging.warning(f"ai_control: template missing, returning JSON: {e}")
            return jsonify({"status": "ok", "view": "ai_control", **ctx})
    ''').strip("\n")

    # Replace the first ai_control definition
    code = re.sub(r'@app\.route\([^\n]+\)\s*\ndef\s+ai_control\(\):.*?(?=\n@|$)', ai_control_safe, code, flags=re.S)

# 7) Ensure logging configured once at top
code = re.sub(r'logging\.basicConfig\(.*?\)\s*', 'logging.basicConfig(level=logging.DEBUG)\n', code, flags=re.S)

open(OUT, "w", encoding="utf-8").write(code)
print(f"Wrote cleaned {OUT}")


__all__ = ['flush_block']
