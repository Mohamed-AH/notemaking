# Lecture Notes Generator for Claude Code

Automated system for converting Arabic lecture transcripts into comprehensive, professionally formatted notes using Claude Code (no API key needed!).

## Overview

This system transforms raw Arabic lecture transcripts (with English translations) into well-structured, bilingual markdown notes following strict formatting rules. It's designed specifically for Islamic scholarly lectures, particularly Sahih Al-Bukhari explanations.

**NEW**: Now works directly with Claude Code - no Anthropic API key required!

## Features

- **Claude Code Integration**: Uses Claude Code environment directly (no external API calls)
- **Bilingual Support**: Maintains both Arabic and English in structured format
- **Timestamp Preservation**: Ensures all timestamps from source appear in output
- **Quality Assurance**: Built-in validation checks for completeness and accuracy
- **Batch Processing**: Process multiple transcripts automatically
- **Comprehensive Coverage**: Captures every detail including digressions, Q&A, and side comments

## Directory Structure

```
notemaking/
├── source_transcripts/      # Input: Place your .txt transcript files here
├── outputs/                 # Output: Generated comprehensive notes
├── working/                 # Temporary: Segment files for processing
├── logs/                    # Quality check logs
├── agent/                   # Core processing code
│   ├── processor.py         # Main preparation logic
│   ├── quality_checker.py   # Validation system
│   ├── formatter.py         # Formatting rules
│   └── master_prompt.txt    # Processing template
├── batch_process.py         # Batch preparation script
├── process_segments.py      # Segment processing helper
├── process_helper.py        # Preparation and finalization helper
├── example_transcript.txt   # Example input format
├── idea.md                  # Detailed procedure documentation
└── README.md               # This file
```

## Prerequisites

1. **Python 3.8+**
2. **Claude Code** - This system is designed to work within Claude Code environment

## Installation

No installation needed! The system uses only Python standard library.

```bash
# Optional: Install in a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# No dependencies to install!
```

## Usage

The workflow has three main steps:

### Step 1: Prepare Transcripts

First, add your transcript files to `source_transcripts/` folder, then prepare them:

```bash
# Prepare all transcripts
python batch_process.py

# Or prepare a single transcript
python process_helper.py prepare source_transcripts/transcript_01.txt
```

