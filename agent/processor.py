"""
Lecture Notes Processor Agent
Automated agent for converting Arabic lecture transcripts to comprehensive formatted notes
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from anthropic import Anthropic
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
    Automated agent for converting Arabic lecture transcripts
    to comprehensive formatted notes.
    """

    def __init__(self, source_folder: str, destination_folder: str, api_key: Optional[str] = None):
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.formatting_rules = FormattingRules()

        # Initialize Anthropic client
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

        # Load master prompt template
        template_path = os.path.join(os.path.dirname(__file__), 'master_prompt.txt')
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                self.master_prompt_template = f.read()
        else:
            self.master_prompt_template = self._get_default_prompt_template()

    def process_lecture(self, transcript_file: str) -> ProcessingResult:
        """Main processing pipeline"""
        print(f"Processing: {transcript_file}")

        # Phase 1: Analysis
        print("  Phase 1: Analyzing transcript...")
        analysis = self.analyze_transcript(transcript_file)

        # Phase 2: Planning
        print("  Phase 2: Creating segmentation plan...")
        plan = self.create_segmentation_plan(analysis)

        # Phase 3: Execution
        print("  Phase 3: Processing segments...")
        parts = self.process_segments(transcript_file, plan)

        # Phase 4: Merge
        print("  Phase 4: Merging parts...")
        comprehensive = self.merge_parts(parts, analysis)

        # Phase 5: Quality Check
        print("  Phase 5: Quality checking...")
        quality_checker = QualityChecker(transcript_file)
        try:
            validated = quality_checker.validate(comprehensive)
            quality_score = 100.0
        except Exception as e:
            print(f"  Warning: Quality check issues: {e}")
            validated = comprehensive
            quality_score = 50.0

        # Phase 6: Output
        print("  Phase 6: Writing output...")
        output_path = self.output_file(transcript_file, validated)

        # Calculate statistics
        word_count = len(validated.split())
        timestamp_coverage = self._calculate_timestamp_coverage(validated, analysis)

        result = ProcessingResult(
            output_path=output_path,
            word_count=word_count,
            timestamp_coverage=timestamp_coverage,
            quality_score=quality_score
        )

        print(f"✓ Completed: {output_path}")
        print(f"  Words: {word_count}, Coverage: {timestamp_coverage:.1f}%, Quality: {quality_score:.1f}")

        return result

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

        # For now, use a simple strategy: split by character count
        # More sophisticated splitting could be done based on chapters, timestamps, etc.
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

    def process_segments(self, transcript_file: str, plan: List[Dict[str, Any]]) -> List[str]:
        """Process each segment sequentially"""
        parts = []

        for segment in plan:
            print(f"    Processing part {segment['part_number']}/{len(plan)}...")
            part = self.process_single_segment(segment, len(plan))
            parts.append(part)

        return parts

    def process_single_segment(self, segment: Dict[str, Any], total_parts: int) -> str:
        """Process one segment with full detail capture using Claude API"""

        part_number = segment['part_number']
        segment_content = segment['content']

        # Create the prompt for this segment
        prompt = self._create_segment_prompt(segment_content, part_number, total_parts)

        # Call Claude API
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=16000,
                temperature=0,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract the response
            response_text = message.content[0].text
            return response_text

        except Exception as e:
            print(f"    Error processing segment {part_number}: {e}")
            # Return formatted error fallback
            return f"# Part {part_number}\n\n[Error processing this segment: {e}]\n\n```\n{segment_content}\n```"

    def merge_parts(self, parts: List[str], analysis: Dict[str, Any]) -> str:
        """Combine all parts into comprehensive document"""

        comprehensive = []

        # Title and metadata
        filename = analysis['filename']
        lecture_num = self._extract_lecture_number(filename)

        comprehensive.append("# صحيح البخاري | Ṣaḥīḥ Al-Bukhārī")
        comprehensive.append(f"# Comprehensive Lecture Notes - Lecture {lecture_num}")
        comprehensive.append("")
        comprehensive.append("---")
        comprehensive.append("")

        # Merge parts sequentially
        for i, part in enumerate(parts):
            if i > 0:
                # Add separator between parts
                comprehensive.append("")
                comprehensive.append("---")
                comprehensive.append("")

            comprehensive.append(part)

        return "\n".join(comprehensive)

    def output_file(self, transcript_file: str, content: str) -> str:
        """Write output file"""
        # Extract lecture number from filename
        filename = os.path.basename(transcript_file)
        lecture_num = self._extract_lecture_number(filename)

        # Create output filename
        output_filename = f"lecture_notes_L{lecture_num:02d}_COMPREHENSIVE.md"
        output_path = os.path.join(self.destination_folder, output_filename)

        # Ensure destination folder exists
        os.makedirs(self.destination_folder, exist_ok=True)

        # Write file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return output_path

    def _create_segment_prompt(self, segment_content: str, part_number: int, total_parts: int) -> str:
        """Create prompt for processing a segment"""

        prompt = f"""You are an expert Arabic-English bilingual transcription processor specializing in Islamic scholarly lectures. Your task is to convert this raw Arabic lecture transcript segment into comprehensive, professionally formatted notes.

This is PART {part_number} of {total_parts}.

## STRICT FORMATTING RULES

### 1. Headers (Bilingual)
- # Arabic Title | English Title          (Book level)
- ## Arabic | English                    (Chapter/Major section)
- ### Arabic | English                   (Subsection)

### 2. Timestamps
- (MM:SS-MM:SS)    Range format
- (MM:SS)          Single point format
- Every timestamp from source MUST appear in output

### 3. Text Formatting
- **Hadith text**: Full Arabic, then full English in bold
- **Sheikh explanations**: Arabic paragraph, then English translation
- **Student interactions**: Mark with [Student question] or [Student comment]

### 4. Content Capture Rules
- **Zero additions**: Add NO content not in source
- **Complete capture**: Miss NO content from source
- **Preserve tone**: Maintain sheikh's rhetorical style
- **Include everything**: Main teaching, digressions, side comments, questions, answers, contemporary applications, personal anecdotes, cross-references, variant narrations

## TRANSCRIPT SEGMENT

```
{segment_content}
```

## YOUR TASK

Process this transcript segment following ALL the rules above. Create comprehensive, well-formatted notes that:
1. Preserve all Arabic text exactly as written
2. Provide English translations for all Arabic content
3. Use bilingual headers with proper markdown hierarchy
4. Include all timestamps
5. Capture every detail from the sheikh's teaching
6. Mark all student interactions clearly
7. Maintain consistent formatting throughout

Begin processing now. Output ONLY the formatted notes, no other commentary."""

        return prompt

    def _extract_duration(self, content: str) -> str:
        """Extract total duration from timestamps"""
        timestamps = re.findall(r'(\d{1,2}:\d{2}(?::\d{2})?)', content)
        if timestamps:
            return timestamps[-1]  # Last timestamp
        return "Unknown"

    def _identify_chapters(self, content: str) -> List[str]:
        """Identify chapter markers"""
        # Look for common chapter patterns in Arabic
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
        # Look for hadith number patterns
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
        # Try to find number in filename
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
        return """You are an expert Arabic-English bilingual transcription processor specializing in Islamic scholarly lectures.
Your task is to convert raw Arabic lecture transcripts into comprehensive, professionally formatted notes.

Follow these strict rules:
1. Bilingual headers (Arabic | English)
2. Preserve all timestamps
3. Include all content with zero additions
4. Provide English translations for all Arabic
5. Use proper markdown hierarchy
6. Mark student interactions clearly
"""
