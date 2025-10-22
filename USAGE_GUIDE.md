# Usage Guide

Comprehensive guide for using Valley Business Partners API Tools in your due diligence workflow.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Use Cases](#use-cases)
3. [Tool-by-Tool Guide](#tool-by-tool-guide)
4. [Workflow Examples](#workflow-examples)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

## Quick Start

### First Time Setup
```bash
# 1. Run setup script
./setup.sh  # Linux/Mac
# or
setup.bat   # Windows

# 2. Add your API keys to .env
nano .env

# 3. Test installation
python test_installation.py

# 4. Run the application
python main.py
```

### Daily Usage
```bash
# Activate environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate.bat  # Windows

# Run the tool
python main.py

# When done
deactivate
```

## Use Cases

### 1. Pre-Acquisition Due Diligence

**Scenario:** Evaluating a local grocery store chain for potential acquisition.

**Workflow:**
1. Run comprehensive analysis (Option 1 in main menu)
2. Review customer sentiment from Google Reviews
3. Analyze competitive landscape
4. Get AI-powered market analysis
5. Review SBA loan options for financing

**Output:** Complete due diligence package in Excel format ready for financial modeling.

### 2. Market Research

**Scenario:** Understanding the competitive landscape in Western Massachusetts retail.

**Workflow:**
1. Use Competitors Tool (Option 3)
2. Search for "retail store" in specific locations
3. Expand radius to cover entire region
4. Export to Excel
5. Use OpenAI tool for industry analysis

**Output:** Competitive intelligence report with market insights.

### 3. Customer Sentiment Analysis

**Scenario:** Assessing customer satisfaction for a target business.

**Workflow:**
1. Use Google Reviews Tool (Option 2)
2. Pull reviews for target business
3. Analyze ratings and feedback
4. Compare with competitors' reviews
5. Use OpenAI for sentiment synthesis

**Output:** Customer sentiment report with actionable insights.

### 4. Financing Analysis

**Scenario:** Determining optimal SBA loan structure for an acquisition.

**Workflow:**
1. Use SBA Loans Tool (Option 5)
2. Get current loan rates
3. Analyze eligibility based on business metrics
4. Review historical rate trends
5. Compare different loan programs

**Output:** Financing options analysis for investment committee.

## Tool-by-Tool Guide

### Google Reviews Tool

**What it does:**
- Fetches Google reviews for any business
- Provides overall ratings and statistics
- Includes business contact information

**When to use:**
- Customer sentiment analysis
- Reputation assessment
- Quality of service evaluation

**Example:**
```python
from src.tools.google_reviews import GoogleReviewsTool

tool = GoogleReviewsTool()
reviews_df = tool.get_reviews("Business Name", "Location")
tool.export_to_excel(reviews_df, "reviews.xlsx")
```

**Output includes:**
- Individual reviews with ratings
- Overall business rating
- Total number of reviews
- Business address and contact info

### Competitors Tool

**What it does:**
- Finds competitors in a specified region
- Provides ratings and review counts
- Includes business types and locations

**When to use:**
- Market landscape analysis
- Competitive positioning
- Benchmarking opportunities

**Example:**
```python
from src.tools.competitors import CompetitorsTool

tool = CompetitorsTool()
competitors_df = tool.get_competitors_dataframe(
    business_type="restaurant",
    location="Springfield, MA",
    radius=25000  # 25km
)
tool.export_to_excel(competitors_df, "competitors.xlsx")
```

**Output includes:**
- Competitor names and addresses
- Ratings and review counts
- Business types
- Operational status

### OpenAI Research Tool

**What it does:**
- Generates comprehensive business analysis using GPT-4
- Conducts market research
- Provides strategic recommendations

**When to use:**
- Deep market analysis
- Strategic planning
- Investment thesis development

**Example:**
```python
from src.tools.openai_research import OpenAIResearchTool

tool = OpenAIResearchTool()
analysis = tool.analyze_business(
    business_name="Business Name",
    business_type="Industry",
    location="Location",
    additional_context="Specific questions or context"
)
tool.export_to_file(analysis['analysis'], "analysis", format="md")
```

**Output includes:**
- Market overview and trends
- Competitive landscape
- Growth opportunities
- Risk factors
- Financial considerations
- Strategic recommendations

### SBA Loans Tool

**What it does:**
- Provides current SBA loan rates
- Shows historical rate trends
- Analyzes loan eligibility
- Compares different loan programs

**When to use:**
- Financing structuring
- Cost of capital analysis
- Loan eligibility assessment

**Example:**
```python
from src.tools.sba_loans import SBALoansTool

tool = SBALoansTool()

# Get rates
rates_df = tool.get_loan_rates()

# Analyze eligibility
eligibility = tool.analyze_loan_eligibility({
    'annual_revenue': 5_000_000,
    'employees': 25,
    'years_in_business': 5,
    'credit_score': 720
})

tool.export_to_excel({
    'Rates': rates_df
}, "sba_analysis.xlsx")
```

**Output includes:**
- 7(a) loan rates and terms
- 504 loan rates and terms
- Microloan information
- Express loan options
- Eligibility recommendations

## Workflow Examples

### Example 1: Restaurant Acquisition in Springfield, MA

```python
from dotenv import load_dotenv
from src.tools.google_reviews import GoogleReviewsTool
from src.tools.competitors import CompetitorsTool
from src.tools.openai_research import OpenAIResearchTool
from src.tools.sba_loans import SBALoansTool

load_dotenv()

# Target business
target = "The Student Prince"
location = "Springfield, MA"
business_type = "restaurant"

# 1. Get reviews
reviews_tool = GoogleReviewsTool()
reviews = reviews_tool.get_reviews(target, location)
reviews_tool.export_to_excel(reviews, "student_prince_reviews.xlsx")

# 2. Find competitors
competitors_tool = CompetitorsTool()
competitors = competitors_tool.get_competitors_dataframe(
    business_type=business_type,
    location=location,
    radius=10000
)
competitors_tool.export_to_excel(competitors, "springfield_restaurants.xlsx")

# 3. AI analysis
openai_tool = OpenAIResearchTool()
analysis = openai_tool.analyze_business(
    business_name=target,
    business_type="German Restaurant",
    location=location,
    additional_context="Historic restaurant, family business, potential acquisition"
)
openai_tool.export_to_file(analysis['analysis'], "student_prince_analysis", "md")

# 4. SBA loans
sba_tool = SBALoansTool()
rates = sba_tool.get_loan_rates()
eligibility = sba_tool.analyze_loan_eligibility({
    'annual_revenue': 2_000_000,
    'employees': 15,
    'years_in_business': 80,
    'credit_score': 750
})
sba_tool.export_to_excel({
    'Rates': rates
}, "financing_options.xlsx")

print("Due diligence package complete!")
```

### Example 2: Multi-Location Retail Chain Analysis

```python
locations = [
    "Springfield, MA",
    "Northampton, MA",
    "Amherst, MA"
]

competitors_tool = CompetitorsTool()

for location in locations:
    print(f"\nAnalyzing {location}...")
    
    competitors = competitors_tool.get_competitors_dataframe(
        business_type="retail store",
        location=location,
        radius=15000
    )
    
    filename = f"competitors_{location.replace(', ', '_').replace(' ', '_')}.xlsx"
    competitors_tool.export_to_excel(competitors, filename)
    
    print(f"Found {len(competitors)} competitors")
    print(f"Saved to output/{filename}")

print("\nRegional analysis complete!")
```

## Best Practices

### API Usage

1. **Rate Limiting**
   - Google Places API: 100 requests per second
   - OpenAI API: Depends on your tier
   - Be mindful of costs

2. **Cost Management**
   - Start with free tools (SBA, Google Reviews)
   - Use OpenAI strategically for final analysis
   - Cache results to avoid repeated API calls

3. **Data Quality**
   - Verify business names and locations
   - Use specific search terms
   - Cross-reference data from multiple sources

### Workflow Optimization

1. **Batch Processing**
   ```python
   # Analyze multiple businesses at once
   businesses = [
       ("Business 1", "Location 1"),
       ("Business 2", "Location 2"),
   ]
   
   for name, location in businesses:
       # Run analysis
       pass
   ```

2. **Incremental Analysis**
   - Start with free data collection
   - Review preliminary results
   - Use paid APIs for promising opportunities

3. **Output Organization**
   ```
   output/
   ├── deal_name/
   │   ├── reviews.xlsx
   │   ├── competitors.xlsx
   │   ├── analysis.md
   │   └── sba_loans.xlsx
   ```

### Data Integration

1. **Excel Integration**
   - All tools export to Excel
   - Use pivot tables for analysis
   - Integrate with financial models

2. **Report Generation**
   - Combine outputs from all tools
   - Create executive summaries
   - Build due diligence binders

## Troubleshooting

### Common Issues

**"API key is required"**
```bash
# Solution:
cp config.example.env .env
nano .env  # Add your API keys
```

**"No reviews found"**
- Verify business name is correct
- Check business exists on Google Maps
- Try different search terms

**"Network timeout"**
- Check internet connection
- Try again later
- Reduce search radius

**OpenAI rate limits**
- Wait a few seconds between requests
- Check your usage limits
- Upgrade your OpenAI plan if needed

### Getting Help

1. Check error messages carefully
2. Review the README.md
3. Look at example scripts
4. Test with test_installation.py
5. Contact your technical team

## Tips for Success

1. **Start Small**
   - Test with one business first
   - Verify outputs are correct
   - Scale up gradually

2. **Document Your Process**
   - Keep notes on searches performed
   - Track API usage and costs
   - Record insights and findings

3. **Integrate with Existing Tools**
   - Export to Excel for financial modeling
   - Combine with proprietary data
   - Share results with team

4. **Stay Updated**
   - APIs change over time
   - Keep dependencies updated
   - Review documentation regularly

## Advanced Usage

### Custom Scripts

Create your own scripts for specific workflows:

```python
# custom_analysis.py
from src.tools import *

def analyze_acquisition_target(business_name, location):
    """Custom analysis for acquisition targets"""
    # Your custom logic here
    pass

if __name__ == "__main__":
    analyze_acquisition_target("Target Business", "Location")
```

### Automated Reporting

```python
# Generate PDF reports
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_report(data):
    """Create PDF report from analysis data"""
    # Your reporting logic here
    pass
```

### Integration with Other Tools

```python
# Export to Google Sheets
import gspread

def upload_to_sheets(df, spreadsheet_name):
    """Upload DataFrame to Google Sheets"""
    # Your integration logic here
    pass
```

---

## Need More Help?

- 📖 See [README.md](README.md) for full documentation
- 🚀 See [QUICKSTART.md](QUICKSTART.md) for quick start
- 💻 See [examples/](examples/) for code examples
- 🧪 Run `python test_installation.py` to verify setup

**Happy analyzing!** 🎉
