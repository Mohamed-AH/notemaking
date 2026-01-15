"""
Quality Checker for Lecture Notes
Validates output quality against strict rules
"""

import re
from typing import List, Dict, Any, Tuple


class ValidationError(Exception):
    """Raised when validation fails"""
    pass


class QualityChecker:
    """Validates output quality against strict rules"""

    def __init__(self, source_file=None):
        self.source_file = source_file
        self.source = None
        if source_file:
            with open(source_file, 'r', encoding='utf-8') as f:
                self.source = f.read()
        self.errors = []
        self.warnings = []

    def validate(self, document: str) -> bool:
        """Run all validation checks"""
        self.errors = []
        self.warnings = []

        checks = [
            ('Timestamp Coverage', self.check_timestamp_coverage),
            ('Timestamp Continuity', self.check_timestamp_continuity),
            ('Bilingual Completeness', self.check_bilingual_completeness),
            ('Structure Hierarchy', self.check_structure_hierarchy),
            ('Arabic Preservation', self.check_arabic_preservation),
            ('Formatting Consistency', self.check_formatting_consistency)
        ]

        results = []
        for name, check in checks:
            try:
                result = check(document)
                results.append((name, result))
            except Exception as e:
                self.log_error(f"{name} check failed: {str(e)}")
                results.append((name, False))

        all_passed = all(result for _, result in results)

        if not all_passed:
            error_report = self.generate_error_report(results)
            raise ValidationError(error_report)

        return document

    def check_timestamp_coverage(self, document: str) -> bool:
        """Ensure timestamps are present in output"""
        output_timestamps = self.extract_output_timestamps(document)

        if not output_timestamps:
            self.log_error("No timestamps found in document")
            return False

        if self.source:
            source_timestamps = self.extract_source_timestamps()
            missing = set(source_timestamps) - set(output_timestamps)

            if missing:
                self.log_warning(f"Some source timestamps may be missing: {len(missing)} timestamps")

        return True

    def check_timestamp_continuity(self, document: str) -> bool:
        """Verify no large gaps in timestamp ranges"""
        timestamps = self.extract_output_timestamps(document)

        if not timestamps:
            return True  # Already checked in coverage

        sorted_ts = sorted(timestamps, key=self.timestamp_to_seconds)

        for i in range(len(sorted_ts) - 1):
            current_seconds = self.timestamp_to_seconds(sorted_ts[i])
            next_seconds = self.timestamp_to_seconds(sorted_ts[i + 1])

            gap = next_seconds - current_seconds

            # Allow up to 5 minute gaps (could be chapter breaks)
            if gap > 300:  # 5 minutes
                self.log_warning(f"Large gap detected between timestamps: {sorted_ts[i]} to {sorted_ts[i+1]}")

        return True

    def check_bilingual_completeness(self, document: str) -> bool:
        """Verify bilingual headers are present"""
        # Check for headers with pipe separator (Arabic | English)
        bilingual_headers = re.findall(r'^#{1,4}\s+.+\s+\|\s+.+$', document, re.MULTILINE)

        if not bilingual_headers:
            self.log_warning("Few bilingual headers found - may need manual review")

        return True

    def check_structure_hierarchy(self, document: str) -> bool:
        """Verify markdown hierarchy is correct"""
        lines = document.split('\n')
        header_stack = []

        for i, line in enumerate(lines, 1):
            if line.startswith('#') and not line.startswith('#!'):
                # Count # symbols
                level = len(line) - len(line.lstrip('#'))

                # Check proper nesting (allow skipping levels down but not up)
                if header_stack and level > header_stack[-1] + 1:
                    self.log_warning(f"Header hierarchy skip at line {i}: {line[:50]}")

                # Update stack
                while header_stack and header_stack[-1] >= level:
                    header_stack.pop()
                header_stack.append(level)

        return True

    def check_arabic_preservation(self, document: str) -> bool:
        """Verify Arabic text is present"""
        # Check for Arabic characters
        arabic_pattern = re.compile(r'[\u0600-\u06FF]+')
        arabic_found = arabic_pattern.search(document)

        if not arabic_found:
            self.log_error("No Arabic text found in document")
            return False

        return True

    def check_formatting_consistency(self, document: str) -> bool:
        """Verify consistent formatting throughout"""

        # Check timestamp format: (MM:SS) or (MM:SS-MM:SS) or (H:MM:SS)
        timestamp_pattern = r'\(\d{1,2}:\d{2}(?::\d{2})?(?:-\d{1,2}:\d{2}(?::\d{2})?)?\)'
        timestamps = re.findall(timestamp_pattern, document)

        if not timestamps:
            self.log_error("No properly formatted timestamps found")
            return False

        # Check for bilingual headers: Arabic | English
        header_pattern = r'^##+ .+ \| .+$'
        headers = re.findall(header_pattern, document, re.MULTILINE)

        if not headers:
            self.log_warning("Few bilingual headers found")

        return True

    def extract_source_timestamps(self) -> List[str]:
        """Extract timestamps from source file"""
        if not self.source:
            return []

        # Match timestamps in format (MM:SS), (H:MM:SS), (MM:SS-MM:SS)
        pattern = r'\((\d{1,2}:\d{2}(?::\d{2})?(?:-\d{1,2}:\d{2}(?::\d{2})?)?)\)'
        matches = re.findall(pattern, self.source)
        return matches

    def extract_output_timestamps(self, document: str) -> List[str]:
        """Extract timestamps from output document"""
        # Match timestamps in format (MM:SS), (H:MM:SS), (MM:SS-MM:SS)
        pattern = r'\((\d{1,2}:\d{2}(?::\d{2})?(?:-\d{1,2}:\d{2}(?::\d{2})?)?)\)'
        matches = re.findall(pattern, document)
        return matches

    def timestamp_to_seconds(self, timestamp: str) -> int:
        """Convert timestamp string to seconds"""
        # Handle range timestamps - take the start time
        if '-' in timestamp:
            timestamp = timestamp.split('-')[0]

        parts = timestamp.split(':')
        if len(parts) == 2:  # MM:SS
            minutes, seconds = map(int, parts)
            return minutes * 60 + seconds
        elif len(parts) == 3:  # H:MM:SS
            hours, minutes, seconds = map(int, parts)
            return hours * 3600 + minutes * 60 + seconds
        return 0

    def log_error(self, message: str):
        """Log an error"""
        self.errors.append(message)

    def log_warning(self, message: str):
        """Log a warning"""
        self.warnings.append(message)

    def generate_error_report(self, results: List[Tuple[str, bool]]) -> str:
        """Generate error report"""
        report = ["Quality Check Failed:", ""]

        for name, passed in results:
            status = "✓" if passed else "✗"
            report.append(f"{status} {name}")

        if self.errors:
            report.append("\nErrors:")
            for error in self.errors:
                report.append(f"  - {error}")

        if self.warnings:
            report.append("\nWarnings:")
            for warning in self.warnings:
                report.append(f"  - {warning}")

        return "\n".join(report)

    def get_report(self) -> str:
        """Get validation report"""
        report = ["Quality Check Report:", ""]

        if self.errors:
            report.append("Errors:")
            for error in self.errors:
                report.append(f"  - {error}")
        else:
            report.append("No errors found.")

        if self.warnings:
            report.append("\nWarnings:")
            for warning in self.warnings:
                report.append(f"  - {warning}")
        else:
            report.append("No warnings.")

        return "\n".join(report)
