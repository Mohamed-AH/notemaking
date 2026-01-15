"""
Lecture Notes Processor for Claude Code
Prepares transcripts for processing within Claude Code environment
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from formatter import FormattingRules
from quality_checker import QualityChecker


class ProcessingResult:
    """Result of processing a lecture"""

    def __init__(self, output_path: str, word_count: int,
                 timestamp_coverage: float, quality_score: float):
        self.output_path = output_path
        self.word_count = word_count
        self.timestamp_coverage = timestamp_coverage
        self.quality_score = quality_score


class LectureNotesAgent:
    """
    Prepares Arabic lecture transcripts for processing in Claude Code environment.
    """

    def __init__(self, source_folder: str, destination_folder: str, working_folder: str = "working"):
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.working_folder = working_folder
        self.formatting_rules = FormattingRules()

        # Ensure folders exist
        os.makedirs(working_folder, exist_ok=True)
        os.makedirs(destination_folder, exist_ok=True)

        # Load master prompt template
        template_path = os.path.join(os.path.dirname(__file__), 'master_prompt.txt')
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                self.master_prompt_template = f.read()
        else:
            self.master_prompt_template = self._get_default_prompt_template()

    def prepare_lecture(self, transcript_file: str) -> Dict[str, Any]:
        """Prepare lecture for processing - creates segment files"""
        print(f"Preparing: {transcript_file}")

        # Phase 1: Analysis
        print("  Phase 1: Analyzing transcript...")
        analysis = self.analyze_transcript(transcript_file)

        # Phase 2: Planning
        print("  Phase 2: Creating segmentation plan...")
        plan = self.create_segmentation_plan(analysis)

        # Phase 3: Create segment files
        print("  Phase 3: Creating segment files...")
        segment_files = self.create_segment_files(transcript_file, plan, analysis)

        return {
            'transcript_file': transcript_file,
            'analysis': analysis,
            'plan': plan,
            'segment_files': segment_files,
            'lecture_number': self._extract_lecture_number(os.path.basename(transcript_file))
        }

    def analyze_transcript(self, file: str) -> Dict[str, Any]:
        """Extract structure and metadata"""
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        analysis = {
            'filename': os.path.basename(file),
            'line_count': len(content.split('\n')),
            'char_count': len(content),
            'duration': self._extract_duration(content),
            'chapters': self._identify_chapters(content),
            'hadith_numbers': self._identify_hadith(content),
            'timestamp_ranges': self._map_timestamps(content),
            'content': content
        }

        return analysis

    def create_segmentation_plan(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Divide into optimal processing segments"""
        content = analysis['content']
        lines = content.split('\n')

        # Split by character count for manageable segments
        max_chars_per_segment = 15000  # ~15k characters per segment

        segments = []
        current_segment_lines = []
        current_char_count = 0

        for line in lines:
            line_length = len(line) + 1  # +1 for newline

            if current_char_count + line_length > max_chars_per_segment and current_segment_lines:
                # Save current segment
                segment_content = '\n'.join(current_segment_lines)
                segments.append({
                    'part_number': len(segments) + 1,
                    'content': segment_content,
                    'line_count': len(current_segment_lines)
                })
                current_segment_lines = []
                current_char_count = 0

            current_segment_lines.append(line)
            current_char_count += line_length

        # Add final segment
        if current_segment_lines:
            segment_content = '\n'.join(current_segment_lines)
            segments.append({
                'part_number': len(segments) + 1,
                'content': segment_content,
                'line_count': len(current_segment_lines)
            })

        # If only one small segment, keep it
        if not segments:
            segments.append({
                'part_number': 1,
                'content': content,
                'line_count': len(lines)
            })

        return segments

    def create_segment_files(self, transcript_file: str, plan: List[Dict[str, Any]],
                           analysis: Dict[str, Any]) -> List[str]:
        """Create work files for each segment"""
        filename = os.path.basename(transcript_file)
        lecture_num = self._extract_lecture_number(filename)

        segment_files = []

        for segment in plan:
            part_num = segment['part_number']
            total_parts = len(plan)

            # Create segment file
            segment_filename = f"L{lecture_num:02d}_PART{part_num}_segment.txt"
            segment_path = os.path.join(self.working_folder, segment_filename)

            with open(segment_path, 'w', encoding='utf-8') as f:
                f.write(segment['content'])

            # Create instruction file
            instruction_filename = f"L{lecture_num:02d}_PART{part_num}_instructions.md"
            instruction_path = os.path.join(self.working_folder, instruction_filename)

            instruction_content = self._create_segment_instructions(
                segment, part_num, total_parts, lecture_num
            )

            with open(instruction_path, 'w', encoding='utf-8') as f:
                f.write(instruction_content)

            segment_files.append({
                'part_number': part_num,
                'segment_file': segment_path,
                'instruction_file': instruction_path,
                'output_file': os.path.join(self.working_folder,
                                           f"L{lecture_num:02d}_PART{part_num}_output.md")
            })

            print(f"    Created part {part_num}/{total_parts}: {segment_filename}")

        return segment_files

    def _create_segment_instructions(self, segment: Dict[str, Any],
                                    part_number: int, total_parts: int,
                                    lecture_num: int) -> str:
        """Create instruction file for segment processing"""

        return f"""# Processing Instructions for Lecture {lecture_num:02d} - Part {part_number}/{total_parts}

## Task
Convert this Arabic lecture transcript segment into comprehensive, professionally formatted notes.

## Input File
`L{lecture_num:02d}_PART{part_number}_segment.txt`

## Output File
`L{lecture_num:02d}_PART{part_number}_output.md`

## Formatting Rules

### 1. Headers (Bilingual)
- `# Arabic Title | English Title` (Book level)
- `## Arabic | English` (Chapter/Major section)
- `### Arabic | English` (Subsection)

### 2. Timestamps
- `(MM:SS-MM:SS)` for ranges
- `(MM:SS)` for single points
- Every timestamp from source MUST appear in output
- Place timestamp immediately after section header

### 3. Text Formatting
- **Hadith text**: Full Arabic, then full English in bold
- **Sheikh explanations**: Arabic paragraph, then English translation
- **Student interactions**: Mark with `[Student question]` or `[Student comment]`

### 4. Content Capture Rules
- **Zero additions**: Add NO content not in source
- **Complete capture**: Miss NO content from source
- **Preserve tone**: Maintain sheikh's rhetorical style
- **Include everything**: Main teaching, digressions, side comments, questions, answers

### 5. Example Format

```markdown
## الحديث الأول | Hadith 1
(0:45-5:00)

### الإسناد | Chain of Narration

حَدَّثَنَا الْحُمَيْدِيُّ...

Al-Humaidi narrated to us...

### المتن | Text

إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ

**"Actions are but by intentions"**

### شرح الشيخ | Sheikh's Explanation
(4:00-4:45)

هذا الحديث العظيم...

This great hadith...

**[Student question]** (5:00):
ما معنى النية؟
What is the meaning of intention?

**Sheikh's answer** (5:15):
النية محلها القلب...
The intention is in the heart...
```

## Instructions

1. Read the segment file: `L{lecture_num:02d}_PART{part_number}_segment.txt`
2. Process ALL content following the formatting rules above
3. Preserve all Arabic text exactly as written
4. Provide English translations for all Arabic content
5. Use bilingual headers throughout
6. Include all timestamps
7. Capture every detail from the transcript
8. Write output to: `L{lecture_num:02d}_PART{part_number}_output.md`

## Critical Reminders
- Never skip timestamps
- Never add content not in source
- Always provide translations
- Maintain proper hierarchy
- Preserve Arabic exactly
- Include everything (digressions, Q&A, side comments)
"""

    def merge_parts(self, segment_files: List[Dict[str, Any]], analysis: Dict[str, Any],
                   lecture_num: int) -> str:
        """Combine all processed parts into comprehensive document"""

        print(f"Merging {len(segment_files)} parts...")

        comprehensive = []

        # Title and metadata
        comprehensive.append("# صحيح البخاري | Ṣaḥīḥ Al-Bukhārī")
        comprehensive.append(f"# Comprehensive Lecture Notes - Lecture {lecture_num:02d}")
        comprehensive.append("")
        comprehensive.append("---")
        comprehensive.append("")

        # Merge parts sequentially
        for i, segment_info in enumerate(segment_files):
            output_file = segment_info['output_file']

            if not os.path.exists(output_file):
                print(f"  Warning: Output file not found: {output_file}")
                comprehensive.append(f"\n\n**[Part {segment_info['part_number']} - Not yet processed]**\n\n")
                continue

            with open(output_file, 'r', encoding='utf-8') as f:
                part_content = f.read()

            if i > 0:
                comprehensive.append("")
                comprehensive.append("---")
                comprehensive.append("")

            comprehensive.append(part_content)
            print(f"  Merged part {segment_info['part_number']}")

        return "\n".join(comprehensive)

    def finalize_lecture(self, preparation: Dict[str, Any]) -> ProcessingResult:
        """Finalize and validate the comprehensive notes"""

        lecture_num = preparation['lecture_number']
        segment_files = preparation['segment_files']
        analysis = preparation['analysis']

        print(f"\nFinalizing Lecture {lecture_num:02d}...")

        # Merge all parts
        comprehensive = self.merge_parts(segment_files, analysis, lecture_num)

        # Quality check
        print("  Running quality checks...")
        quality_checker = QualityChecker(preparation['transcript_file'])
        try:
            validated = quality_checker.validate(comprehensive)
            quality_score = 100.0
            print("  ✓ Quality checks passed")
        except Exception as e:
            print(f"  ⚠ Quality check warnings: {e}")
            validated = comprehensive
            quality_score = 70.0

        # Write final output
        output_filename = f"lecture_notes_L{lecture_num:02d}_COMPREHENSIVE.md"
        output_path = os.path.join(self.destination_folder, output_filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(validated)

        # Calculate statistics
        word_count = len(validated.split())
        timestamp_coverage = self._calculate_timestamp_coverage(validated, analysis)

        result = ProcessingResult(
            output_path=output_path,
            word_count=word_count,
            timestamp_coverage=timestamp_coverage,
            quality_score=quality_score
        )

        print(f"\n✓ Completed: {output_path}")
        print(f"  Words: {word_count}, Coverage: {timestamp_coverage:.1f}%, Quality: {quality_score:.1f}")

        return result

    def _extract_duration(self, content: str) -> str:
        """Extract total duration from timestamps"""
        timestamps = re.findall(r'(\d{1,2}:\d{2}(?::\d{2})?)', content)
        if timestamps:
            return timestamps[-1]
        return "Unknown"

    def _identify_chapters(self, content: str) -> List[str]:
        """Identify chapter markers"""
        patterns = [
            r'كتاب\s+[\u0600-\u06FF\s]+',
            r'باب\s+[\u0600-\u06FF\s]+',
        ]

        chapters = []
        for pattern in patterns:
            matches = re.findall(pattern, content)
            chapters.extend(matches)

        return chapters

    def _identify_hadith(self, content: str) -> List[int]:
        """Identify hadith numbers"""
        patterns = [
            r'(?:الحديث|حديث)\s+(?:رقم\s+)?(\d+)',
            r'Hadith\s+(?:number\s+)?(\d+)',
        ]

        hadith_numbers = set()
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            hadith_numbers.update(int(m) for m in matches)

        return sorted(list(hadith_numbers))

    def _map_timestamps(self, content: str) -> List[str]:
        """Extract all timestamps"""
        pattern = r'\((\d{1,2}:\d{2}(?::\d{2})?(?:-\d{1,2}:\d{2}(?::\d{2})?)?)\)'
        timestamps = re.findall(pattern, content)
        return timestamps

    def _extract_lecture_number(self, filename: str) -> int:
        """Extract lecture number from filename"""
        matches = re.findall(r'(\d+)', filename)
        if matches:
            return int(matches[0])
        return 1

    def _calculate_timestamp_coverage(self, document: str, analysis: Dict[str, Any]) -> float:
        """Calculate what percentage of source timestamps appear in output"""
        source_timestamps = set(analysis['timestamp_ranges'])

        output_pattern = r'\((\d{1,2}:\d{2}(?::\d{2})?(?:-\d{1,2}:\d{2}(?::\d{2})?)?)\)'
        output_timestamps = set(re.findall(output_pattern, document))

        if not source_timestamps:
            return 100.0

        coverage = len(output_timestamps & source_timestamps) / len(source_timestamps) * 100
        return coverage

    def _get_default_prompt_template(self) -> str:
        """Return default prompt template"""
        return """Process this Arabic lecture transcript into comprehensive formatted notes following strict bilingual formatting rules."""
