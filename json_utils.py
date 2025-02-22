import json
import re
def clean_json_output(llm_output: str) -> dict:
  try:
    # Remove line break escape characters (\)
    cleaned_output = re.sub(r'\\\n', ' ',llm_output)
    #Optionally, remove other unnecessary escape characters
    cleaned_output = re.sub(r'\\','', cleaned_output)
    return cleaned_output
  except json. JSONDecodeError as e:
    print(f"Failed to parse JSON: {e}")
    return None
