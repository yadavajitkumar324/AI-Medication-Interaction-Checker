import json
from difflib import get_close_matches
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

class MedicalInteractionChecker:
    def __init__(self):
        self.load_drug_database()
        self.load_symptom_database()
        self.initialize_similarity_matcher()
        
    def load_drug_database(self):
        """Initialize with sample drug interaction data"""
        self.drug_db = {
            "aspirin": {
                "interactions": ["ibuprofen", "warfarin", "clopidogrel"],
                "warnings": "May increase bleeding risk with other blood thinners",
                "type": "NSAID"
            },
            "ibuprofen": {
                "interactions": ["aspirin", "lithium", "methotrexate"],
                "warnings": "May reduce effectiveness of blood pressure medications",
                "type": "NSAID"
            },
            "warfarin": {
                "interactions": ["aspirin", "ibuprofen", "vitamin K"],
                "warnings": "Many drug and food interactions - requires careful monitoring",
                "type": "Anticoagulant"
            },
            "paracetamol": {
                "interactions": ["alcohol"],
                "warnings": "Alcohol may increase liver damage risk",
                "type": "Analgesic"
            },
            "simvastatin": {
                "interactions": ["grapefruit", "erythromycin"],
                "warnings": "Grapefruit may increase side effects",
                "type": "Statin"
            }
        }
    
    def load_symptom_database(self):
        """Initialize symptom database"""
        self.symptom_db = {
            "headache": ["aspirin", "ibuprofen", "paracetamol"],
            "fever": ["paracetamol", "ibuprofen"],
            "pain": ["aspirin", "ibuprofen", "paracetamol"],
            "inflammation": ["ibuprofen", "aspirin"],
            "blood clot prevention": ["warfarin", "aspirin"]
        }
    
    def initialize_similarity_matcher(self):
        """Initialize TF-IDF vectorizer for similarity matching"""
        self.vectorizer = TfidfVectorizer()
        self.drug_names = list(self.drug_db.keys())
        self.tfidf_matrix = self.vectorizer.fit_transform(self.drug_names)
    
    def find_closest_drug(self, drug_name):
        """Find the closest matching drug name in the database"""
        query_vec = self.vectorizer.transform([drug_name.lower()])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix)
        best_match_idx = similarities.argmax()
        best_match = self.drug_names[best_match_idx]
        
        if similarities[0, best_match_idx] > 0.6:  # Similarity threshold
            return best_match
        return None
    
    def check_interaction(self, drug1, drug2):
        """Check for interaction between two drugs"""
        drug1_match = self.find_closest_drug(drug1)
        drug2_match = self.find_closest_drug(drug2)
        
        if not drug1_match or not drug2_match:
            return None, None, "One or both drugs not recognized in our database."
        
        interactions = []
        warnings = []
        
        if drug2_match in self.drug_db.get(drug1_match, {}).get("interactions", []):
            interactions.append(f"{drug1_match} may interact with {drug2_match}")
            warnings.append(self.drug_db[drug1_match]["warnings"])
        
        if drug1_match in self.drug_db.get(drug2_match, {}).get("interactions", []):
            interactions.append(f"{drug2_match} may interact with {drug1_match}")
            warnings.append(self.drug_db[drug2_match]["warnings"])
        
        if not interactions:
            return drug1_match, drug2_match, "No known interactions found between these medications."
        
        return drug1_match, drug2_match, {
            "interactions": interactions,
            "warnings": warnings
        }
    
    def get_drug_info(self, drug_name):
        """Get information about a specific drug"""
        drug_match = self.find_closest_drug(drug_name)
        if not drug_match:
            return None, "Drug not recognized in our database."
        
        return drug_match, self.drug_db.get(drug_match, {})
    
    def suggest_medication(self, symptom):
        """Suggest medications for a given symptom"""
        symptom_lower = symptom.lower()
        closest_symptoms = get_close_matches(symptom_lower, self.symptom_db.keys(), n=1, cutoff=0.5)
        
        if not closest_symptoms:
            return None, "No medication suggestions available for this symptom."
        
        closest_symptom = closest_symptoms[0]
        medications = self.symptom_db[closest_symptom]
        
        # Get additional info for each medication
        med_info = []
        for med in medications:
            match = self.find_closest_drug(med)
            if match:
                med_info.append({
                    "name": match,
                    "type": self.drug_db[match].get("type", "Unknown"),
                    "warnings": self.drug_db[match].get("warnings", "None")
                })
        
        return closest_symptom, med_info