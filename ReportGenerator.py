from fpdf import FPDF
from datetime import datetime
from typing import List, Dict

class ReportGenerator:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.add_page()
        
    def generate_report(self, policy_results: List[Dict], output_file: str = None):
        """Generate PDF report from policy check results"""
        if not output_file:
            output_file = f"conditional_access_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
        # Set up document
        self.pdf.set_font("Arial", "B", 16)
        self.pdf.cell(0, 10, "Conditional Access Policy Compliance Report", ln=True, align='C')
        self.pdf.ln(10)
        
        # Add timestamp
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        self.pdf.ln(10)
        
        # Add summary
        total_policies = len(policy_results)
        compliant_policies = len([r for r in policy_results if r['found']])
        
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 10, "Summary:", ln=True)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(0, 10, f"Total Required Policies: {total_policies}", ln=True)
        self.pdf.cell(0, 10, f"Compliant Policies: {compliant_policies}", ln=True)
        self.pdf.cell(0, 10, f"Missing Policies: {total_policies - compliant_policies}", ln=True)
        self.pdf.ln(10)
        
        # Add detailed results
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 10, "Detailed Results:", ln=True)
        self.pdf.ln(5)
        
        for result in policy_results:
            self.pdf.set_font("Arial", "B", 10)
            self.pdf.cell(0, 10, f"Policy: {result['requirement_name']}", ln=True)
            self.pdf.set_font("Arial", "", 10)
            # Replace emoji with text
            status = "PRESENT" if result['found'] else "MISSING"
            self.pdf.cell(0, 10, f"Status: {status}", ln=True)
            
            if result['matching_policies']:
                self.pdf.cell(0, 10, "Matching Policies:", ln=True)
                for policy in result['matching_policies']:
                    self.pdf.cell(0, 10, f"  - {policy}", ln=True)
            
            self.pdf.ln(5)
            
        # Save the report
        self.pdf.output(output_file)
        print(f"\nReport generated: {output_file}") 