import yaml
from typing import Dict, List, Any, Union

class PolicyChecker:
    def __init__(self, requirements_file: str = 'policy_requirements.yaml'):
        self.requirements = self._load_requirements(requirements_file)
        self.results = []
        
    def _load_requirements(self, file_path: str) -> Dict:
        """Load requirements from YAML file"""
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
            
    def _compare_lists(self, policy_list: Union[List, None], required_list: Union[List, None]) -> bool:
        """Compare two lists regardless of order, handling None values"""
        # Convert None to empty list
        policy_list = policy_list if policy_list is not None else []
        required_list = required_list if required_list is not None else []
        
        # Ensure we're working with lists
        if not isinstance(policy_list, list):
            policy_list = [policy_list]
        if not isinstance(required_list, list):
            required_list = [required_list]
            
        return all(item in policy_list for item in required_list)
    
    def _get_nested_value(self, obj: Dict, key: str, default: Any = None) -> Any:
        """Safely get nested dictionary values"""
        try:
            return obj.get(key, default)
        except (AttributeError, TypeError):
            return default
    
    def _policy_matches_requirements(self, policy: Dict, required: Dict) -> bool:
        """Check if a policy matches the required conditions and controls"""
        try:
            # Check conditions
            required_conditions = required.get('required_conditions', {})
            policy_conditions = policy.get('conditions', {})
            
            for key, value in required_conditions.items():
                policy_value = self._get_nested_value(policy_conditions, key)
                
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        policy_sub_value = self._get_nested_value(policy_value, sub_key)
                        if not self._compare_lists(policy_sub_value, sub_value):
                            return False
                elif isinstance(value, list):
                    if not self._compare_lists(policy_value, value):
                        return False
                elif policy_value != value:
                    return False
                    
            # Check controls
            required_controls = required.get('required_controls', {})
            if 'grantControls' in required_controls:
                policy_controls = policy.get('grantControls', {})
                required_grant = required_controls['grantControls']
                
                for key, value in required_grant.items():
                    policy_control_value = self._get_nested_value(policy_controls, key)
                    if isinstance(value, list):
                        if not self._compare_lists(policy_control_value, value):
                            return False
                    elif policy_control_value != value:
                        return False
                        
            return True
            
        except Exception as e:
            print(f"Error checking policy {policy.get('displayName')}: {str(e)}")
            return False
    
    def check_policies(self, policies: List[Dict]) -> List[Dict]:
        """Check if policies meet requirements"""
        self.results = []
        required_policies = self.requirements.get('required_policies', [])
        
        for required in required_policies:
            policy_found = False
            matching_policies = []
            
            for policy in policies:
                try:
                    if self._policy_matches_requirements(policy, required):
                        policy_found = True
                        matching_policies.append(policy['displayName'])
                except Exception as e:
                    print(f"Error processing policy {policy.get('displayName')}: {str(e)}")
                    continue
            
            result = {
                'requirement_name': required['name'],
                'found': policy_found,
                'matching_policies': matching_policies,
                'status': 'PRESENT' if policy_found else 'MISSING'
            }
            self.results.append(result)
            
        return self.results 