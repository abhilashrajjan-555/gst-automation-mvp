"""
HSN Code Matcher

Matches item descriptions to HSN codes using fuzzy string matching.
Suggests GST rates based on HSN classification.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from difflib import SequenceMatcher

try:
    from fuzzywuzzy import fuzz
    FUZZYWUZZY_AVAILABLE = True
except ImportError:
    print("Warning: fuzzywuzzy not installed. Using basic matching. Install with: pip install fuzzywuzzy")
    FUZZYWUZZY_AVAILABLE = False


class HSNMatcher:
    """Match item descriptions to HSN codes"""

    def __init__(self, hsn_db_path: Optional[str] = None):
        """
        Initialize HSN matcher with database

        Args:
            hsn_db_path: Path to HSN master JSON file
        """
        if hsn_db_path is None:
            # Default path relative to this file
            base_dir = Path(__file__).parent.parent
            hsn_db_path = base_dir / 'data' / 'hsn_master.json'

        self.hsn_db_path = Path(hsn_db_path)
        self.hsn_data = self._load_hsn_database()
        self.user_corrections = {}  # Store user corrections for learning

    def _load_hsn_database(self) -> List[Dict]:
        """Load HSN master database from JSON file"""
        if not self.hsn_db_path.exists():
            raise FileNotFoundError(
                f"HSN database not found at: {self.hsn_db_path}\n"
                f"Please create the HSN master file first."
            )

        with open(self.hsn_db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"✓ Loaded {len(data)} HSN codes from database")
        return data

    def suggest_hsn(self, item_description: str, top_n: int = 3) -> Dict:
        """
        Suggest HSN code for an item description

        Args:
            item_description: Item name/description from invoice
            top_n: Number of top matches to return

        Returns:
            Dictionary with best match and alternatives
        """
        if not item_description or not item_description.strip():
            return {
                'hsn_code': None,
                'gst_rate': None,
                'confidence': 0,
                'matches': []
            }

        item_description = item_description.lower().strip()

        # Check user corrections first (highest priority)
        if item_description in self.user_corrections:
            correction = self.user_corrections[item_description]
            return {
                'hsn_code': correction['hsn_code'],
                'gst_rate': correction['gst_rate'],
                'confidence': 100,  # User confirmed
                'matches': [correction],
                'source': 'user_correction'
            }

        # Find best matches
        matches = []

        for hsn_entry in self.hsn_data:
            score = self._calculate_match_score(item_description, hsn_entry)

            if score > 0:
                matches.append({
                    'hsn_code': hsn_entry['hsn'],
                    'description': hsn_entry['description'],
                    'gst_rate': hsn_entry['gst_rate'],
                    'confidence': score
                })

        # Sort by confidence (highest first)
        matches.sort(key=lambda x: x['confidence'], reverse=True)

        # Get top N matches
        top_matches = matches[:top_n]

        if not top_matches:
            return {
                'hsn_code': None,
                'gst_rate': None,
                'confidence': 0,
                'matches': []
            }

        # Return best match + alternatives
        best_match = top_matches[0]

        return {
            'hsn_code': best_match['hsn_code'],
            'gst_rate': best_match['gst_rate'],
            'confidence': best_match['confidence'],
            'matches': top_matches,
            'source': 'fuzzy_match'
        }

    def _calculate_match_score(self, item_description: str, hsn_entry: Dict) -> int:
        """
        Calculate match score (0-100) between item and HSN entry

        Uses multiple signals:
        1. Direct keyword match (highest priority)
        2. Fuzzy match with HSN description
        3. Partial word matches
        """
        item_description = item_description.lower()
        score = 0

        # 1. Check keyword matches (strong signal)
        keywords = hsn_entry.get('keywords', [])
        for keyword in keywords:
            keyword_lower = keyword.lower()

            # Exact keyword match in description
            if keyword_lower in item_description or item_description in keyword_lower:
                score = max(score, 90)  # High confidence

            # Fuzzy keyword match
            elif FUZZYWUZZY_AVAILABLE:
                keyword_score = fuzz.partial_ratio(keyword_lower, item_description)
                score = max(score, keyword_score)
            else:
                # Fallback to basic similarity
                keyword_score = self._simple_similarity(keyword_lower, item_description) * 100
                score = max(score, int(keyword_score))

        # 2. Match with HSN description
        hsn_desc = hsn_entry['description'].lower()

        if FUZZYWUZZY_AVAILABLE:
            desc_score = fuzz.partial_ratio(hsn_desc, item_description)
            score = max(score, desc_score - 10)  # Slight penalty vs keyword match
        else:
            desc_score = self._simple_similarity(hsn_desc, item_description) * 100
            score = max(score, int(desc_score) - 10)

        # 3. Boost score for multi-word matches
        item_words = set(item_description.split())
        for keyword in keywords:
            keyword_words = set(keyword.lower().split())
            common_words = item_words.intersection(keyword_words)
            if len(common_words) > 1:
                score = min(score + 15, 100)  # Boost for multiple word matches

        return int(score)

    def _simple_similarity(self, str1: str, str2: str) -> float:
        """
        Calculate simple string similarity (0.0 to 1.0)
        Fallback when fuzzywuzzy is not available
        """
        return SequenceMatcher(None, str1, str2).ratio()

    def learn_from_correction(self, item_description: str, correct_hsn: str, gst_rate: int):
        """
        Store user correction for future matching

        Args:
            item_description: Original item description
            correct_hsn: User-selected correct HSN code
            gst_rate: GST rate for the HSN code
        """
        item_description = item_description.lower().strip()

        self.user_corrections[item_description] = {
            'hsn_code': correct_hsn,
            'gst_rate': gst_rate,
            'description': item_description
        }

        print(f"✓ Learned: '{item_description}' → HSN {correct_hsn} ({gst_rate}%)")

    def save_corrections(self, output_path: str):
        """
        Save user corrections to JSON file for persistence

        Args:
            output_path: Path to save corrections
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.user_corrections, f, indent=2, ensure_ascii=False)

        print(f"✓ Saved {len(self.user_corrections)} corrections to {output_path}")

    def load_corrections(self, corrections_path: str):
        """
        Load previously saved user corrections

        Args:
            corrections_path: Path to corrections JSON file
        """
        corrections_path = Path(corrections_path)

        if not corrections_path.exists():
            print(f"No corrections file found at {corrections_path}")
            return

        with open(corrections_path, 'r', encoding='utf-8') as f:
            self.user_corrections = json.load(f)

        print(f"✓ Loaded {len(self.user_corrections)} corrections")

    def get_hsn_details(self, hsn_code: str) -> Optional[Dict]:
        """
        Get details for a specific HSN code

        Args:
            hsn_code: HSN code to lookup

        Returns:
            HSN entry details or None if not found
        """
        for hsn_entry in self.hsn_data:
            if hsn_entry['hsn'] == hsn_code:
                return hsn_entry

        return None

    def get_all_hsn_codes(self) -> List[str]:
        """Get list of all HSN codes in database"""
        return [entry['hsn'] for entry in self.hsn_data]

    def search_by_gst_rate(self, gst_rate: int) -> List[Dict]:
        """
        Find all HSN codes with a specific GST rate

        Args:
            gst_rate: GST rate (0, 5, 12, 18, 28)

        Returns:
            List of HSN entries with that rate
        """
        return [entry for entry in self.hsn_data if entry['gst_rate'] == gst_rate]


