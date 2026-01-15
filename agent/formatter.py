"""
Formatting Rules for Lecture Notes Generation
Provides centralized formatting rules for consistent output
"""


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
