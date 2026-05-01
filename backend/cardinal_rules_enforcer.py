#!/usr/bin/env python3
"""
LAYER 4: CARDINAL RULES SECURITY ENFORCEMENT
Ensures all 4 Cardinal Rules are enforced across ALL missions
"""

class CardinalRulesSecurityEnforcer:
    def __init__(self):
        self.cardinal_rules = {
            "RULE_1": "System Integrity Above All",
            "RULE_2": "Data Protection is Paramount", 
            "RULE_3": "User Privacy is Sacred",
            "RULE_4": "Never Fail Protected Populations (Children, Veterans, Patients)"
        }
        
        self.protected_populations = {
            "CHILDREN": {"count": 42_000_000, "failure_tolerance": 0.02},    # 98% minimum
            "VETERANS": {"count": 22_000_000, "failure_tolerance": 0.02},    # 98% minimum
            "MEDICAL": {"count": "UNLIMITED", "failure_tolerance": 0.01},     # 99% minimum
            "GENERAL": {"count": "UNLIMITED", "failure_tolerance": 0.05}      # 95% minimum
        }
        
    def enforce_rule_4_capacity(self, mission_type, current_capacity):
        """Enforce Cardinal Rule #4 capacity requirements by mission"""
        population = self.protected_populations.get(mission_type, self.protected_populations["GENERAL"])
        minimum_capacity = 1.0 - population["failure_tolerance"]
        
        if current_capacity < minimum_capacity:
            required_pct = minimum_capacity * 100
            current_pct = current_capacity * 100
            
            raise CardinalRuleViolation(
                f"CARDINAL RULE #4 VIOLATION: {mission_type} capacity {current_pct:.1f}% "
                f"below required {required_pct:.1f}% - PROTECTED POPULATION AT RISK"
            )
            
        return True
        
    def validate_all_cardinal_rules(self, system_state):
        """Validate all Cardinal Rules across the entire system"""
        violations = []
        
        # Rule 1: System Integrity
        if not system_state.get("integrity_verified"):
            violations.append("RULE_1: System integrity not verified")
            
        # Rule 2: Data Protection
        if not system_state.get("data_encrypted"):
            violations.append("RULE_2: Data protection not ensured")
            
        # Rule 3: User Privacy  
        if not system_state.get("privacy_controls_active"):
            violations.append("RULE_3: User privacy controls not active")
            
        # Rule 4: Protected Population Support
        for mission, capacity in system_state.get("mission_capacities", {}).items():
            try:
                self.enforce_rule_4_capacity(mission, capacity)
            except CardinalRuleViolation as e:
                violations.append(str(e))
                
        if violations:
            raise CardinalRuleViolation(f"Multiple Cardinal Rule violations: {violations}")
            
        return True

class CardinalRuleViolation(Exception):
    """Critical violation of Cardinal Rules that threatens mission success"""
    pass

__all__ = ['CardinalRulesSecurityEnforcer', 'CardinalRuleViolation']