# Convenience function
def suggest_hsn(item_description: str, hsn_db_path: Optional[str] = None) -> Dict:
    """
    Suggest HSN code for item description (convenience function)

    Usage:
        from app.hsn_matcher import suggest_hsn
        result = suggest_hsn("Laptop Dell Inspiron")
        print(result)
    """
    matcher = HSNMatcher(hsn_db_path)
    return matcher.suggest_hsn(item_description)


# CLI for testing
if __name__ == '__main__':
    import sys

    print("HSN Matcher - Interactive Testing")
    print("=" * 60)

    matcher = HSNMatcher()

    # Test with command line argument
    if len(sys.argv) > 1:
        test_items = [' '.join(sys.argv[1:])]
    else:
        # Default test items
        test_items = [
            "Laptop Dell Inspiron 15",
            "iPhone 13 Pro",
            "Office Chair",
            "LED Bulb",
            "Consulting Services",
            "Software Development",
            "Rice",
            "Cement",
            "Printer HP LaserJet"
        ]

    print(f"\nTesting {len(test_items)} items:\n")

    for item in test_items:
        print(f"Item: {item}")
        result = matcher.suggest_hsn(item)

        if result['hsn_code']:
            print(f"  → HSN: {result['hsn_code']} | GST Rate: {result['gst_rate']}% | Confidence: {result['confidence']}%")

            # Show alternatives if available
            if len(result['matches']) > 1:
                print(f"  Alternatives:")
                for alt in result['matches'][1:]:
                    print(f"    - HSN {alt['hsn_code']}: {alt['description']} ({alt['gst_rate']}%) - {alt['confidence']}%")
        else:
            print(f"  → No match found")

        print()

    print("=" * 60)
    print("\n✓ Test completed!")
    print("\nTry it yourself:")
    print("  python hsn_matcher.py 'your item description here'")
