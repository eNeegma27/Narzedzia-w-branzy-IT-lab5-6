"""
Data Format Converter
Main program entry point.

Converts data between formats: .xml, .json, and .yaml
"""

import sys
from arg_parser import parse_arguments, print_usage


def main():
    """Main program entry point."""
    try:
        # Parse and validate arguments (Task 1)
        args = parse_arguments()
        
        print("Data Format Converter")
        print("=" * 50)
        print(f"Input file:  {args['input_file']} ({args['input_format'].upper()})")
        print(f"Output file: {args['output_file']} ({args['output_format'].upper()})")
        print("=" * 50)
        print("\nTask 1 completed: Arguments parsed successfully!")
        print("\nNext tasks will implement:")
        print("- Task 2: Reading data from input file")
        print("- Task 3: Converting between formats")
        print("- Task 4: Writing output to file")
        print("- Task 5-7: Format verification")
        print("- Task 8-9: UI implementation")
        
        return 0
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("\n" + "=" * 50)
        print_usage()
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
