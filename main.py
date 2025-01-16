from GraphAuthenticator import GraphAuthenticator
from ConditionalAccessPolicies import ConditionalAccessPolicies
from PolicyChecker import PolicyChecker
from ReportGenerator import ReportGenerator

def main():
    # Get authentication token
    auth = GraphAuthenticator()
    token = auth.authenticate()
    
    if token:
        # Get all policies
        ca_policies = ConditionalAccessPolicies(token)
        policies = ca_policies.get_all_policies()
        
        # Check policies against requirements
        checker = PolicyChecker('policy_requirements.yaml')
        results = checker.check_policies(policies)
        
        # Generate report
        report = ReportGenerator()
        report.generate_report(results)

if __name__ == '__main__':
    main()