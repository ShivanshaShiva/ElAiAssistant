"""
Sanskrit NLP Module.
This module provides Sanskrit language processing functionality.
"""

import os
import json
import re
from kivy.logger import Logger

class SanskritNLP:
    """Provides Sanskrit language processing functionality."""
    
    def __init__(self, data_dir='data/sanskrit'):
        """
        Initialize the Sanskrit NLP processor.
        
        Args:
            data_dir (str): Directory to store data files
        """
        self.data_dir = data_dir
        self._init_data_dir()
        
        # Rules
        self.grammar_rules = []
        self.sandhi_rules = []
        self._load_rules()
        
        # Transliteration schemes
        self.transliteration_maps = {
            'iast_to_devanagari': {
                'a': 'अ', 'ā': 'आ', 'i': 'इ', 'ī': 'ई', 'u': 'उ', 'ū': 'ऊ',
                'ṛ': 'ऋ', 'ṝ': 'ॠ', 'ḷ': 'ऌ', 'e': 'ए', 'ai': 'ऐ', 'o': 'ओ', 'au': 'औ',
                'ka': 'क', 'kha': 'ख', 'ga': 'ग', 'gha': 'घ', 'ṅa': 'ङ',
                'ca': 'च', 'cha': 'छ', 'ja': 'ज', 'jha': 'झ', 'ña': 'ञ',
                'ṭa': 'ट', 'ṭha': 'ठ', 'ḍa': 'ड', 'ḍha': 'ढ', 'ṇa': 'ण',
                'ta': 'त', 'tha': 'थ', 'da': 'द', 'dha': 'ध', 'na': 'न',
                'pa': 'प', 'pha': 'फ', 'ba': 'ब', 'bha': 'भ', 'ma': 'म',
                'ya': 'य', 'ra': 'र', 'la': 'ल', 'va': 'व',
                'śa': 'श', 'ṣa': 'ष', 'sa': 'स', 'ha': 'ह',
                'aṃ': 'अं', 'aḥ': 'अः'
            },
            'devanagari_to_iast': {
                'अ': 'a', 'आ': 'ā', 'इ': 'i', 'ई': 'ī', 'उ': 'u', 'ऊ': 'ū',
                'ऋ': 'ṛ', 'ॠ': 'ṝ', 'ऌ': 'ḷ', 'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au',
                'क': 'ka', 'ख': 'kha', 'ग': 'ga', 'घ': 'gha', 'ङ': 'ṅa',
                'च': 'ca', 'छ': 'cha', 'ज': 'ja', 'झ': 'jha', 'ञ': 'ña',
                'ट': 'ṭa', 'ठ': 'ṭha', 'ड': 'ḍa', 'ढ': 'ḍha', 'ण': 'ṇa',
                'त': 'ta', 'थ': 'tha', 'द': 'da', 'ध': 'dha', 'न': 'na',
                'प': 'pa', 'फ': 'pha', 'ब': 'ba', 'भ': 'bha', 'म': 'ma',
                'य': 'ya', 'र': 'ra', 'ल': 'la', 'व': 'va',
                'श': 'śa', 'ष': 'ṣa', 'स': 'sa', 'ह': 'ha',
                'ं': 'ṃ', 'ः': 'ḥ'
            },
            'hk_to_iast': {
                'a': 'a', 'A': 'ā', 'i': 'i', 'I': 'ī', 'u': 'u', 'U': 'ū',
                'R': 'ṛ', 'RR': 'ṝ', 'lR': 'ḷ', 'e': 'e', 'ai': 'ai', 'o': 'o', 'au': 'au',
                'k': 'k', 'kh': 'kh', 'g': 'g', 'gh': 'gh', 'G': 'ṅ',
                'c': 'c', 'ch': 'ch', 'j': 'j', 'jh': 'jh', 'J': 'ñ',
                'T': 'ṭ', 'Th': 'ṭh', 'D': 'ḍ', 'Dh': 'ḍh', 'N': 'ṇ',
                't': 't', 'th': 'th', 'd': 'd', 'dh': 'dh', 'n': 'n',
                'p': 'p', 'ph': 'ph', 'b': 'b', 'bh': 'bh', 'm': 'm',
                'y': 'y', 'r': 'r', 'l': 'l', 'v': 'v',
                'z': 'ś', 'S': 'ṣ', 's': 's', 'h': 'h',
                'M': 'ṃ', 'H': 'ḥ'
            },
            'iast_to_hk': {
                'a': 'a', 'ā': 'A', 'i': 'i', 'ī': 'I', 'u': 'u', 'ū': 'U',
                'ṛ': 'R', 'ṝ': 'RR', 'ḷ': 'lR', 'e': 'e', 'ai': 'ai', 'o': 'o', 'au': 'au',
                'k': 'k', 'kh': 'kh', 'g': 'g', 'gh': 'gh', 'ṅ': 'G',
                'c': 'c', 'ch': 'ch', 'j': 'j', 'jh': 'jh', 'ñ': 'J',
                'ṭ': 'T', 'ṭh': 'Th', 'ḍ': 'D', 'ḍh': 'Dh', 'ṇ': 'N',
                't': 't', 'th': 'th', 'd': 'd', 'dh': 'dh', 'n': 'n',
                'p': 'p', 'ph': 'ph', 'b': 'b', 'bh': 'bh', 'm': 'm',
                'y': 'y', 'r': 'r', 'l': 'l', 'v': 'v',
                'ś': 'z', 'ṣ': 'S', 's': 's', 'h': 'h',
                'ṃ': 'M', 'ḥ': 'H'
            }
        }
    
    def _init_data_dir(self):
        """Initialize the data directory structure."""
        if not os.path.exists(self.data_dir):
            try:
                os.makedirs(self.data_dir)
                Logger.info(f"SanskritNLP: Created data directory at {self.data_dir}")
            except OSError as e:
                Logger.error(f"SanskritNLP: Failed to create data directory: {e}")
        
        # Create necessary files
        grammar_rules_file = os.path.join(self.data_dir, 'grammar_rules.json')
        sandhi_rules_file = os.path.join(self.data_dir, 'sandhi_rules.json')
        
        if not os.path.exists(grammar_rules_file):
            self._create_default_file(grammar_rules_file, [])
        
        if not os.path.exists(sandhi_rules_file):
            self._create_default_file(sandhi_rules_file, [])
    
    def _create_default_file(self, file_path, default_content):
        """Create a default file with the given content."""
        try:
            with open(file_path, 'w') as f:
                json.dump(default_content, f, indent=2)
            Logger.info(f"SanskritNLP: Created default file at {file_path}")
        except OSError as e:
            Logger.error(f"SanskritNLP: Failed to create default file: {e}")
    
    def _load_rules(self):
        """Load grammar and sandhi rules from files."""
        grammar_rules_file = os.path.join(self.data_dir, 'grammar_rules.json')
        sandhi_rules_file = os.path.join(self.data_dir, 'sandhi_rules.json')
        
        try:
            if os.path.exists(grammar_rules_file):
                with open(grammar_rules_file, 'r') as f:
                    self.grammar_rules = json.load(f)
            
            if os.path.exists(sandhi_rules_file):
                with open(sandhi_rules_file, 'r') as f:
                    self.sandhi_rules = json.load(f)
                    
            Logger.info(f"SanskritNLP: Loaded {len(self.grammar_rules)} grammar rules and {len(self.sandhi_rules)} sandhi rules")
        except (json.JSONDecodeError, OSError) as e:
            Logger.error(f"SanskritNLP: Failed to load rules: {e}")
    
    def _save_rules(self):
        """Save grammar and sandhi rules to files."""
        grammar_rules_file = os.path.join(self.data_dir, 'grammar_rules.json')
        sandhi_rules_file = os.path.join(self.data_dir, 'sandhi_rules.json')
        
        try:
            with open(grammar_rules_file, 'w') as f:
                json.dump(self.grammar_rules, f, indent=2)
            
            with open(sandhi_rules_file, 'w') as f:
                json.dump(self.sandhi_rules, f, indent=2)
                
            Logger.info(f"SanskritNLP: Saved {len(self.grammar_rules)} grammar rules and {len(self.sandhi_rules)} sandhi rules")
            return True
        except OSError as e:
            Logger.error(f"SanskritNLP: Failed to save rules: {e}")
            return False
    
    def transliterate(self, text, scheme_from='iast', scheme_to='devanagari'):
        """
        Transliterate text between different writing systems.
        
        Args:
            text (str): Text to transliterate
            scheme_from (str): Source scheme ('iast', 'hk', 'slp1', 'devanagari')
            scheme_to (str): Target scheme ('iast', 'hk', 'slp1', 'devanagari')
            
        Returns:
            dict: Result with 'success' and 'text' keys
        """
        if not text:
            return {'success': False, 'error': 'No text provided'}
        
        # Check supported schemes
        supported_schemes = ['iast', 'hk', 'devanagari']
        if scheme_from not in supported_schemes:
            return {'success': False, 'error': f'Unsupported source scheme: {scheme_from}'}
        
        if scheme_to not in supported_schemes:
            return {'success': False, 'error': f'Unsupported target scheme: {scheme_to}'}
        
        # If same scheme, return the text unchanged
        if scheme_from == scheme_to:
            return {'success': True, 'text': text}
        
        # Convert to IAST first (as intermediary)
        iast_text = text
        if scheme_from == 'hk':
            iast_text = self._convert_with_map(text, self.transliteration_maps['hk_to_iast'])
        elif scheme_from == 'devanagari':
            iast_text = self._convert_with_map(text, self.transliteration_maps['devanagari_to_iast'])
        
        # Convert from IAST to target scheme
        result_text = iast_text
        if scheme_to == 'hk':
            result_text = self._convert_with_map(iast_text, self.transliteration_maps['iast_to_hk'])
        elif scheme_to == 'devanagari':
            result_text = self._convert_with_map(iast_text, self.transliteration_maps['iast_to_devanagari'])
        
        return {'success': True, 'text': result_text}
    
    def _convert_with_map(self, text, conversion_map):
        """Convert text using a conversion map."""
        # Sort keys by length in descending order to avoid partial matches
        sorted_keys = sorted(conversion_map.keys(), key=len, reverse=True)
        
        result = text
        for key in sorted_keys:
            result = result.replace(key, conversion_map[key])
        
        return result
    
    def learn_grammar_rule(self, instruction):
        """
        Learn a new grammar rule from an instruction.
        
        Args:
            instruction (str): Natural language instruction describing the rule
            
        Returns:
            dict: Result with 'success', 'rule', and possibly 'error' keys
        """
        if not instruction:
            return {'success': False, 'error': 'No instruction provided'}
        
        # Simplified rule extraction (placeholder)
        # In a real system, this would use NLP to extract rule details
        # For example, finding patterns like "add a to b to form c"
        
        try:
            # Simple pattern matching for demonstration
            rule = {
                'id': len(self.grammar_rules) + 1,
                'description': instruction,
                'created_at': self._get_current_timestamp()
            }
            
            # Try to extract pattern and replacement
            pattern_match = re.search(r'when\s+(.+?)\s+becomes\s+(.+)', instruction, re.IGNORECASE)
            if pattern_match:
                rule['pattern'] = pattern_match.group(1).strip()
                rule['replacement'] = pattern_match.group(2).strip()
            
            # Add rule to collection
            self.grammar_rules.append(rule)
            
            # Save rules
            self._save_rules()
            
            return {'success': True, 'rule': rule}
        
        except Exception as e:
            Logger.error(f"SanskritNLP: Error learning grammar rule: {e}")
            return {'success': False, 'error': str(e)}
    
    def tokenize(self, text):
        """
        Tokenize Sanskrit text into words.
        
        Args:
            text (str): Sanskrit text to tokenize
            
        Returns:
            dict: Result with 'success', 'tokens', and possibly 'error' keys
        """
        if not text:
            return {'success': False, 'error': 'No text provided'}
        
        try:
            # Simple tokenization (placeholder)
            # In a real system, this would use proper Sanskrit tokenization rules
            # For now, we'll use spaces and punctuation
            tokens = re.findall(r'\b\w+\b', text)
            
            return {'success': True, 'tokens': tokens}
        
        except Exception as e:
            Logger.error(f"SanskritNLP: Error tokenizing text: {e}")
            return {'success': False, 'error': str(e)}
    
    def analyze_sandhi(self, text):
        """
        Analyze sandhi (word combinations) in Sanskrit text.
        
        Args:
            text (str): Sanskrit text to analyze
            
        Returns:
            dict: Result with 'success', 'analysis', and possibly 'error' keys
        """
        if not text:
            return {'success': False, 'error': 'No text provided'}
        
        try:
            # Simple sandhi analysis (placeholder)
            # In a real system, this would apply proper Sanskrit sandhi rules
            
            # Tokenize first
            tokens_result = self.tokenize(text)
            if not tokens_result['success']:
                return tokens_result
            
            tokens = tokens_result['tokens']
            
            # For now, just look for potential sandhi combinations based on vowel sequences
            # This is a very simplified approach
            analysis = []
            for i in range(len(tokens) - 1):
                if tokens[i].endswith(('a', 'i', 'u')) and tokens[i+1].startswith(('a', 'i', 'u')):
                    analysis.append({
                        'word1': tokens[i],
                        'word2': tokens[i+1],
                        'combined': tokens[i] + tokens[i+1],
                        'type': 'vowel_sandhi'
                    })
            
            return {'success': True, 'analysis': analysis}
        
        except Exception as e:
            Logger.error(f"SanskritNLP: Error analyzing sandhi: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_grammar_rules(self):
        """
        Get all grammar rules.
        
        Returns:
            list: List of grammar rules
        """
        return self.grammar_rules
    
    def get_sandhi_rules(self):
        """
        Get all sandhi rules.
        
        Returns:
            list: List of sandhi rules
        """
        return self.sandhi_rules
    
    def _get_current_timestamp(self):
        """Get current timestamp as a string."""
        from datetime import datetime
        return datetime.now().isoformat()