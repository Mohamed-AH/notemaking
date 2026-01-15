#!/usr/bin/env python3
"""
Batch processor for converting all lecture transcripts
to comprehensive formatted notes.
"""

import os
import sys
import glob
import argparse
from pathlib import Path
from datetime import datetime

# Add agent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agent'))

from processor import LectureNotesAgent


def batch_process_lectures(source_folder, destination_folder, api_key=None):
    """Process all transcripts in source folder"""

    # Initialize agent
    agent = LectureNotesAgent(source_folder, destination_folder, api_key)

    # Get all transcript files
    transcript_files = sorted(glob.glob(f"{source_folder}/*.txt"))

    if not transcript_files:
        print(f"No transcript files found in {source_folder}")
        print("Please add .txt transcript files to the source_transcripts folder")
        return []

    print(f"Found {len(transcript_files)} transcripts to process")
    print("=" * 70)

    results = []

    for i, transcript_file in enumerate(transcript_files, 1):
        print(f"\n{'=' * 70}")
        print(f"Processing {i}/{len(transcript_files)}: {os.path.basename(transcript_file)}")
        print(f"{'=' * 70}\n")

        try:
            # Process single lecture
            result = agent.process_lecture(transcript_file)

            # Log success
            results.append({
                'file': transcript_file,
                'status': 'SUCCESS',
                'output': result.output_path,
                'word_count': result.word_count,
                'timestamp_coverage': result.timestamp_coverage,
                'quality_score': result.quality_score
            })

            print(f"\n✓ Successfully processed {os.path.basename(transcript_file)}")

        except Exception as e:
            # Log failure
            results.append({
                'file': transcript_file,
                'status': 'FAILED',
                'error': str(e)
            })

            print(f"\n✗ Failed to process {os.path.basename(transcript_file)}: {e}")

    # Generate summary report
    print(f"\n{'=' * 70}")
    print("Processing Complete - Generating Report")
    print(f"{'=' * 70}\n")
    generate_summary_report(results, destination_folder)

    return results


def generate_summary_report(results, output_folder):
    """Create summary report of batch processing"""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_path = os.path.join(output_folder, "PROCESSING_REPORT.md")

    os.makedirs(output_folder, exist_ok=True)

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Batch Processing Report\n\n")
        f.write(f"Generated: {timestamp}\n\n")

        # Summary statistics
        total = len(results)
        successful = sum(1 for r in results if r['status'] == 'SUCCESS')
        failed = total - successful

        f.write(f"## Summary\n\n")
        f.write(f"- Total files: {total}\n")
        f.write(f"- Successful: {successful}\n")
        f.write(f"- Failed: {failed}\n")

        if total > 0:
            f.write(f"- Success rate: {successful / total * 100:.1f}%\n\n")

        # Detailed results
        f.write(f"## Detailed Results\n\n")

        for result in results:
            f.write(f"### {os.path.basename(result['file'])}\n\n")
            f.write(f"- Status: {result['status']}\n")

            if result['status'] == 'SUCCESS':
                f.write(f"- Output: `{result['output']}`\n")
                f.write(f"- Word count: {result['word_count']}\n")
                f.write(f"- Timestamp coverage: {result['timestamp_coverage']:.1f}%\n")
                f.write(f"- Quality score: {result['quality_score']:.1f}/100\n")
            else:
                f.write(f"- Error: {result['error']}\n")

            f.write("\n")

    print(f"Summary report generated: {report_path}")

    # Print summary to console
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total files: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    if total > 0:
        print(f"Success rate: {successful / total * 100:.1f}%")
    print("=" * 70)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Batch process lecture transcripts into comprehensive notes'
    )
    parser.add_argument(
        '--source',
        default='source_transcripts',
        help='Source folder containing transcript files (default: source_transcripts)'
    )
    parser.add_argument(
        '--output',
        default='outputs',
        help='Destination folder for output files (default: outputs)'
    )
    parser.add_argument(
        '--api-key',
        help='Anthropic API key (or set ANTHROPIC_API_KEY environment variable)'
    )

    args = parser.parse_args()

    # Check for API key
    api_key = args.api_key or os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: No API key provided!")
        print("Please either:")
        print("  1. Set ANTHROPIC_API_KEY environment variable")
        print("  2. Use --api-key argument")
        sys.exit(1)

    # Resolve paths
    source_folder = os.path.abspath(args.source)
    output_folder = os.path.abspath(args.output)

    print("Lecture Notes Batch Processor")
    print("=" * 70)
    print(f"Source folder: {source_folder}")
    print(f"Output folder: {output_folder}")
    print("=" * 70)

    # Create folders if they don't exist
    os.makedirs(source_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    # Process all lectures
    batch_process_lectures(source_folder, output_folder, api_key)


if __name__ == "__main__":
    main()
