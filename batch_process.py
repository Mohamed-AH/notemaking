#!/usr/bin/env python3
"""
Automated batch processor using Claude Code
No API key needed - uses Claude Code agents for processing
"""

import os
import sys
import glob
from pathlib import Path
from datetime import datetime

# Add agent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agent'))

from processor import LectureNotesAgent


def process_lecture_automated(transcript_file, agent):
    """
    Process a complete lecture using Claude Code
    This prepares segments that need to be processed by Claude Code
    """
    print(f"\n{'='*70}")
    print(f"Processing: {os.path.basename(transcript_file)}")
    print(f"{'='*70}\n")

    # Step 1: Prepare lecture (create segment files)
    preparation = agent.prepare_lecture(transcript_file)

    print(f"\n{'='*70}")
    print(f"PREPARATION COMPLETE")
    print(f"{'='*70}")
    print(f"Created {len(preparation['segment_files'])} segments")
    print(f"Segments are in: working/")
    print()

    return preparation


def batch_process_lectures(source_folder='source_transcripts', destination_folder='outputs'):
    """Prepare all transcripts for processing"""

    # Initialize agent
    agent = LectureNotesAgent(source_folder, destination_folder, 'working')

    # Get all transcript files
    transcript_files = sorted(glob.glob(f"{source_folder}/*.txt"))

    if not transcript_files:
        print(f"No transcript files found in {source_folder}/")
        print("Please add .txt transcript files to the source_transcripts folder")
        return []

    print(f"Found {len(transcript_files)} transcripts to process")
    print("="*70)

    preparations = []

    for i, transcript_file in enumerate(transcript_files, 1):
        try:
            preparation = process_lecture_automated(transcript_file, agent)
            preparations.append({
                'file': transcript_file,
                'status': 'PREPARED',
                'lecture_num': preparation['lecture_number'],
                'segments': len(preparation['segment_files'])
            })
        except Exception as e:
            preparations.append({
                'file': transcript_file,
                'status': 'FAILED',
                'error': str(e)
            })
            print(f"\n✗ Failed to prepare {os.path.basename(transcript_file)}: {e}")

    # Generate summary
    print(f"\n{'='*70}")
    print("PREPARATION SUMMARY")
    print(f"{'='*70}\n")

    for prep in preparations:
        if prep['status'] == 'PREPARED':
            print(f"✓ Lecture {prep['lecture_num']:02d}: {prep['segments']} segments prepared")
        else:
            print(f"✗ {os.path.basename(prep['file'])}: Failed")

    print(f"\n{'='*70}")
    print("NEXT STEPS")
    print(f"{'='*70}")
    print("\nSegments are ready in working/ directory.")
    print("\nTo process segments with Claude Code:")
    print("  1. Ask Claude to process each segment following the instructions")
    print("  2. Or use: python process_segments.py")
    print("\nTo finalize a lecture after processing:")
    print("  python process_helper.py finalize <lecture_number>")
    print()

    return preparations


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Batch prepare lecture transcripts for Claude Code processing'
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

    args = parser.parse_args()

    # Resolve paths
    source_folder = os.path.abspath(args.source)
    output_folder = os.path.abspath(args.output)

    print("Lecture Notes Batch Processor (Claude Code)")
    print("="*70)
    print(f"Source folder: {source_folder}")
    print(f"Output folder: {output_folder}")
    print("="*70)

    # Create folders if they don't exist
    os.makedirs(source_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs('working', exist_ok=True)

    # Process all lectures
    batch_process_lectures(source_folder, output_folder)


if __name__ == "__main__":
    main()
