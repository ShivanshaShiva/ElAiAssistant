"""
Sanskrit NLP Module.
This module provides utilities for processing Sanskrit text.
"""

import os
import re
import json
import string
from typing import List, Dict, Tuple, Optional, Any, Union
from datetime import datetime

from kivy.logger import Logger


class SanskritNLP:
    """
    Sanskrit Natural Language Processing Utility.
    Provides functions for Sanskrit transliteration, tokenization,
    sandhi analysis, and grammar rule learning.
    """
    
    def __init__(self, rules_path: str = None):
        """
        Initialize the Sanskrit NLP processor.
        
        Args:
            rules_path (str): Path to the grammar rules file (JSON)
        """
        self.rules_path = rules_path or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            '..', '..', 'data', 'sanskrit_rules.json'
        )
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.rules_path), exist_ok=True)
        
        # Load grammar rules
        self.rules = self._load_rules()
    
    def _load_rules(self) -> Dict:
        """
        Load grammar rules from file.
        
        Returns:
            Dict: Dictionary of grammar rules
        """
        try:
            if os.path.exists(self.rules_path):
                with open(self.rules_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Create default rules structure
                default_rules = {
                    "sandhi": {},
                    "vibhakti": {},
                    "noun_declensions": {},
                    "verb_conjugations": {},
                    "custom_rules": {}
                }
                
                # Write default rules to file
                with open(self.rules_path, 'w', encoding='utf-8') as f:
                    json.dump(default_rules, f, indent=2)
                
                return default_rules
        except Exception as e:
            Logger.error(f"SanskritNLP: Failed to load rules: {e}")
            return {
                "sandhi": {},
                "vibhakti": {},
                "noun_declensions": {},
                "verb_conjugations": {},
                "custom_rules": {}
            }
    
    def _save_rules(self) -> bool:
        """
        Save grammar rules to file.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(self.rules_path, 'w', encoding='utf-8') as f:
                json.dump(self.rules, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            Logger.error(f"SanskritNLP: Failed to save rules: {e}")
            return False
    
    def transliterate(self, text: str, to_script: str = 'devanagari') -> str:
        """
        Transliterate text between Latin (IAST) and Devanagari.
        
        Args:
            text (str): The text to transliterate
            to_script (str): Target script ('devanagari' or 'latin')
            
        Returns:
            str: Transliterated text
        """
        # Mapping from Latin (IAST) to Devanagari
        iast_to_devanagari = {
            'a': 'अ', 'ā': 'आ', 'i': 'इ', 'ī': 'ई', 'u': 'उ', 'ū': 'ऊ',
            'e': 'ए', 'ai': 'ऐ', 'o': 'ओ', 'au': 'औ',
            'ṛ': 'ऋ', 'ṝ': 'ॠ', 'ḷ': 'ऌ', 'ḹ': 'ॡ',
            'k': 'क्', 'kh': 'ख्', 'g': 'ग्', 'gh': 'घ्', 'ṅ': 'ङ्',
            'c': 'च्', 'ch': 'छ्', 'j': 'ज्', 'jh': 'झ्', 'ñ': 'ञ्',
            'ṭ': 'ट्', 'ṭh': 'ठ्', 'ḍ': 'ड्', 'ḍh': 'ढ्', 'ṇ': 'ण्',
            't': 'त्', 'th': 'थ्', 'd': 'द्', 'dh': 'ध्', 'n': 'न्',
            'p': 'प्', 'ph': 'फ्', 'b': 'ब्', 'bh': 'भ्', 'm': 'म्',
            'y': 'य्', 'r': 'र्', 'l': 'ल्', 'v': 'व्',
            'ś': 'श्', 'ṣ': 'ष्', 's': 'स्', 'h': 'ह्',
            'ṃ': 'ं', 'ḥ': 'ः', '\'': 'ऽ',
            ' ': ' ', '.': '।', ',': ',', '\n': '\n'
        }
        
        # Mapping from Devanagari to Latin (IAST)
        # This is simplified and will need improvement for a real application
        devanagari_to_iast = {v: k for k, v in iast_to_devanagari.items() if len(k) == 1}
        devanagari_to_iast.update({
            'अ': 'a', 'आ': 'ā', 'इ': 'i', 'ई': 'ī', 'उ': 'u', 'ऊ': 'ū', 
            'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au',
            'ऋ': 'ṛ', 'ॠ': 'ṝ', 'ऌ': 'ḷ', 'ॡ': 'ḹ',
            'क': 'ka', 'ख': 'kha', 'ग': 'ga', 'घ': 'gha', 'ङ': 'ṅa',
            'च': 'ca', 'छ': 'cha', 'ज': 'ja', 'झ': 'jha', 'ञ': 'ña',
            'ट': 'ṭa', 'ठ': 'ṭha', 'ड': 'ḍa', 'ढ': 'ḍha', 'ण': 'ṇa',
            'त': 'ta', 'थ': 'tha', 'द': 'da', 'ध': 'dha', 'न': 'na',
            'प': 'pa', 'फ': 'pha', 'ब': 'ba', 'भ': 'bha', 'म': 'ma',
            'य': 'ya', 'र': 'ra', 'ल': 'la', 'व': 'va',
            'श': 'śa', 'ष': 'ṣa', 'स': 'sa', 'ह': 'ha',
            'ं': 'ṃ', 'ः': 'ḥ', 'ऽ': '\'',
            ' ': ' ', '।': '.', ',': ',', '\n': '\n'
        })
        
        result = ""
        
        if to_script == 'devanagari':
            # Latin to Devanagari
            i = 0
            while i < len(text):
                # Check for two-character matches first
                if i < len(text) - 1 and text[i:i+2] in iast_to_devanagari:
                    # Get the Devanagari equivalent
                    devanagari_char = iast_to_devanagari[text[i:i+2]]
                    # Add to result
                    result += devanagari_char
                    # Skip the next character as it's part of the current mapping
                    i += 2
                # Then check for single-character matches
                elif text[i] in iast_to_devanagari:
                    # Get the Devanagari equivalent
                    devanagari_char = iast_to_devanagari[text[i]]
                    # Add to result
                    result += devanagari_char
                    i += 1
                else:
                    # Character not in mapping, just add it as is
                    result += text[i]
                    i += 1
            
            # Process the result for correct Devanagari rendering
            # Replace implicit 'a' vowels
            result = result.replace('्अ', '')
            
            # Add inherent 'a' vowel to consonants not followed by vowel or virama
            vowel_markers = ['ा', 'ि', 'ी', 'ु', 'ू', 'े', 'ै', 'ो', 'ौ', 'ृ', 'ॄ', 'ॢ', 'ॣ', '्']
            chars = list(result)
            i = 0
            while i < len(chars):
                if chars[i].endswith('्') and i < len(chars) - 1 and chars[i+1] not in vowel_markers:
                    chars[i] = chars[i][:-1]  # Remove virama
                i += 1
            
            result = ''.join(chars)
            
        else:
            # Devanagari to Latin
            # This is a simplified conversion that needs improvement
            for char in text:
                if char in devanagari_to_iast:
                    result += devanagari_to_iast[char]
                else:
                    result += char
        
        return result
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize Sanskrit text into words.
        
        Args:
            text (str): Sanskrit text to tokenize
            
        Returns:
            List[str]: List of tokens (words)
        """
        # Basic whitespace and punctuation-based tokenization
        # For a real application, this would need to be much more sophisticated
        text = text.replace('।', ' । ')
        text = text.replace(',', ' , ')
        text = text.replace('.', ' . ')
        text = text.replace('!', ' ! ')
        text = text.replace('?', ' ? ')
        
        # Split by whitespace
        tokens = text.split()
        
        # Filter out empty tokens
        tokens = [token for token in tokens if token.strip()]
        
        return tokens
    
    def analyze_sandhi(self, compound: str) -> List[Dict[str, str]]:
        """
        Analyze Sanskrit sandhi (euphonic combination) in a compound word.
        
        Args:
            compound (str): The compound word to analyze
            
        Returns:
            List[Dict[str, str]]: List of possible sandhi analyses
        """
        # This is a placeholder implementation
        # A real implementation would use rule-based or ML-based analysis
        
        # Check if we have this compound in our rules
        if compound in self.rules["sandhi"]:
            return self.rules["sandhi"][compound]
        
        # Basic analysis based on common patterns
        # This is very rudimentary and would need significant improvement
        results = []
        
        # Check for visarga sandhi
        visarga_match = re.search(r'([aāiīuūeaioauṛṝḷḹ])([ḥ]?)([aāiīuūeaioauṛṝḷḹ])', compound)
        if visarga_match:
            groups = visarga_match.groups()
            first_part = compound[:visarga_match.start()]
            second_part = compound[visarga_match.end():]
            
            # Visarga sandhi: aḥ + a = o
            if groups[0] == 'a' and (not groups[1] or groups[1] == 'ḥ') and groups[2] == 'a':
                results.append({
                    "type": "visarga_sandhi",
                    "components": [f"{first_part}aḥ", f"{second_part}"],
                    "rule": "aḥ + a -> o",
                    "confidence": 0.8
                })
        
        # If no results found, return a generic analysis
        if not results:
            # Try to find potential word boundaries
            vowels = 'aāiīuūeaioauṛṝḷḹ'
            for i in range(1, len(compound)):
                if compound[i] in vowels and compound[i-1] in vowels:
                    results.append({
                        "type": "generic_sandhi",
                        "components": [compound[:i], compound[i:]],
                        "rule": "Potential vowel sandhi",
                        "confidence": 0.5
                    })
        
        # If still no results, offer a simple split
        if not results:
            mid = len(compound) // 2
            results.append({
                "type": "unknown",
                "components": [compound[:mid], compound[mid:]],
                "rule": "Arbitrary split (unknown sandhi rule)",
                "confidence": 0.1
            })
        
        return results
    
    def add_custom_rule(self, rule_type: str, name: str, pattern: str, 
                      explanation: str, examples: List[str]) -> bool:
        """
        Add a custom grammar rule.
        
        Args:
            rule_type (str): Type of rule ('sandhi', 'vibhakti', etc.)
            name (str): Name of the rule
            pattern (str): Pattern or formula of the rule
            explanation (str): Explanation of the rule
            examples (List[str]): Examples demonstrating the rule
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create rule entry
            rule = {
                "name": name,
                "pattern": pattern,
                "explanation": explanation,
                "examples": examples,
                "created": datetime.now().isoformat()
            }
            
            # Add to appropriate section
            if rule_type not in self.rules:
                self.rules[rule_type] = {}
            
            if "custom_rules" not in self.rules[rule_type]:
                self.rules[rule_type]["custom_rules"] = {}
            
            self.rules[rule_type]["custom_rules"][name] = rule
            
            # Save to file
            return self._save_rules()
            
        except Exception as e:
            Logger.error(f"SanskritNLP: Failed to add custom rule: {e}")
            return False
    
    def get_grammar_rules(self, rule_type: str = None) -> Dict:
        """
        Get grammar rules of a specific type or all rules.
        
        Args:
            rule_type (str): Type of rules to get (None for all)
            
        Returns:
            Dict: Dictionary of grammar rules
        """
        if rule_type:
            return self.rules.get(rule_type, {})
        return self.rules
    
    def get_noun_declension(self, noun: str, gender: str = None) -> Dict:
        """
        Get the declension table for a Sanskrit noun.
        
        Args:
            noun (str): The noun to decline
            gender (str): Gender of the noun ('m', 'f', 'n')
            
        Returns:
            Dict: Declension table for the noun
        """
        # Check if we have this noun in our rules
        if noun in self.rules.get("noun_declensions", {}):
            return self.rules["noun_declensions"][noun]
        
        # This is a placeholder for a more sophisticated implementation
        # A real implementation would use proper morphological analysis
        
        # Create an empty declension table
        declension = {
            "word": noun,
            "gender": gender or "unknown",
            "cases": {
                "nominative": {
                    "singular": f"{noun}ḥ",
                    "dual": f"{noun}au",
                    "plural": f"{noun}āḥ"
                },
                "accusative": {
                    "singular": f"{noun}am",
                    "dual": f"{noun}au",
                    "plural": f"{noun}ān"
                },
                "instrumental": {
                    "singular": f"{noun}ena",
                    "dual": f"{noun}ābhyām",
                    "plural": f"{noun}aiḥ"
                },
                "dative": {
                    "singular": f"{noun}āya",
                    "dual": f"{noun}ābhyām",
                    "plural": f"{noun}ebhyaḥ"
                },
                "ablative": {
                    "singular": f"{noun}āt",
                    "dual": f"{noun}ābhyām",
                    "plural": f"{noun}ebhyaḥ"
                },
                "genitive": {
                    "singular": f"{noun}asya",
                    "dual": f"{noun}ayoḥ",
                    "plural": f"{noun}ānām"
                },
                "locative": {
                    "singular": f"{noun}e",
                    "dual": f"{noun}ayoḥ",
                    "plural": f"{noun}eṣu"
                },
                "vocative": {
                    "singular": f"{noun}a",
                    "dual": f"{noun}au",
                    "plural": f"{noun}āḥ"
                }
            }
        }
        
        return declension