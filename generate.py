#!/usr/bin/env python3

import json

def generate_filter_rules(terms):
    # Header comments
    header = """# Block political related posts on HN. This leaves the comment section still since that's just another <tr>.
# HN then has two more <tr>s afterwards - one for the comment link and one for spacing
! Generated filter rules
"""

    # Escape any dots in terms and join with |
    escaped_terms = [term.replace('.', r'\.') for term in terms]
    regex_pattern = '|'.join(escaped_terms)

    # Base rule template
    base_rule = f'news.ycombinator.com##.submission:has-text(/\\b({regex_pattern})\\b/i)'
    comment_rule = f'news.ycombinator.com##.comment:has-text(/\\b({regex_pattern})\\b/i)'

    # Full set of rules including the tr selectors
    rules = [
        base_rule,
        f'{base_rule} + tr',
        f'{base_rule} + tr + tr',
        comment_rule,
    ]

    return header + '\n'.join(rules)

def main():
    # Read terms from JSON file
    try:
        with open('blocked_terms.json', 'r') as f:
            terms = json.load(f)

        if not isinstance(terms, list):
            raise ValueError("JSON file must contain an array of strings")

        # Generate and write rules
        rules = generate_filter_rules(terms)

        with open('filter.txt', 'w') as f:
            f.write(rules)

        print("Successfully generated filter.txt")

    except FileNotFoundError:
        print("Error: blocked_terms.json not found")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
