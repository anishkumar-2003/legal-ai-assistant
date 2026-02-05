import re

def extract_clauses(text):
    pattern = r'(\n\d+\.?.*?)(?=\n\d+\.|\Z)'
    clauses = re.findall(pattern, text, re.S)
    return clauses