This creates segment files in the `working/` directory. Each segment includes:
- `L##_PART#_segment.txt` - The transcript segment
- `L##_PART#_instructions.md` - Processing instructions
- `L##_PART#_output.md` - Where output should be written (you'll create this)

### Step 2: Process Segments with Claude Code

Now ask Claude Code to process each segment. You have two options:

**Option A: Ask Claude directly**
```
Ask Claude: "Please process all pending lecture segments in the working/ directory.
For each segment, read the instructions file and segment file, then create the
formatted output following the rules."
```

**Option B: Process segments one by one**
```
Ask Claude: "Please process Lecture 01 Part 1 - read working/L01_PART1_instructions.md
and working/L01_PART1_segment.txt, then create working/L01_PART1_output.md"
```

**Option C: Use the helper script**
```bash
python process_segments.py
# This lists all pending segments and their status
```

### Step 3: Finalize Lecture

Once all segments for a lecture are processed:

```bash
# Finalize lecture 01
python process_helper.py finalize 1

# This will:
# - Merge all processed segments
# - Run quality checks
# - Generate final comprehensive notes in outputs/
```

### Check Status

To see which segments are done and which are pending:

```bash
python process_helper.py list
```

## Input Format

Your transcript files should be in `.txt` format with:

- **Timestamps**: In format `(MM:SS)` or `(H:MM:SS)` or `(MM:SS-MM:SS)`
- **Language**: Mixed Arabic and English text
- **Structure**: Chapter markers, hadith numbers, speaker labels
- **Encoding**: UTF-8

Example:
```
(0:00) بسم الله الرحمن الرحيم

In the name of Allah, the Most Merciful, the Most Compassionate

(0:15) كتاب بدء الوحي | The Book of Revelation

(1:30) حَدَّثَنَا الْحُمَيْدِيُّ...
```

See `example_transcript.txt` for a complete example.

## Output Format

The system generates comprehensive markdown notes with:

- **Bilingual headers**: `## Arabic Title | English Title`
- **Preserved timestamps**: All timestamps from source
- **Structured hierarchy**: Proper markdown levels (# ## ### ####)
- **Complete content**: Every detail from the lecture
- **Quality validation**: Checked for completeness and accuracy

## Processing Pipeline

The system follows these phases:

1. **Preparation**: Extract structure, timestamps, create segments
2. **Processing**: Claude Code processes each segment following strict rules
3. **Merging**: Combine segments into comprehensive document
4. **Quality Check**: Validate timestamps, bilingual content, structure
5. **Output**: Save to destination folder with summary stats

## Quality Checks

The system validates:

- ✓ Timestamp coverage (all source timestamps present)
- ✓ Timestamp continuity (no large gaps)
- ✓ Bilingual completeness (all Arabic has English)
- ✓ Structure hierarchy (proper markdown levels)
- ✓ Arabic preservation (text unchanged)
- ✓ Formatting consistency (standardized patterns)

## Example Workflow

Complete example of processing one transcript:

```bash
# 1. Add transcript to source_transcripts/
cp my_lecture.txt source_transcripts/

# 2. Prepare it
python process_helper.py prepare source_transcripts/my_lecture.txt

# 3. Check what needs processing
python process_helper.py list

# 4. Ask Claude Code:
# "Please process all segments for Lecture 01 following the instructions"

# 5. After Claude processes all segments, finalize:
python process_helper.py finalize 1

# 6. Check the output
cat outputs/lecture_notes_L01_COMPREHENSIVE.md
```

## Troubleshooting

### "No transcript files found"
- Ensure `.txt` files are in `source_transcripts/` folder
- Check file permissions are readable

### "No segments found"
- Run `python batch_process.py` or `python process_helper.py prepare` first

### Quality check warnings
- Review the warnings in console output
- Check the specific timestamps or sections mentioned
- May need manual review for complex transcripts

### Segment not processed
- Check if output file exists in `working/` directory
- Ask Claude Code to process that specific segment
- Review the instruction file for formatting requirements

## Commands Reference

```bash
# Preparation
python batch_process.py                    # Prepare all transcripts
python process_helper.py prepare FILE      # Prepare one transcript
python process_helper.py prepare --all     # Prepare all in source_transcripts/

# Status
python process_helper.py list              # Show all segments and status
python process_segments.py                 # List pending segments

# Finalization
python process_helper.py finalize 1        # Finalize lecture 01
python process_helper.py finalize 2        # Finalize lecture 02
```

## Performance

- **Processing time**: Depends on Claude Code processing speed
- **No API costs**: Uses Claude Code environment directly
- **Output size**: Typically 5-10x larger than input transcript
- **Quality**: Publication-ready comprehensive notes

## Processing Rules

Each segment is processed following strict rules:

1. **Bilingual headers**: All headers have both Arabic and English
2. **Timestamp preservation**: Every timestamp from source must appear
3. **Zero additions**: Never add content not in source
4. **Complete capture**: Never skip any content from source
5. **Proper formatting**: Follow markdown hierarchy strictly
6. **Arabic preservation**: Keep all Arabic exactly as written
7. **Include everything**: Main content, digressions, Q&A, side comments

## Documentation

For detailed procedure documentation, see `idea.md` which contains:

- Complete processing procedure
- Formatting rules specification
- Quality checker details
- Edge case handling
- Agent architecture

## Example Output

From a 15-minute lecture transcript (500 words) → Comprehensive notes (2,500 words):

- All hadith captured with full isnad and matn
- Complete sheikh explanations paragraph-by-paragraph
- All student Q&A interactions preserved
- Digressions and side topics included
- Contemporary applications documented
- 100% timestamp coverage
- Consistent bilingual formatting throughout

## Support

For issues or questions:
1. Check `idea.md` for detailed documentation
2. Run `python process_helper.py list` to see segment status
3. Ask Claude Code for help processing specific segments

## Why Claude Code?

Using Claude Code instead of the Anthropic API provides several advantages:

- **No API key needed**: Works directly in Claude Code environment
- **No API costs**: Free to process as many transcripts as you want
- **Better context**: Claude Code has full access to files and project structure
- **Interactive**: Can review and adjust processing in real-time
- **Flexible**: Easy to modify rules and reprocess segments

## License

This project is designed for processing Islamic scholarly lecture transcripts.

## Credits

Based on the comprehensive procedure developed for Sahih Al-Bukhari lecture note generation.
