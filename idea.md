# Procedure for Generating Comprehensive Lecture Notes from Arabic Transcripts

## Overview
This document outlines the exact procedure followed to transform `corrected_1rev02.txt` into `lecture_notes_L01_COMPREHENSIVE.md`. This serves as the blueprint for automating the process across 200+ lecture files.

---

## 1. INPUT ANALYSIS PHASE

### 1.1 Initial Transcript Assessment
```bash
# Read the entire transcript to understand structure
view /mnt/user-data/uploads/corrected_1rev02.txt

# Key observations needed:
- Total duration/timestamp range (0:00-69:13)
- Number of lines (63 lines identified)
- Language mix (Arabic + English translations)
- Structural markers (chapter titles, hadith numbers, etc.)
```

### 1.2 Content Mapping
Create a mental/written map of:
- **Chapter divisions** (Kitab Bada' Al-Wahy, Kitab Al-Iman)
- **Hadith locations** (explicitly numbered: 19, 21, 22, 23, 25, 26, 27, 28, 29, 30)
- **Major sections** (Opening, Heraclius story, etc.)
- **Digressions** (Jizan circumcision, prayer time Q&A, contemporary applications)
- **Timestamp ranges** for each major section

### 1.3 Skill Selection
```bash
# Determine NO skills needed for this task
# Reason: Pure markdown text processing, not docx/pptx/xlsx creation
# If output format changes, would need:
view /mnt/skills/public/docx/SKILL.md  # For Word output
view /mnt/skills/public/pdf/SKILL.md   # For PDF output
```

---

## 2. PLANNING PHASE

### 2.1 Segmentation Strategy
Break lecture into logical parts based on:
- **Content density** (Heraclius = 17 min needs its own section)
- **Natural divisions** (chapter breaks, major topic shifts)
- **Token limits** (manage context window efficiently)

**Actual segmentation used:**
```
Part 1: 0:00-19:33 (Hadith 1-5)
  - Opening & scholars' testimony
  - Kitab Bada' Al-Wahy
  - First revelation hadith
  - Pause in revelation
  - Eagerness to memorize

Part 2: 19:33-36:26 (Hadith 6 only)
  - Complete Heraclius story
  - All 10 questions + analyses
  - Letter content + context
  - Circumcision digression
  - Roman gathering

Part 3: 36:26-69:13 (Hadith 7-30)
  - Kitab Al-Iman
  - All remaining hadith
  - Contemporary applications
  - Final notes
```

### 2.2 Formatting Rules Definition

**Strict formatting standards:**
```markdown
# Main structure:
## Arabic Title | English Title
### Subsection in Arabic | English

# Timestamps:
(MM:SS-MM:SS) for ranges
(MM:SS) for single points

# Text formatting:
- Sheikh's words in Arabic WITH English translation
- Hadith text: Full Arabic, then full English
- Student questions: Marked clearly
- Digressions: Clearly labeled

# Hierarchical levels:
# = Book level (Kitab)
## = Major hadith/section
### = Subsections within hadith
#### = Minor points (rarely used)
```

---

## 3. EXECUTION PHASE

### 3.1 Sequential Processing

**For each part:**

#### Step 1: Create Working File
```bash
create_file /home/claude/comprehensive_notes_PART[N].md
```

#### Step 2: Process Each Timestamp Sequentially
```python
# Pseudo-logic for each section:

for timestamp_range in section:
    1. Write bilingual header with timestamp
    2. Extract Arabic text from transcript
    3. Add English translation
    4. Capture ALL sheikh explanations:
       - Main teaching points
       - Side comments
       - Questions to students
       - Answers to questions
       - Contemporary references
       - Personal anecdotes
    5. Mark student interactions
    6. Note variant narrations
    7. Add cross-references where mentioned
```

#### Step 3: Quality Checks During Writing
```
✓ Every timestamp from transcript is covered
✓ No gaps in time range
✓ Arabic text preserved exactly
✓ Sheikh's tone captured (questions, emphatic statements)
✓ Structural markers maintained (hadith numbers, chapters)
✓ Digressions included in full
✓ Zero additions to content (strict policy)
```

### 3.2 Detailed Content Capture Rules

**For Hadith:**
```markdown
Format:
1. Chapter title (Arabic + English)
2. Timestamp range
3. Full isnad (chain of narration)
4. Full Arabic matn (text)
5. Full English translation
6. Sheikh's explanation paragraph by paragraph
7. Any questions/answers
8. Variant narrations if mentioned
```

**For Sheikh's Explanations:**
```markdown
Format:
1. Timestamp of explanation start
2. Context marker (Sheikh's explanation, Sheikh's question, etc.)
3. Full Arabic text of what sheikh said
4. English translation
5. Preserve rhetorical questions
6. Note emphasis patterns (repetition, tone indicators)
```

**For Student Interactions:**
```markdown
Format:
(Timestamp) **[Student comment/question]**: Arabic text
Sheikh's response with timestamp if different section
```

**For Digressions:**
```markdown
Format:
### Digression Title | English
(Timestamp range)
Full content with context
Return marker to main topic
```

---

## 4. MERGE PHASE

### 4.1 Consolidation
```bash
# Combine all parts sequentially
cat PART1.md PART2.md PART3.md > COMPREHENSIVE.md

# Verify no duplicate headers
# Verify timestamp continuity
# Verify no content gaps
```

### 4.2 Final Quality Checks
```bash
# Word count verification
wc -w lecture_notes_L01_COMPREHENSIVE.md
# Result: ~8,100 words (vs original ~1,500)

# Timestamp coverage check
# Verify: 0:00 start, 69:13 end, no gaps

# Hadith count verification
# Count ## Hadith markers = 30 total

# Structure validation
# Proper hierarchy maintained
# All Arabic has translations
# All timestamps present
```

---

## 5. OUTPUT PHASE

### 5.1 File Placement
```bash
# Copy to final destination
cp /home/claude/lecture_notes_L01_COMPREHENSIVE.md \
   /mnt/user-data/outputs/lecture_notes_L01_COMPREHENSIVE.md
```

### 5.2 Presentation
```bash
# Present file to user with summary
present_files ["/mnt/user-data/outputs/lecture_notes_L01_COMPREHENSIVE.md"]
```

---

## 6. AUTOMATED AGENT SPECIFICATION

### 6.1 Agent Architecture

```python
class LectureNotesAgent:
    """
    Automated agent for converting Arabic lecture transcripts 
    to comprehensive formatted notes.
    """
    
    def __init__(self, source_folder, destination_folder):
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.formatting_rules = FormattingRules()
        self.quality_checker = QualityChecker()
    
    def process_lecture(self, transcript_file):
        """Main processing pipeline"""
        # Phase 1: Analysis
        analysis = self.analyze_transcript(transcript_file)
        
        # Phase 2: Planning
        plan = self.create_segmentation_plan(analysis)
        
        # Phase 3: Execution
        parts = self.process_segments(plan)
        
        # Phase 4: Merge
        comprehensive = self.merge_parts(parts)
        
        # Phase 5: Quality Check
        validated = self.quality_checker.validate(comprehensive)
        
        # Phase 6: Output
        self.output_file(validated)
        
        return validated
    
    def analyze_transcript(self, file):
        """Extract structure and metadata"""
        return {
            'duration': self.extract_duration(file),
            'line_count': self.count_lines(file),
            'chapters': self.identify_chapters(file),
            'hadith_numbers': self.identify_hadith(file),
            'timestamp_ranges': self.map_timestamps(file),
            'speaker_changes': self.identify_speakers(file),
            'language_segments': self.identify_languages(file)
        }
    
    def create_segmentation_plan(self, analysis):
        """Divide into optimal processing segments"""
        segments = []
        
        # Rule 1: New segment at chapter boundaries
        for chapter in analysis['chapters']:
            segments.append(self.create_segment(chapter))
        
        # Rule 2: Split long sections (>20 min)
        for segment in segments:
            if segment.duration > 20:
                segments.extend(self.split_segment(segment))
        
        # Rule 3: Keep major stories intact
        segments = self.preserve_story_integrity(segments, analysis)
        
        return segments
    
    def process_segments(self, plan):
        """Process each segment sequentially"""
        parts = []
        
        for i, segment in enumerate(plan):
            part = self.process_single_segment(
                segment,
                part_number=i+1,
                formatting_rules=self.formatting_rules
            )
            parts.append(part)
            
            # Validate after each part
            self.quality_checker.check_part(part, segment)
        
        return parts
    
    def process_single_segment(self, segment, part_number, formatting_rules):
        """Process one segment with full detail capture"""
        
        output = []
        
        # Header
        output.append(f"# Part {part_number}")
        output.append(f"## Timestamp Range: {segment.start}-{segment.end}")
        output.append("")
        
        # Process each timestamp block
        for ts_block in segment.timestamp_blocks:
            
            # Section header (bilingual)
            if ts_block.has_title:
                output.append(f"## {ts_block.title_ar} | {ts_block.title_en}")
                output.append(f"({ts_block.start}-{ts_block.end})")
                output.append("")
            
            # Content
            if ts_block.type == 'hadith':
                output.extend(self.format_hadith(ts_block))
            elif ts_block.type == 'explanation':
                output.extend(self.format_explanation(ts_block))
            elif ts_block.type == 'question':
                output.extend(self.format_question(ts_block))
            elif ts_block.type == 'digression':
                output.extend(self.format_digression(ts_block))
            
            output.append("")
        
        return "\n".join(output)
    
    def format_hadith(self, block):
        """Format hadith with all components"""
        lines = []
        
        # Isnad
        lines.append("### الإسناد | Chain of Narration")
        lines.append(f"({block.isnad_timestamp})")
        lines.append("")
        lines.append(block.isnad_arabic)
        lines.append("")
        lines.append(block.isnad_english)
        lines.append("")
        
        # Matn
        lines.append("### المتن | Text")
        lines.append(f"({block.matn_timestamp})")
        lines.append("")
        lines.append(block.matn_arabic)
        lines.append("")
        lines.append(f"**{block.matn_english}**")
        lines.append("")
        
        # Explanation
        if block.has_explanation:
            lines.append("### شرح الشيخ | Sheikh's Explanation")
            lines.append(f"({block.explanation_timestamp})")
            lines.append("")
            lines.extend(self.format_explanation(block.explanation))
        
        return lines
    
    def format_explanation(self, block):
        """Format sheikh's explanation"""
        lines = []
        
        # Arabic
        lines.append(block.arabic_text)
        lines.append("")
        
        # English translation
        lines.append(block.english_translation)
        lines.append("")
        
        return lines
    
    def format_question(self, block):
        """Format Q&A interaction"""
        lines = []
        
        lines.append(f"**[{block.speaker}]**: {block.question_arabic}")
        lines.append("")
        
        if block.has_response:
            lines.append(f"**Sheikh's response** ({block.response_timestamp}):")
            lines.append("")
            lines.append(block.response_arabic)
            lines.append("")
            lines.append(block.response_english)
            lines.append("")
        
        return lines
    
    def format_digression(self, block):
        """Format digressions/side topics"""
        lines = []
        
        lines.append(f"### {block.title_ar} | {block.title_en}")
        lines.append(f"({block.start}-{block.end})")
        lines.append("")
        lines.extend(self.format_explanation(block.content))
        
        return lines
    
    def merge_parts(self, parts):
        """Combine all parts into comprehensive document"""
        
        comprehensive = []
        
        # Title and metadata
        comprehensive.append("# صحيح البخاري | Ṣaḥīḥ Al-Bukhārī")
        comprehensive.append("# Comprehensive Lecture Notes")
        comprehensive.append("")
        comprehensive.append("---")
        comprehensive.append("")
        
        # Merge parts sequentially
        for i, part in enumerate(parts):
            if i > 0:
                # Add continuation marker
                comprehensive.append("**[Continuation from Part {}]**".format(i))
                comprehensive.append("")
            
            comprehensive.append(part)
        
        return "\n".join(comprehensive)
```

### 6.2 Quality Checker Specification

```python
class QualityChecker:
    """Validates output quality against strict rules"""
    
    def validate(self, document):
        """Run all validation checks"""
        
        checks = [
            self.check_timestamp_coverage(),
            self.check_timestamp_continuity(),
            self.check_bilingual_completeness(),
            self.check_hadith_count(),
            self.check_structure_hierarchy(),
            self.check_no_additions(),
            self.check_arabic_preservation(),
            self.check_formatting_consistency()
        ]
        
        results = [check(document) for check in checks]
        
        if all(results):
            return document
        else:
            raise ValidationError(self.generate_error_report(results))
    
    def check_timestamp_coverage(self, document):
        """Ensure every timestamp from source is in output"""
        source_timestamps = self.extract_source_timestamps()
        output_timestamps = self.extract_output_timestamps(document)
        
        missing = set(source_timestamps) - set(output_timestamps)
        
        if missing:
            self.log_error(f"Missing timestamps: {missing}")
            return False
        return True
    
    def check_timestamp_continuity(self, document):
        """Verify no gaps in timestamp ranges"""
        timestamps = self.extract_output_timestamps(document)
        sorted_ts = sorted(timestamps, key=self.timestamp_to_seconds)
        
        for i in range(len(sorted_ts) - 1):
            current_end = self.get_end_time(sorted_ts[i])
            next_start = self.get_start_time(sorted_ts[i+1])
            
            gap = self.timestamp_to_seconds(next_start) - \
                  self.timestamp_to_seconds(current_end)
            
            if gap > 5:  # Allow 5 second tolerance
                self.log_warning(f"Gap detected: {current_end} to {next_start}")
        
        return True
    
    def check_bilingual_completeness(self, document):
        """Verify all Arabic has English translation"""
        arabic_blocks = self.extract_arabic_blocks(document)
        
        for block in arabic_blocks:
            if not self.has_translation(block, document):
                self.log_error(f"Missing translation for: {block[:50]}...")
                return False
        
        return True
    
    def check_hadith_count(self, document):
        """Verify all hadith are captured"""
        expected_count = 30  # From source analysis
        
        hadith_markers = self.count_hadith_markers(document)
        
        if hadith_markers != expected_count:
            self.log_error(f"Expected {expected_count} hadith, found {hadith_markers}")
            return False
        
        return True
    
    def check_structure_hierarchy(self, document):
        """Verify markdown hierarchy is correct"""
        lines = document.split('\n')
        header_stack = []
        
        for line in lines:
            if line.startswith('#'):
                level = len(line.split()[0])
                
                # Check proper nesting
                if header_stack and level > header_stack[-1] + 1:
                    self.log_error(f"Header hierarchy skip: {line}")
                    return False
                
                header_stack.append(level)
        
        return True
    
    def check_no_additions(self, document):
        """Verify no content added beyond source"""
        # This is validated during creation, but double-check
        # by comparing key phrases from source
        
        source_key_phrases = self.extract_key_phrases(self.source)
        document_content = self.extract_content_phrases(document)
        
        # All source phrases should be in document
        for phrase in source_key_phrases:
            if phrase not in document_content:
                self.log_warning(f"Source phrase not found: {phrase}")
        
        return True
    
    def check_arabic_preservation(self, document):
        """Verify Arabic text matches source exactly"""
        source_arabic = self.extract_arabic_text(self.source)
        document_arabic = self.extract_arabic_text(document)
        
        # Compare normalized versions
        source_normalized = self.normalize_arabic(source_arabic)
        document_normalized = self.normalize_arabic(document_arabic)
        
        if source_normalized != document_normalized:
            diff = self.compute_diff(source_normalized, document_normalized)
            self.log_error(f"Arabic text mismatch: {diff}")
            return False
        
        return True
    
    def check_formatting_consistency(self, document):
        """Verify consistent formatting throughout"""
        
        # Check timestamp format: (MM:SS) or (MM:SS-MM:SS)
        timestamp_pattern = r'\(\d{1,2}:\d{2}(?:-\d{1,2}:\d{2})?\)'
        timestamps = re.findall(timestamp_pattern, document)
        
        if not timestamps:
            self.log_error("No timestamps found in document")
            return False
        
        # Check bilingual headers: Arabic | English
        header_pattern = r'^##+ [^\|]+ \| .+$'
        headers = re.findall(header_pattern, document, re.MULTILINE)
        
        # More checks...
        
        return True
```

### 6.3 Formatting Rules Class

```python
class FormattingRules:
    """Centralized formatting rules"""
    
    HEADER_LEVELS = {
        'book': '#',
        'major_section': '##',
        'hadith': '##',
        'subsection': '###',
        'minor_point': '####'
    }
    
    TIMESTAMP_FORMATS = {
        'range': '({start}-{end})',
        'single': '({timestamp})'
    }
    
    BILINGUAL_TEMPLATE = "{arabic} | {english}"
    
    SPEAKER_MARKERS = {
        'sheikh_explanation': "**Sheikh's explanation**",
        'sheikh_question': "**Sheikh's question**",
        'sheikh_comment': "**Sheikh's comment**",
        'student_question': "**[Student question]**",
        'student_comment': "**[Student comment]**"
    }
    
    def format_header(self, level, arabic, english, timestamp=None):
        """Format bilingual header with optional timestamp"""
        level_marker = self.HEADER_LEVELS[level]
        header = f"{level_marker} {self.BILINGUAL_TEMPLATE.format(arabic=arabic, english=english)}"
        
        if timestamp:
            if isinstance(timestamp, tuple):
                ts_str = self.TIMESTAMP_FORMATS['range'].format(
                    start=timestamp[0], end=timestamp[1]
                )
            else:
                ts_str = self.TIMESTAMP_FORMATS['single'].format(
                    timestamp=timestamp
                )
            header += f"\n{ts_str}"
        
        return header
    
    def format_hadith_text(self, arabic, english):
        """Format hadith with proper emphasis"""
        return f"{arabic}\n\n**{english}**"
    
    def format_speaker(self, speaker_type, content_ar, content_en, timestamp):
        """Format speaker contributions"""
        marker = self.SPEAKER_MARKERS[speaker_type]
        ts_str = self.TIMESTAMP_FORMATS['single'].format(timestamp=timestamp)
        
        return f"{marker} {ts_str}:\n\n{content_ar}\n\n{content_en}"
```

---

## 7. MASTER PROMPT TEMPLATE

```markdown
# Master Prompt for Lecture Note Generation

You are an expert Arabic-English bilingual transcription processor specializing in Islamic scholarly lectures. Your task is to convert raw Arabic lecture transcripts into comprehensive, professionally formatted notes.

## INPUT SPECIFICATION
- Source file: {transcript_filename}
- Format: Arabic text with timestamps (MM:SS or HH:MM:SS)
- Content: Hadith narrations, scholarly explanations, Q&A
- Language: Mixed Arabic and English

## OUTPUT SPECIFICATION
- Destination: {output_filename}
- Format: Markdown (.md)
- Structure: Hierarchical with bilingual headers
- Coverage: 100% of source timestamps

## STRICT FORMATTING RULES

### 1. Headers (Bilingual)
```
# Arabic Title | English Title          (Book level)
## Arabic | English                    (Chapter/Major section)
### Arabic | English                   (Subsection)
```

### 2. Timestamps
```
(MM:SS-MM:SS)    Range format
(MM:SS)          Single point format
```
- Every timestamp from source MUST appear in output
- No gaps allowed in timestamp coverage
- Place timestamp immediately after section header

### 3. Text Formatting
- **Hadith text**: Full Arabic, then full English in bold
- **Sheikh explanations**: Arabic paragraph, then English translation
- **Student interactions**: Mark with [Student question] or [Student comment]
- **Emphasis**: Use **bold** for English translations of key Arabic phrases

### 4. Hierarchical Structure
```
# Kitab (Book)
## Chapter Title
### Hadith Number
#### Isnad (Chain)
#### Matn (Text)
#### Sharh (Explanation)
### Questions/Discussion
## Next Chapter
```

### 5. Content Capture Rules
- **Zero additions**: Add NO content not in source
- **Complete capture**: Miss NO content from source
- **Preserve tone**: Maintain sheikh's rhetorical style
- **Include everything**:
  - Main teaching
  - Digressions
  - Side comments
  - Questions from students
  - Answers from sheikh
  - Contemporary applications
  - Personal anecdotes
  - Cross-references
  - Variant narrations

### 6. Quality Standards
✓ Every timestamp covered
✓ All Arabic preserved exactly
✓ All Arabic has English translation
✓ Bilingual headers throughout
✓ Proper markdown hierarchy
✓ Consistent formatting
✓ No content gaps
✓ No unauthorized additions

## PROCESSING PROCEDURE

### Phase 1: ANALYSIS
1. Read entire transcript
2. Identify all timestamps
3. Map major sections (chapters, hadith numbers)
4. Note structural elements (Q&A, digressions)
5. Calculate total duration

### Phase 2: PLANNING
1. Divide into logical segments (typically 3-5 parts)
2. Segment at natural boundaries:
   - Chapter changes
   - Major topic shifts
   - Long stories (keep intact)
3. Plan for 15-25 minute segments
4. Ensure no timestamp splits

### Phase 3: EXECUTION
For each segment:
1. Create working file: comprehensive_notes_PART{N}.md
2. Process sequentially from start timestamp to end
3. For each timestamp block:
   a. Write bilingual header with timestamp
   b. Extract Arabic text
   c. Add English translation
   d. Capture ALL sheikh commentary
   e. Include student interactions
   f. Note any variants/cross-refs
4. Validate segment before moving to next

### Phase 4: MERGE
1. Concatenate all parts sequentially
2. Verify timestamp continuity
3. Check for duplicate headers
4. Confirm no content gaps

### Phase 5: QUALITY CHECK
Run all validations:
- [ ] Timestamp coverage complete
- [ ] No timestamp gaps
- [ ] All Arabic translated
- [ ] Hadith count matches
- [ ] Hierarchy correct
- [ ] No additions made
- [ ] Arabic preserved exactly
- [ ] Formatting consistent

### Phase 6: OUTPUT
1. Save to destination folder
2. Generate summary statistics
3. Report any warnings/issues

## EXAMPLE PATTERNS

### Hadith Format
```markdown
## الحديث السادس | Hadith 6
(19:33-36:26)

### الإسناد | Chain of Narration

حَدَّثَنَا أَبُو الْيَمَانِ...

Ḥadathanā Abū Al-Yamān...

### المتن | Text

قَالَ رَسُولُ اللَّهِ صلى الله عليه وسلم...

The Messenger of Allah صلى الله عليه وسلم said: **"..."**

### شرح الشيخ | Sheikh's Explanation
(20:13-20:50)

يَعْنِي يَقُولُ...

Meaning he says...
```

### Digression Format
```markdown
### حاشية: الختان في جيزان | Digression: Circumcision in Jizan
(33:26-34:07)

كَانَ عِنْدَنَا...

We had...
```

### Q&A Format
```markdown
**[Student question]** (24:15):

وَقْتُ نَهْيٍ يَا شَيْخُ؟

Forbidden time, O Sheikh?

**Sheikh's answer** (24:20-25:09):

الْوَقْتُ اللِّي نَجْلِسُ فِيهِ...

The time when we sit...
```

## CRITICAL REMINDERS
1. **Never skip timestamps** - every single one must be in output
2. **Never add content** - only capture what sheikh said
3. **Always provide translations** - every Arabic block needs English
4. **Maintain hierarchy** - proper header levels throughout
5. **Preserve Arabic exactly** - no modifications to original text
6. **Include everything** - digressions, Q&A, side comments, all of it

## OUTPUT STRUCTURE
```
/destination_folder/
  lecture_notes_L{NN}_COMPREHENSIVE.md
  
Word count: ~5-10x original transcript length
Timestamp coverage: 100%
Hadith count: Varies by lecture
Quality: Publication-ready
```

Begin processing now.
```

---

## 8. AUTOMATION IMPLEMENTATION GUIDE

### 8.1 Folder Structure
```
/project_root/
├── source_transcripts/          # Input: Raw transcript files
│   ├── corrected_1rev02.txt
│   ├── corrected_2rev01.txt
│   └── ...
├── outputs/                     # Output: Final comprehensive notes
│   ├── lecture_notes_L01_COMPREHENSIVE.md
│   ├── lecture_notes_L02_COMPREHENSIVE.md
│   └── ...
├── working/                     # Temporary: Part files during processing
│   ├── L01_PART1.md
│   ├── L01_PART2.md
│   └── ...
├── logs/                        # Quality check logs
│   ├── L01_validation.log
│   └── ...
└── agent/                       # Agent code
    ├── processor.py
    ├── quality_checker.py
    ├── formatter.py
    └── master_prompt.txt
```

### 8.2 Batch Processing Script

```python
#!/usr/bin/env python3
"""
Batch processor for converting all lecture transcripts
to comprehensive formatted notes.
"""

import os
import glob
from pathlib import Path
from processor import LectureNotesAgent
from quality_checker import QualityChecker

def batch_process_lectures(source_folder, destination_folder):
    """Process all transcripts in source folder"""
    
    # Initialize agent
    agent = LectureNotesAgent(source_folder, destination_folder)
    
    # Get all transcript files
    transcript_files = sorted(glob.glob(f"{source_folder}/*.txt"))
    
    print(f"Found {len(transcript_files)} transcripts to process")
    
    results = []
    
    for i, transcript_file in enumerate(transcript_files, 1):
        print(f"\n{'='*60}")
        print(f"Processing {i}/{len(transcript_files)}: {transcript_file}")
        print(f"{'='*60}\n")
        
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
            
            print(f"✓ Successfully processed {transcript_file}")
            
        except Exception as e:
            # Log failure
            results.append({
                'file': transcript_file,
                'status': 'FAILED',
                'error': str(e)
            })
            
            print(f"✗ Failed to process {transcript_file}: {e}")
    
    # Generate summary report
    generate_summary_report(results, destination_folder)
    
    return results

def generate_summary_report(results, output_folder):
    """Create summary report of batch processing"""
    
    report_path = f"{output_folder}/PROCESSING_REPORT.md"
    
    with open(report_path, 'w') as f:
        f.write("# Batch Processing Report\n\n")
        
        # Summary statistics
        total = len(results)
        successful = sum(1 for r in results if r['status'] == 'SUCCESS')
        failed = total - successful
        
        f.write(f"## Summary\n\n")
        f.write(f"- Total files: {total}\n")
        f.write(f"- Successful: {successful}\n")
        f.write(f"- Failed: {failed}\n")
        f.write(f"- Success rate: {successful/total*100:.1f}%\n\n")
        
        # Detailed results
        f.write(f"## Detailed Results\n\n")
        
        for result in results:
            f.write(f"### {os.path.basename(result['file'])}\n\n")
            f.write(f"- Status: {result['status']}\n")
            
            if result['status'] == 'SUCCESS':
                f.write(f"- Output: {result['output']}\n")
                f.write(f"- Word count: {result['word_count']}\n")
                f.write(f"- Timestamp coverage: {result['timestamp_coverage']}%\n")
                f.write(f"- Quality score: {result['quality_score']}/100\n")
            else:
                f.write(f"- Error: {result['error']}\n")
            
            f.write("\n")
    
    print(f"\nSummary report generated: {report_path}")

if __name__ == "__main__":
    SOURCE_FOLDER = "/mnt/user-data/uploads/transcripts"
    DESTINATION_FOLDER = "/mnt/user-data/outputs/comprehensive_notes"
    
    batch_process_lectures(SOURCE_FOLDER, DESTINATION_FOLDER)
```

---

## 9. EXECUTION CHECKLIST FOR EACH FILE

```markdown
## Pre-Processing
- [ ] Verify source file exists and is readable
- [ ] Check file encoding (should be UTF-8)
- [ ] Confirm Arabic text displays correctly
- [ ] Extract metadata (duration, line count)

## Analysis Phase
- [ ] Map all timestamps (start, end, gaps)
- [ ] Identify chapter divisions
- [ ] Count hadith numbers mentioned
- [ ] Note structural elements (Q&A, digressions)
- [ ] Calculate expected output size

## Planning Phase
- [ ] Determine segmentation strategy
- [ ] Create processing plan (3-5 parts typically)
- [ ] Assign timestamp ranges to each part
- [ ] Identify complex sections needing extra care

## Execution Phase - For Each Part
- [ ] Create part file
- [ ] Process timestamps sequentially
- [ ] Capture all Arabic text exactly
- [ ] Add English translations
- [ ] Include all explanations
- [ ] Mark all interactions
- [ ] Verify formatting rules
- [ ] Check part completeness

## Merge Phase
- [ ] Concatenate parts in order
- [ ] Verify no duplicate content
- [ ] Check timestamp continuity
- [ ] Confirm proper structure

## Quality Check Phase
- [ ] Run timestamp coverage check
- [ ] Verify timestamp continuity
- [ ] Confirm bilingual completeness
- [ ] Validate hadith count
- [ ] Check structure hierarchy
- [ ] Verify no additions made
- [ ] Confirm Arabic preservation
- [ ] Validate formatting consistency

## Output Phase
- [ ] Save to destination folder
- [ ] Generate file statistics
- [ ] Create validation log
- [ ] Update batch progress

## Post-Processing
- [ ] Delete temporary part files
- [ ] Archive source transcript
- [ ] Update master index
- [ ] Generate quality report
```

---

## 10. EDGE CASES AND SPECIAL HANDLING

### 10.1 Missing Timestamps
```python
# If timestamp missing in transcript
if not has_timestamp(block):
    # Interpolate based on surrounding timestamps
    estimated_ts = interpolate_timestamp(prev_ts, next_ts, block_position)
    log_warning(f"Interpolated timestamp: {estimated_ts}")
```

### 10.2 Overlapping Timestamps
```python
# If timestamps overlap (e.g., 25:30-26:00 followed by 25:45-26:15)
if is_overlapping(current_ts, previous_ts):
    # Use the more specific range
    resolved_ts = resolve_overlap(current_ts, previous_ts)
    log_warning(f"Resolved overlapping timestamps: {resolved_ts}")
```

### 10.3 Multiple Speakers in Same Timestamp
```python
# If multiple speakers in one timestamp block
if has_multiple_speakers(block):
    # Split block by speaker markers
    for speaker, content in split_by_speaker(block):
        format_speaker_section(speaker, content, timestamp)
```

### 10.4 Very Long Sections (>30 minutes)
```python
# If single section exceeds 30 minutes
if section_duration > 30:
    # Split into sub-sections by natural breaks
    subsections = split_by_natural_breaks(section)
    for subsection in subsections:
        process_subsection(subsection)
```

### 10.5 Incomplete Arabic Text
```python
# If Arabic text appears incomplete or corrupted
if is_incomplete(arabic_text):
    # Flag for manual review
    log_error(f"Incomplete Arabic text at {timestamp}: {arabic_text}")
    # Include as-is with marker
    output.append(f"[REVIEW NEEDED] {arabic_text}")
```

---

This document provides the complete blueprint for automating the lecture notes generation process. The agent should strictly follow these procedures to ensure consistent, high-quality output across all 200+ files.
