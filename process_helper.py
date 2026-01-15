#!/usr/bin/env python3
"""
Helper script for processing lecture segments
Works within Claude Code environment - no API key needed
"""

import os
import sys

# Add agent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agent'))

from processor import LectureNotesAgent


def prepare_transcript(transcript_file, agent):
    """Prepare a transcript for processing"""
    print(f"\n{'='*70}")
    print(f"PREPARING: {os.path.basename(transcript_file)}")
    print(f"{'='*70}\n")

    preparation = agent.prepare_lecture(transcript_file)

    print(f"\n✓ Preparation complete!")
    print(f"  Created {len(preparation['segment_files'])} segment files in working/")
    print(f"  Ready for processing\n")

    return preparation


def finalize_lecture(preparation, agent):
    """Finalize a lecture after all segments are processed"""
    print(f"\n{'='*70}")
    print(f"FINALIZING: Lecture {preparation['lecture_number']:02d}")
    print(f"{'='*70}\n")

    result = agent.finalize_lecture(preparation)

    return result


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Prepare and finalize lecture transcripts for Claude Code processing'
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Prepare command
    prepare_parser = subparsers.add_parser('prepare', help='Prepare transcript(s) for processing')
    prepare_parser.add_argument('transcript', nargs='?', help='Transcript file to prepare (optional)')
    prepare_parser.add_argument('--all', action='store_true', help='Prepare all transcripts in source_transcripts/')

    # Finalize command
    finalize_parser = subparsers.add_parser('finalize', help='Finalize processed lecture')
    finalize_parser.add_argument('lecture_num', type=int, help='Lecture number to finalize')

    # List command
    list_parser = subparsers.add_parser('list', help='List segments ready for processing')

    args = parser.parse_args()

    # Initialize agent
    agent = LectureNotesAgent(
        source_folder='source_transcripts',
        destination_folder='outputs',
        working_folder='working'
    )

    if args.command == 'prepare':
        if args.all:
            # Prepare all transcripts
            import glob
            transcripts = sorted(glob.glob('source_transcripts/*.txt'))
            if not transcripts:
                print("No transcript files found in source_transcripts/")
                return

            preparations = []
            for transcript in transcripts:
                prep = prepare_transcript(transcript, agent)
                preparations.append(prep)

            print(f"\n{'='*70}")
            print(f"SUMMARY: Prepared {len(preparations)} lectures")
            print(f"{'='*70}")
            for prep in preparations:
                print(f"  Lecture {prep['lecture_number']:02d}: {len(prep['segment_files'])} segments")
            print()

        elif args.transcript:
            # Prepare single transcript
            if not os.path.exists(args.transcript):
                print(f"Error: File not found: {args.transcript}")
                return
            prepare_transcript(args.transcript, agent)
        else:
            print("Error: Specify a transcript file or use --all")
            parser.print_help()

    elif args.command == 'finalize':
        # Find preparation data for this lecture
        import glob
        import json

        # Look for segment files
        segment_pattern = f"working/L{args.lecture_num:02d}_PART*_segment.txt"
        segments = glob.glob(segment_pattern)

        if not segments:
            print(f"Error: No segments found for lecture {args.lecture_num:02d}")
            print(f"Run 'python process_helper.py prepare' first")
            return

        # Reconstruct preparation data
        transcript_file = f"source_transcripts/corrected_{args.lecture_num}*.txt"
        transcript_matches = glob.glob(transcript_file)

        if not transcript_matches:
            print(f"Warning: Source transcript not found, using generic name")
            transcript_file = f"lecture_{args.lecture_num:02d}.txt"
        else:
            transcript_file = transcript_matches[0]

        # Build segment files list
        segment_files = []
        part_num = 1
        while True:
            seg_file = f"working/L{args.lecture_num:02d}_PART{part_num}_segment.txt"
            if not os.path.exists(seg_file):
                break

            segment_files.append({
                'part_number': part_num,
                'segment_file': seg_file,
                'instruction_file': f"working/L{args.lecture_num:02d}_PART{part_num}_instructions.md",
                'output_file': f"working/L{args.lecture_num:02d}_PART{part_num}_output.md"
            })
            part_num += 1

        # Quick analysis
        analysis = agent.analyze_transcript(transcript_file) if os.path.exists(transcript_file) else {'timestamp_ranges': []}

        preparation = {
            'transcript_file': transcript_file,
            'lecture_number': args.lecture_num,
            'segment_files': segment_files,
            'analysis': analysis
        }

        result = finalize_lecture(preparation, agent)

        print(f"\n✓ Lecture {args.lecture_num:02d} finalized successfully!")
        print(f"  Output: {result.output_path}")
        print()

    elif args.command == 'list':
        # List all pending segments
        import glob

        segments = glob.glob('working/*_segment.txt')
        if not segments:
            print("No segments found in working/")
            print("Run 'python process_helper.py prepare' first")
            return

        # Group by lecture
        lectures = {}
        for seg in segments:
            basename = os.path.basename(seg)
            # Extract L##_PART#
            import re
            match = re.match(r'L(\d+)_PART(\d+)_segment\.txt', basename)
            if match:
                lecture_num = int(match.group(1))
                part_num = int(match.group(2))

                if lecture_num not in lectures:
                    lectures[lecture_num] = []

                # Check if output exists
                output_file = f'working/L{lecture_num:02d}_PART{part_num}_output.md'
                status = '✓ Done' if os.path.exists(output_file) else '○ Pending'

                lectures[lecture_num].append({
                    'part': part_num,
                    'status': status,
                    'segment': seg,
                    'output': output_file
                })

        print("\n" + "="*70)
        print("SEGMENTS STATUS")
        print("="*70 + "\n")

        for lecture_num in sorted(lectures.keys()):
            parts = sorted(lectures[lecture_num], key=lambda x: x['part'])
            total = len(parts)
            done = sum(1 for p in parts if '✓' in p['status'])

            print(f"Lecture {lecture_num:02d}: {done}/{total} segments processed")
            for part_info in parts:
                print(f"  Part {part_info['part']}: {part_info['status']}")
            print()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
