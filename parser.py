import argparse
from exceptions import ParserError, InvalidField
def field_splitter(cron_str):
    """
    Splits the cron string into its components.
    """
    parts = cron_str.strip().split()
    if len(parts) < 6:
        raise ParserError("Cron string must contain at least 5 fields and a command.")
    return parts[:5], ' '.join(parts[5:])

def simplify_field(field_str, min_val, max_val):
    """
    Expands a cron field string into a list of valid integers.
    Handles '*', ranges (e.g. '1-5'), steps (e.g. '*/10'), and comma-separated lists.
    Raises InvalidField for invalid formats or out-of-bounds values.
    :param field_str: The cron field string to simplify.
    :param min_val: Minimum valid value for the field.
    :param max_val: Maximum valid value for the field.
    """
    values = set()

    for part in field_str.split(','):
        part = part.strip()
        if not part:
            raise InvalidField(f"Empty field part")
        if part == '*':
            values.update(range(min_val, max_val + 1))

        elif part.startswith('*/'):
            try:
                jump = int(part[2:])
                if jump <= 0:
                    raise ValueError
            except ValueError:
                raise InvalidField(f"Invalid jump value. Expected a positive integer after '*/'.")
            values.update(range(min_val, max_val + 1, jump))

        elif '-' in part:
            try:
                start, end = map(int, part.split('-'))
                if start > end:
                    raise InvalidField(f"Invalid range '{part}'. Start must be less than or equal to end.")
                
                if start < min_val or end > max_val:
                    raise InvalidField(f"Range '{part}' is out of bounds.")
            except ValueError:
                raise InvalidField(f"Invalid range format '{part}'. Expected 'start-end'.")
            
            values.update(range(start, end + 1))

        else:
            try:
                value = int(part)
                if value < min_val or value > max_val:
                    raise InvalidField(f"Value '{part}' is out of bounds.")
            except ValueError:
                raise InvalidField(f"Invalid value '{part}'. Expected an integer.")
            values.add(value)

    return sorted(values)

def parse_exp(cron_str):
    """    Parses a full cron expression string into its components.
    :param cron_str: The cron expression string to parse.
    :return: A dictionary with keys for each field and the command.
    """
    field_info = [
        ("minute", 0, 59),
        ("hour", 0, 23),
        ("day of month", 1, 31),
        ("month", 1, 12),
        ("day of week", 0, 6)
    ]
    fields, command = field_splitter(cron_str)
    parsed_expression = {}
    for i, (name, min_val, max_val) in enumerate(field_info):
        parsed_expression[name] = simplify_field(fields[i], min_val, max_val)
    parsed_expression["command"] = command
    return parsed_expression

def output_format(parsed_expression):
    """    Formats the parsed cron expression into a readable table.
    """
    rows = []
    for time in ["minute", "hour", "day of month", "month", "day of week"]:
        rows.append(f"{time:14} {' '.join(map(str, parsed_expression[time]))}")
    rows.append(f"{'command':14} {parsed_expression['command']}")
    return '\n'.join(rows)

def main():
    """Main function to run the cron parser with CLI arguments."""
    parser = argparse.ArgumentParser(
        description='Parse a cron expression and display it in a table format.'
    )
    parser.add_argument(
        'expression',
        type=str,
        help='Cron expression (e.g., "*/15 0 1,15 * 1-5 /usr/bin/find")'
    )
    
    args = parser.parse_args()
    cron_str = args.expression
    try:
        parsed_expression = parse_exp(cron_str)
        print(output_format(parsed_expression))
    except ParserError as e:
        print(f"Error: {e}")    

if __name__ == "__main__":
    main()  
