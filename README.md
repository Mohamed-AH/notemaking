# Lecture Notes Generator

Automated system for converting Arabic lecture transcripts into comprehensive, professionally formatted notes using Claude AI.

## Overview

This system transforms raw Arabic lecture transcripts (with English translations) into well-structured, bilingual markdown notes following strict formatting rules. It's designed specifically for Islamic scholarly lectures, particularly Sahih Al-Bukhari explanations.

## Features

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
├── working/                 # Temporary: Intermediate processing files
├── logs/                    # Quality check logs
├── agent/                   # Core processing code
│   ├── processor.py         # Main agent logic
│   ├── quality_checker.py   # Validation system
│   ├── formatter.py         # Formatting rules
│   └── master_prompt.txt    # Claude prompt template
├── batch_process.py         # Batch processing script
├── requirements.txt         # Python dependencies
├── idea.md                  # Detailed procedure documentation
└── README.md               # This file
```

## Prerequisites

1. **Python 3.8+**
2. **Anthropic API Key** - Get one from https://console.anthropic.com/

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Anthropic API key:
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

Or on Windows:
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

## Usage

### Single File Processing

To process a single transcript file:

```python
from agent.processor import LectureNotesAgent

# Initialize the agent
agent = LectureNotesAgent(
    source_folder='source_transcripts',
    destination_folder='outputs'
)

# Process a single file
result = agent.process_lecture('source_transcripts/transcript_01.txt')

print(f"Output: {result.output_path}")
print(f"Words: {result.word_count}")
print(f"Quality: {result.quality_score}")
```

### Batch Processing

To process all transcript files in the source folder:

```bash
python batch_process.py
```

With custom folders:
```bash
python batch_process.py --source /path/to/transcripts --output /path/to/outputs
```

With API key as argument:
```bash
python batch_process.py --api-key your-api-key-here
```

## Input Format

Your transcript files should be in `.txt` format with the following characteristics:

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

## Output Format

The system generates comprehensive markdown notes with:

- **Bilingual headers**: `## Arabic Title | English Title`
- **Preserved timestamps**: All timestamps from source
- **Structured hierarchy**: Proper markdown levels (# ## ### ####)
- **Complete content**: Every detail from the lecture
- **Quality validation**: Checked for completeness and accuracy

## Processing Pipeline

The system follows these phases:

1. **Analysis**: Extract structure, timestamps, chapters, hadith numbers
2. **Planning**: Divide into optimal segments for processing
3. **Execution**: Process each segment using Claude AI
4. **Merge**: Combine segments into comprehensive document
5. **Quality Check**: Validate timestamps, bilingual content, structure
6. **Output**: Save to destination folder with summary stats

## Quality Checks

The system validates:

- ✓ Timestamp coverage (all source timestamps present)
- ✓ Timestamp continuity (no large gaps)
- ✓ Bilingual completeness (all Arabic has English)
- ✓ Structure hierarchy (proper markdown levels)
- ✓ Arabic preservation (text unchanged)
- ✓ Formatting consistency (standardized patterns)

## Configuration

### Adjusting Segment Size

Edit `processor.py` line 94:
```python
max_chars_per_segment = 15000  # Adjust as needed
```

### Modifying Prompts

Edit `agent/master_prompt.txt` to customize Claude's behavior

### Changing Model

Edit `processor.py` line 122:
```python
model="claude-sonnet-4-5-20250929"  # Change model as needed
```

## Troubleshooting

### "No API key provided"
- Set the `ANTHROPIC_API_KEY` environment variable
- Or use `--api-key` argument when running

### "No transcript files found"
- Ensure `.txt` files are in `source_transcripts/` folder
- Check file permissions are readable

### Quality check warnings
- Review the generated `PROCESSING_REPORT.md` in outputs folder
- Check logs for specific issues
- May need manual review for complex transcripts

### Processing errors
- Ensure transcript is UTF-8 encoded
- Check for malformed timestamps
- Verify Arabic text displays correctly

## Performance

- **Processing time**: ~2-5 minutes per hour of lecture
- **Token usage**: ~10-30k tokens per lecture hour
- **Output size**: Typically 5-10x larger than input transcript
- **Quality**: Publication-ready comprehensive notes

## Batch Processing Report

After batch processing, check `outputs/PROCESSING_REPORT.md` for:

- Success/failure summary
- Per-file statistics (word count, coverage, quality score)
- Error details for failed files

## Example Output

From a 69-minute lecture transcript (1,500 words) → Comprehensive notes (8,100 words):

- All 30 hadith captured with full isnad and matn
- Complete sheikh explanations paragraph-by-paragraph
- All student Q&A interactions preserved
- Digressions and side topics included
- Contemporary applications documented
- 100% timestamp coverage
- Consistent bilingual formatting throughout

## Documentation

For detailed procedure documentation, see `idea.md` which contains:

- Complete processing procedure
- Formatting rules specification
- Quality checker details
- Edge case handling
- Agent architecture

## Support

For issues or questions:
1. Check `idea.md` for detailed documentation
2. Review the `PROCESSING_REPORT.md` after batch processing
3. Examine quality check logs in `logs/` folder

## License

This project is designed for processing Islamic scholarly lecture transcripts.

## Credits

Based on the comprehensive procedure developed for Sahih Al-Bukhari lecture note generation.
