"""
OpenAI API Tool
Uses OpenAI API for deep research and analysis
"""
import os
from typing import Optional, Dict, List
import pandas as pd
from openai import OpenAI


class OpenAIResearchTool:
    """Tool for conducting deep research using OpenAI API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the OpenAI Research Tool
        
        Args:
            api_key: OpenAI API key. If not provided, will use OPENAI_API_KEY env var
        """
        api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        self.client = OpenAI(api_key=api_key)
    
    def analyze_business(self, business_name: str, business_type: str, location: str, 
                        additional_context: str = "") -> Dict[str, str]:
        """
        Conduct deep research and analysis on a business
        
        Args:
            business_name: Name of the business
            business_type: Type/industry of the business
            location: Location of the business
            additional_context: Any additional context or specific questions
            
        Returns:
            Dictionary with analysis results
        """
        prompt = f"""
        Conduct a comprehensive business analysis for the following company:
        
        Business Name: {business_name}
        Industry/Type: {business_type}
        Location: {location}
        
        {f"Additional Context: {additional_context}" if additional_context else ""}
        
        Please provide a detailed analysis covering:
        1. Market Overview: Current state of the industry and market trends
        2. Competitive Landscape: Key competitors and market positioning
        3. Growth Opportunities: Potential areas for expansion and improvement
        4. Risk Factors: Potential challenges and threats
        5. Financial Considerations: Key financial metrics and considerations for acquisition
        6. Strategic Recommendations: Actionable recommendations for private equity investment
        
        Format the response in a structured way with clear sections.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Using GPT-4 for deep analysis
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert business analyst specializing in private equity due diligence and financial modeling. Provide comprehensive, data-driven insights."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            analysis = response.choices[0].message.content
            
            return {
                'business_name': business_name,
                'business_type': business_type,
                'location': location,
                'analysis': analysis,
                'model_used': response.model,
                'tokens_used': response.usage.total_tokens if response.usage else 0
            }
            
        except Exception as e:
            print(f"Error conducting OpenAI analysis: {e}")
            return {
                'business_name': business_name,
                'error': str(e)
            }
    
    def market_research(self, industry: str, region: str, specific_questions: List[str] = None) -> str:
        """
        Conduct market research for an industry in a specific region
        
        Args:
            industry: Industry to research
            region: Geographic region
            specific_questions: List of specific questions to address
            
        Returns:
            Research findings as a string
        """
        questions_text = ""
        if specific_questions:
            questions_text = "\n\nSpecifically address these questions:\n" + "\n".join(f"- {q}" for q in specific_questions)
        
        prompt = f"""
        Conduct comprehensive market research for:
        
        Industry: {industry}
        Region: {region}
        
        Provide insights on:
        1. Market Size and Growth Rate
        2. Key Market Trends
        3. Consumer Demographics and Behavior
        4. Regulatory Environment
        5. Technology and Innovation Trends
        6. Market Entry Barriers
        7. Investment Outlook
        {questions_text}
        
        Provide data-driven insights where possible.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a market research expert with deep knowledge of various industries and regional markets. Provide comprehensive, well-researched insights."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error conducting market research: {e}")
            return f"Error: {str(e)}"
    
    def financial_model_insights(self, business_data: Dict[str, any]) -> str:
        """
        Generate insights for financial modeling
        
        Args:
            business_data: Dictionary with business information (revenue, costs, etc.)
            
        Returns:
            Financial modeling insights
        """
        prompt = f"""
        Based on the following business data, provide financial modeling insights:
        
        {self._format_business_data(business_data)}
        
        Provide analysis on:
        1. Revenue projections and growth assumptions
        2. Cost structure analysis
        3. Key financial ratios and metrics
        4. Valuation considerations
        5. Cash flow projections
        6. ROI and IRR considerations for PE investment
        7. Exit strategy considerations
        
        Be specific and provide quantitative insights where possible.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a financial modeling expert specializing in private equity investments. Provide detailed, quantitative financial analysis."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=3000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating financial insights: {e}")
            return f"Error: {str(e)}"
    
    def _format_business_data(self, data: Dict) -> str:
        """Format business data for prompts"""
        formatted = []
        for key, value in data.items():
            formatted.append(f"{key}: {value}")
        return "\n".join(formatted)
    
    def export_to_file(self, content: str, filename: str, format: str = "txt") -> str:
        """
        Export research content to file
        
        Args:
            content: Content to export
            filename: Output filename (without extension)
            format: File format ('txt' or 'md')
            
        Returns:
            Path to the saved file
        """
        output_path = os.path.join('output', f"{filename}.{format}")
        os.makedirs('output', exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Research exported to {output_path}")
        return output_path
    
    def export_analysis_to_excel(self, analysis_dict: Dict, filename: str) -> str:
        """
        Export analysis to Excel format
        
        Args:
            analysis_dict: Dictionary with analysis results
            filename: Output filename
            
        Returns:
            Path to the saved file
        """
        output_path = os.path.join('output', filename)
        os.makedirs('output', exist_ok=True)
        
        # Create a summary DataFrame
        summary_data = {
            'Field': [],
            'Value': []
        }
        
        for key, value in analysis_dict.items():
            if key != 'analysis':
                summary_data['Field'].append(key)
                summary_data['Value'].append(str(value))
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Write summary
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Write full analysis
            if 'analysis' in analysis_dict:
                analysis_df = pd.DataFrame([{'Analysis': analysis_dict['analysis']}])
                analysis_df.to_excel(writer, sheet_name='Full Analysis', index=False)
        
        print(f"Analysis exported to {output_path}")
        return output_path


if __name__ == "__main__":
    # Example usage
    from dotenv import load_dotenv
    load_dotenv()
    
    tool = OpenAIResearchTool()
    
    # Example: Analyze a business
    analysis = tool.analyze_business(
        business_name="Big Y World Class Market",
        business_type="Grocery Store Chain",
        location="Western Massachusetts",
        additional_context="Considering for acquisition by a private equity firm"
    )
    
    print("\nBusiness Analysis:")
    print(analysis.get('analysis', analysis.get('error', 'No analysis available')))
    
    # Export results
    if 'analysis' in analysis:
        tool.export_to_file(analysis['analysis'], "business_analysis", format="md")
        tool.export_analysis_to_excel(analysis, "business_analysis.xlsx")
