# CYP1A2 Caffeine Metabolism Kinetics & Curfew Chronotype Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `model_caffeine_clearance_curfew`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Simulates CYP1A2 SNP pharmacokinetics, paraxanthine decay curves, adenosine A1/A2A receptor blockade, and sets a personalized caffeine intake curfew.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Personal Agent (Bio / Pharmacogenomics)`

## MCP Tool Specification
### `model_caffeine_clearance_curfew`
Parameters:
- `cyp1a2_genotype` (str): Genotype: '*1A/*1A' (Rapid) or '*1A/*1F' (Intermediate) or '*1F/*1F' (Slow)
- `intake_mg` (float): Caffeine consumed (mg)
- `intake_time_decimal_hour` (float): Time of intake in 24h format (e.g. 14.5 for 2:30 PM)
- `planned_bedtime_decimal_hour` (float): Planned bedtime in 24h format (e.g. 23.0 for 11:00 PM)
- `is_smoker` (bool): Whether active smoker (induces CYP1A2)
- `is_oral_contraceptive_user` (bool): Whether taking estrogenic oral contraceptives (inhibits CYP1A2)

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-personal-agent-cyp1a2-caffeine-metabolism-clearance-chronotype-skill": {
      "command": "python",
      "args": ["/path/to/genpark-personal-agent-cyp1a2-caffeine-metabolism-clearance-chronotype-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
