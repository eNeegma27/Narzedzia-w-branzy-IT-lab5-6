"""
Data Format Converter
Main program entry point.

Converts data between formats: .xml, .json, and .yaml
"""

import sys
from arg_parser import parse_arguments, print_usage
from data_reader import read_file, DataReaderError
from data_writer import write_file, DataWriterError, validate_json_syntax, validate_yaml_syntax


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
        
        # Read input file (Task 2, Task 4, Task 6)
        print(f"\n[Task 2-6] Reading input file...")
        try:
            data = read_file(args['input_file'], args['input_format'])
            format_name = args['input_format'].upper()
            print(f"✓ Successfully read {format_name} file")
            print(f"  Data type: {type(data).__name__}")
            if isinstance(data, dict):
                print(f"  Keys: {len(data)} keys found")
            elif isinstance(data, list):
                print(f"  Items: {len(data)} items found")
        except DataReaderError as e:
            print(f"✗ Error reading file: {e}")
            return 1
        
        # Write output file (Task 3, Task 5)
        print(f"\n[Task 3-5] Writing output file...")
        try:
            write_file(args['output_file'], data, args['output_format'])
            format_name = args['output_format'].upper()
            print(f"✓ Successfully wrote data to {format_name} file")
            
            # Verify syntax based on output format
            if args['output_format'] == 'json':
                validate_json_syntax(args['output_file'])
            elif args['output_format'] in ('yaml', 'yml'):
                validate_yaml_syntax(args['output_file'])
            
            print(f"✓ Output {format_name} syntax verified")
        except DataWriterError as e:
            print(f"✗ Error writing file: {e}")
            return 1
        
        print("\n" + "=" * 50)
        print("Task 1-6 completed successfully!")
        print("\nNext tasks will implement:")
        print("- Task 7: Writing XML files and format verification")
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
