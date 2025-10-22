# Quick Start Guide

Get started with Valley Business Partners API Tools in 5 minutes!

## 1. Installation

```bash
# Clone the repository
git clone https://github.com/Ivan-Sapozhnikov-github/ValleyBusinessPartnersAPIs.git
cd ValleyBusinessPartnersAPIs

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 2. Configure API Keys

```bash
# Copy the example config
cp config.example.env .env

# Edit .env and add your API keys
# Use your favorite text editor (nano, vim, vscode, etc.)
nano .env
```

Required API keys:
- **GOOGLE_API_KEY**: Get from [Google Cloud Console](https://console.cloud.google.com/)
- **OPENAI_API_KEY**: Get from [OpenAI Platform](https://platform.openai.com/)

## 3. Run the Application

```bash
python main.py
```

This launches the interactive menu where you can:
1. Run comprehensive business analysis (all tools at once)
2. Use individual tools separately
3. Export data to Excel/CSV

## 4. Example Workflow

### Analyzing a Potential Acquisition Target

1. Launch the application: `python main.py`
2. Select option `1` (Comprehensive Business Analysis)
3. Enter the business details:
   - Business name: "Big Y World Class Market"
   - Business type: "Grocery Store"
   - Location: "Springfield, MA"
4. Wait for all tools to complete (1-2 minutes)
5. Find your results in the `output/` directory

### Generated Files
```
output/
├── Big_Y_World_Class_Market_20241022_120000_reviews.xlsx
├── Big_Y_World_Class_Market_20241022_120000_competitors.xlsx
├── Big_Y_World_Class_Market_20241022_120000_analysis.md
├── Big_Y_World_Class_Market_20241022_120000_analysis.xlsx
└── Big_Y_World_Class_Market_20241022_120000_sba_loans.xlsx
```

## 5. Using Individual Tools

### Quick Google Reviews Check
```bash
python main.py
# Select option 2
# Enter business name
# Results exported to Excel
```

### Find Competitors Only
```bash
python main.py
# Select option 3
# Enter business type (e.g., "restaurant", "retail store")
# Enter location
# Results exported with competitive analysis
```

### AI Deep Research
```bash
python main.py
# Select option 4
# Enter business details
# Get comprehensive market analysis
```

### SBA Loans Information
```bash
python main.py
# Select option 5
# Choose from:
#   a. Current loan rates
#   b. Search loans by state
#   c. Historical rates
#   d. Analyze loan eligibility
```

## 6. Programmatic Usage

Create your own Python scripts:

```python
from src.tools.google_reviews import GoogleReviewsTool
from src.tools.competitors import CompetitorsTool
from src.tools.openai_research import OpenAIResearchTool
from src.tools.sba_loans import SBALoansTool

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Example: Quick competitor analysis
competitors = CompetitorsTool()
df = competitors.get_competitors_dataframe(
    business_type="grocery store",
    location="Western Massachusetts",
    radius=25000
)
competitors.export_to_excel(df, "my_analysis.xlsx")
print(f"Found {len(df)} competitors")
```

## Tips & Tricks

### Working with Excel Files
- All Excel exports include multiple sheets
- Summary sheets provide key metrics
- Use Excel's filters and pivot tables for deeper analysis

### Cost Management
- OpenAI API calls use tokens (costs money)
- Google API has free tier limits
- Use individual tools to control costs

### Best Practices
1. Start with free data (Google Reviews, SBA rates)
2. Use OpenAI for final deep analysis
3. Export everything to Excel for financial modeling
4. Combine data from all tools for comprehensive due diligence

## Troubleshooting

### "API key is required" Error
- Check that `.env` file exists
- Verify API keys are correctly entered
- No quotes needed around keys in `.env` file

### No Results Found
- Try different business names or locations
- Verify the business exists on Google Maps
- Use broader search terms

### Network Errors
- Check internet connection
- Verify API keys are valid
- Some APIs have rate limits

## Next Steps

1. ✅ Run your first analysis
2. 📊 Open results in Excel
3. 🔍 Combine with your financial models
4. 📈 Make data-driven investment decisions

## Support

For questions or issues:
- Check the main [README.md](README.md) for detailed documentation
- Review error messages carefully
- Contact your technical team for help

---

**Ready to analyze your first business?** Run `python main.py` now!
