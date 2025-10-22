# Examples

This directory contains example scripts demonstrating how to use the Valley Business Partners API Tools.

## Running the Examples

```bash
# From the project root directory
python examples/example_usage.py
```

## What's Included

### example_usage.py

Demonstrates basic usage of all four API tools:

1. **Google Reviews Example** - How to fetch and export customer reviews
2. **Competitors Example** - How to find competitors in a region
3. **OpenAI Research Example** - How to generate AI-powered business analysis
4. **SBA Loans Example** - How to get loan rates and eligibility information

Each example includes:
- Tool initialization
- Data fetching
- Data processing
- Export to Excel/CSV

## Customizing the Examples

Feel free to modify these examples for your specific use case:

```python
# Change the business being analyzed
business_name = "Your Business Name"
location = "Your Location"
business_type = "Your Business Type"

# Adjust search parameters
radius = 50000  # Search radius in meters
limit = 100     # Maximum results to return

# Customize analysis questions
specific_questions = [
    "What is the market size?",
    "Who are the competitors?",
    "What are growth opportunities?"
]
```

## Creating Your Own Scripts

Use these examples as templates for your own analysis scripts:

1. Copy an example file
2. Modify the parameters
3. Add your own analysis logic
4. Run and export results

Example custom script structure:
```python
from dotenv import load_dotenv
from src.tools.your_tool import YourTool

load_dotenv()

# Your custom analysis logic here
tool = YourTool()
results = tool.analyze(...)
tool.export_to_excel(results, "my_analysis.xlsx")
```

## Output

All example outputs are saved to the `output/` directory with prefixes like:
- `example_reviews.xlsx`
- `example_competitors.xlsx`
- `example_analysis.md`
- `example_sba_loans.xlsx`

## Notes

- Make sure your `.env` file is configured with API keys
- The SBA loans example works without API keys
- Google and OpenAI examples require valid API keys
- Review the main [README.md](../README.md) for API key setup instructions
