#!/usr/bin/env python3
"""
Process all prepared segments
This script should be run within Claude Code environment
"""

import os
import glob
import re


def find_pending_segments():
    """Find all segments that haven't been processed yet"""
    segments = glob.glob('working/*_segment.txt')
    pending = []

    for seg_file in sorted(segments):
        basename = os.path.basename(seg_file)
        match = re.match(r'L(\d+)_PART(\d+)_segment\.txt', basename)

        if match:
            lecture_num = int(match.group(1))
            part_num = int(match.group(2))

            output_file = f'working/L{lecture_num:02d}_PART{part_num}_output.md'
            instruction_file = f'working/L{lecture_num:02d}_PART{part_num}_instructions.md'

            if not os.path.exists(output_file):
                pending.append({
                    'lecture_num': lecture_num,
                    'part_num': part_num,
                    'segment_file': seg_file,
                    'instruction_file': instruction_file,
                    'output_file': output_file
                })

    return pending


def process_segment(segment_info):
    """
    Process a single segment - reads instructions and segment, outputs formatted notes
    This is meant to be called by Claude Code
    """
    print(f"\n{'='*70}")
    print(f"Processing Lecture {segment_info['lecture_num']:02d} - Part {segment_info['part_num']}")
    print(f"{'='*70}\n")

    # Read instruction file
    with open(segment_info['instruction_file'], 'r', encoding='utf-8') as f:
        instructions = f.read()

    print("Instructions loaded.")

    # Read segment file
    with open(segment_info['segment_file'], 'r', encoding='utf-8') as f:
        segment_content = f.read()

    print(f"Segment loaded: {len(segment_content)} characters")
    print("\nThis segment should now be processed according to the instructions.")
    print(f"Output should be written to: {segment_info['output_file']}")
    print("\n" + "="*70)

    return {
        'instructions': instructions,
        'segment': segment_content,
        'output_path': segment_info['output_file']
    }


def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("SEGMENT PROCESSOR")
    print("="*70)

    pending = find_pending_segments()

    if not pending:
        print("\n✓ No pending segments found!")
        print("All segments have been processed.\n")
        print("To finalize lectures, use:")
        print("  python process_helper.py finalize <lecture_number>")
        return

    print(f"\nFound {len(pending)} segments to process:\n")

    # Group by lecture
    by_lecture = {}
    for seg in pending:
        lnum = seg['lecture_num']
        if lnum not in by_lecture:
            by_lecture[lnum] = []
        by_lecture[lnum].append(seg)

    for lecture_num in sorted(by_lecture.keys()):
        parts = by_lecture[lecture_num]
        print(f"  Lecture {lecture_num:02d}: {len(parts)} parts")

    print("\n" + "="*70)
    print("PROCESSING INSTRUCTIONS")
    print("="*70)
    print("""
These segments need to be processed by Claude Code.

For each segment:
1. Read the instruction file (*_instructions.md)
2. Read the segment file (*_segment.txt)
3. Process the Arabic transcript following the formatting rules
4. Write output to the output file (*_output.md)

You can either:
  a) Ask Claude Code to process each segment one by one
  b) Process them all at once if you provide this list to Claude Code

Segment list:
""")

    for seg in pending:
        print(f"  - Lecture {seg['lecture_num']:02d}, Part {seg['part_num']}")
        print(f"    Input: {seg['segment_file']}")
        print(f"    Instructions: {seg['instruction_file']}")
        print(f"    Output: {seg['output_file']}")
        print()

    print("="*70)


if __name__ == "__main__":
    main()
