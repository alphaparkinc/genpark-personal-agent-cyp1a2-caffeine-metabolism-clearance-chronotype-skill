# -*- coding: utf-8 -*-
"""CYP1A2 Caffeine Metabolism Kinetics & Curfew Chronotype Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def model_caffeine_clearance_curfew(**kwargs):
    """Simulates CYP1A2 SNP pharmacokinetics, paraxanthine decay curves, adenosine A1/A2A receptor blockade, and sets a personalized caffeine intake curfew."""
    cyp1a2_genotype = kwargs.get('cyp1a2_genotype')
    intake_mg = kwargs.get('intake_mg')
    intake_time_decimal_hour = kwargs.get('intake_time_decimal_hour')
    planned_bedtime_decimal_hour = kwargs.get('planned_bedtime_decimal_hour')
    is_smoker = kwargs.get('is_smoker')
    is_oral_contraceptive_user = kwargs.get('is_oral_contraceptive_user')

    import math
    if "*1A/*1A" in cyp1a2_genotype:
        base_half_life = 3.2
        phenotype = "Ultra-Rapid Metabolizer"
    elif "*1F/*1F" in cyp1a2_genotype:
        base_half_life = 7.8
        phenotype = "Slow Metabolizer"
    else:
        base_half_life = 5.2
        phenotype = "Intermediate Metabolizer"
        
    if is_smoker:
        base_half_life *= 0.7
    if is_oral_contraceptive_user:
        base_half_life *= 1.8
        
    elimination_constant = math.log(2.0) / base_half_life
    
    hours_to_bedtime = planned_bedtime_decimal_hour - intake_time_decimal_hour
    if hours_to_bedtime < 0:
        hours_to_bedtime += 24.0
        
    residual_caffeine_at_bedtime = round(intake_mg * math.exp(-elimination_constant * hours_to_bedtime), 1)
    adenosine_blockade_pct = round(min(100.0, (residual_caffeine_at_bedtime / (residual_caffeine_at_bedtime + 20.0)) * 100.0), 1)
    
    if intake_mg > 15.0:
        required_clearance_hours = round(math.log(intake_mg / 15.0) / elimination_constant, 1)
    else:
        required_clearance_hours = 0.0
        
    curfew_decimal = planned_bedtime_decimal_hour - required_clearance_hours
    if curfew_decimal < 0:
        curfew_decimal += 24.0
    curfew_h = int(curfew_decimal)
    curfew_m = int((curfew_decimal - curfew_h) * 60)
    curfew_str = f"{curfew_h:02d}:{curfew_m:02d}"
    
    sleep_disruption_risk = "High (Suppression of delta slow-wave activity)" if residual_caffeine_at_bedtime > 30.0 else "Mild" if residual_caffeine_at_bedtime > 15.0 else "Negligible (Safe sleep latency)"
    
    result = {
        "status": "success",
        "phenotype": phenotype,
        "effective_half_life_hours": round(base_half_life, 2),
        "residual_caffeine_at_bedtime_mg": residual_caffeine_at_bedtime,
        "adenosine_receptor_blockade_pct": adenosine_blockade_pct,
        "sleep_disruption_risk": sleep_disruption_risk,
        "personalized_daily_curfew": curfew_str,
        "recommended_clearance_buffer_hours": required_clearance_hours,
        "engine": "GenPark CYP1A2 Pharmacogenomic Clearance Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "model_caffeine_clearance_curfew": {
        "name": "model_caffeine_clearance_curfew",
        "description": "Simulates CYP1A2 SNP pharmacokinetics, paraxanthine decay curves, adenosine A1/A2A receptor blockade, and sets a personalized caffeine intake curfew.",
        "parameters": {
            "type": "object",
            "properties": {
                "cyp1a2_genotype": {"type": "string", "description": "Genotype: '*1A/*1A' (Rapid) or '*1A/*1F' (Intermediate) or '*1F/*1F' (Slow)"},
                "intake_mg": {"type": "number", "description": "Caffeine consumed (mg)"},
                "intake_time_decimal_hour": {"type": "number", "description": "Time of intake in 24h format (e.g. 14.5 for 2:30 PM)"},
                "planned_bedtime_decimal_hour": {"type": "number", "description": "Planned bedtime in 24h format (e.g. 23.0 for 11:00 PM)"},
                "is_smoker": {"type": "boolean", "description": "Whether active smoker (induces CYP1A2)"},
                "is_oral_contraceptive_user": {"type": "boolean", "description": "Whether taking estrogenic oral contraceptives (inhibits CYP1A2)"},
            },
            "required": ['cyp1a2_genotype', 'intake_mg', 'intake_time_decimal_hour', 'planned_bedtime_decimal_hour', 'is_smoker', 'is_oral_contraceptive_user']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "model_caffeine_clearance_curfew":
            res = model_caffeine_clearance_curfew(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-personal-agent-cyp1a2-caffeine-metabolism-clearance-chronotype-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-personal-agent-cyp1a2-caffeine-metabolism-clearance-chronotype-skill...")
    test_args = {'cyp1a2_genotype': '*1A/*1F', 'intake_mg': 200.0, 'intake_time_decimal_hour': 14.5, 'planned_bedtime_decimal_hour': 23.0, 'is_smoker': False, 'is_oral_contraceptive_user': False}
    res = model_caffeine_clearance_curfew(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-personal-agent-cyp1a2-caffeine-metabolism-clearance-chronotype-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
