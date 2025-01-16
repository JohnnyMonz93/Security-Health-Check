import requests
from typing import Dict, Any, List, Optional

class ConditionalAccessPolicies:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://graph.microsoft.com/v1.0"
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    
    def _print_authentication_flows(self, flows: Dict[str, Any]) -> None:
        """Print authentication flows details"""
        if flows:
            print("\nAuthentication Flows:")
            print(f"  Transfer Methods: {flows.get('transferMethods', 'Not specified')}")
    
    def _print_applications(self, apps: Dict[str, Any]) -> None:
        """Print applications details"""
        if apps:
            print("\nApplications:")
            print(f"  Include Applications: {', '.join(apps.get('includeApplications', []))}")
            print(f"  Exclude Applications: {', '.join(apps.get('excludeApplications', []))}")
            print(f"  Include User Actions: {', '.join(apps.get('includeUserActions', []))}")
            if apps.get('includeAuthenticationContextClassReferences'):
                print(f"  Authentication Context: {', '.join(apps['includeAuthenticationContextClassReferences'])}")
            if apps.get('applicationFilter'):
                print(f"  Application Filter: {apps['applicationFilter']}")
    
    def _print_users(self, users: Dict[str, Any]) -> None:
        """Print users details"""
        if users:
            print("\nUsers:")
            print(f"  Include Users: {', '.join(users.get('includeUsers', []))}")
            print(f"  Exclude Users: {', '.join(users.get('excludeUsers', []))}")
            print(f"  Include Groups: {', '.join(users.get('includeGroups', []))}")
            print(f"  Exclude Groups: {', '.join(users.get('excludeGroups', []))}")
            print(f"  Include Roles: {', '.join(users.get('includeRoles', []))}")
            print(f"  Exclude Roles: {', '.join(users.get('excludeRoles', []))}")
            
            if users.get('includeGuestsOrExternalUsers'):
                print(f"  Include Guests/External: {users['includeGuestsOrExternalUsers']}")
            if users.get('excludeGuestsOrExternalUsers'):
                print(f"  Exclude Guests/External: {users['excludeGuestsOrExternalUsers']}")
    
    def _print_conditions(self, conditions: Dict[str, Any]) -> None:
        """Print all conditions"""
        if conditions:
            print("\nConditions:")
            print(f"  User Risk Levels: {conditions.get('userRiskLevels', [])}")
            print(f"  Sign-in Risk Levels: {conditions.get('signInRiskLevels', [])}")
            print(f"  Client App Types: {conditions.get('clientAppTypes', [])}")
            print(f"  Service Principal Risk Levels: {conditions.get('servicePrincipalRiskLevels', [])}")
            print(f"  Insider Risk Levels: {conditions.get('insiderRiskLevels')}")
            print(f"  Platforms: {conditions.get('platforms')}")
            print(f"  Locations: {conditions.get('locations')}")
            print(f"  Devices: {conditions.get('devices')}")
            
            if conditions.get('applications'):
                self._print_applications(conditions['applications'])
            if conditions.get('users'):
                self._print_users(conditions['users'])
            if conditions.get('authenticationFlows'):
                self._print_authentication_flows(conditions['authenticationFlows'])
    
    def _print_grant_controls(self, controls: Dict[str, Any]) -> None:
        """Print grant controls"""
        if controls:
            print("\nGrant Controls:")
            print(f"  Operator: {controls.get('operator')}")
            print(f"  Built-in Controls: {', '.join(controls.get('builtInControls', []))}")
            print(f"  Custom Authentication Factors: {', '.join(controls.get('customAuthenticationFactors', []))}")
            print(f"  Terms of Use: {', '.join(controls.get('termsOfUse', []))}")
            
            auth_strength = controls.get('authenticationStrength')
            if auth_strength:
                print("\n  Authentication Strength:")
                print(f"    Display Name: {auth_strength.get('displayName')}")
                print(f"    Description: {auth_strength.get('description')}")
                print(f"    Requirements Satisfied: {auth_strength.get('requirementsSatisfied')}")
    
    def get_all_policies(self) -> Optional[List[Dict[str, Any]]]:
        """Retrieves and displays all Conditional Access policies"""
        print("\n📋 Retrieving Conditional Access Policies...")
        
        url = f"{self.base_url}/identity/conditionalAccess/policies"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            policies = response.json().get('value', [])
            
            if not policies:
                print("No Conditional Access policies found.")
                return []
                
            print(f"\n✅ Found {len(policies)} Conditional Access policies:\n")
            
            for policy in policies:
                print("=" * 80)
                print(f"Policy Name: {policy.get('displayName')}")
                print(f"ID: {policy.get('id')}")
                print(f"State: {policy.get('state')}")
                print(f"Created: {policy.get('createdDateTime')}")
                print(f"Modified: {policy.get('modifiedDateTime')}")
                
                self._print_conditions(policy.get('conditions', {}))
                self._print_grant_controls(policy.get('grantControls', {}))
                
                print("=" * 80 + "\n")
            
            return policies
                
        except requests.exceptions.RequestException as e:
            print(f"\n❌ Error retrieving policies: {str(e)}")
            return [] 