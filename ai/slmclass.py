#!/usr/bin/env python3
import os
os.environ['HF_HUB_DISABLE_FILE_LOCKING'] = '1'
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'

import torch
import re
import json
import pickle
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
from sklearn.base import BaseEstimator, RegressorMixin

class FormalityScorer:
    """Core scorer - this gets saved in the pickle"""
    def __init__(self, model_name="Qwen/Qwen2.5-1.5B-Instruct"):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.tokenizer = None
        self._is_loaded = False
        self.last_response=None
        self.loaded_data=None
        
    def load_model(self):
        """Load model only if not already loaded"""
        if not self._is_loaded:
            print(f"Loading {self.model_name}...")
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                device_map="auto",
                torch_dtype=torch.float16,
            )
            self._is_loaded = True
            print("Model loaded!")
            if torch.cuda.is_available():
                print(f"VRAM used: {torch.cuda.memory_allocated()/1024**3:.2f} GB")
    
    def score_formality(self, text):
        """Score a single text"""
        self.load_model()  # Ensures model is loaded

        messages = [
    {
        "role": "system", 
        "content": '''You are a formality scoring tool. Rate text from 0.0 (very casual) to 1.0 (very formal). Include up to 5 important words that influenced your rating, and also rate them  from 0.0 (very casual) to 1.0 (very formal) . Reply ONLY with a JSON object, no other text.'''
    },
    {
        "role": "user",
        "content": 'Rate this text: "hey wassup bro how u doin"'
    },
    {
        "role": "assistant",
        "content": '{"formality": 0.1, "important_words": [["wassup", 0.05], ["bro", 0.1], ["u", 0.15], ["doin", 0.1]]}'
    },
    {
        "role": "user",
        "content": 'Rate this text: "I would like to formally request your presence at the ceremony"'
    },
    {
        "role": "assistant",
        "content": '{"formality": 0.95, "important_words": [["formally", 0.9], ["request", 0.85], ["presence", 0.95], ["ceremony", 0.9]]}'
    },
    {
        "role": "user",
        "content": 'Rate this text: "The meeting is scheduled for tomorrow at 3pm"'
    },
    {
        "role": "assistant",
        "content": '{"formality": 0.5, "important_words": [["meeting", 0.5], ["scheduled", 0.55], ["tomorrow", 0.4]]}'
    },
    {
        "role": "user", 
        "content": f'Rate this text: "{text}"'
    }
]
     #   
    #    messages = [
   #         {
  #              "role": "system", 
         #       "content": '''You are a formality scoring tool. Rate text from 0.0 (very casual) to 1.0 (very formal). Include important words that influenced your rating. Reply ONLY with a JSON object (in the format of {"formality": [formality_rating], "important_words":[list of [important word,the word's formality rating] ]}), no other text.'''
         #   },
         #   {
         #       "role": "user", 
         #       "content": f'Rate this text: "{text}"'
        #    }
       # ]



        
        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=140,
                temperature=0.3,
                do_sample=False,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
        
        response = self.tokenizer.decode(
            outputs[0][inputs.input_ids.shape[1]:], 
            skip_special_tokens=True
        ).strip()
        print("raw response:" + response)
        return response
        # Parse JSON
        json_match = re.search(r'\{[^}]*\}', response)
        if json_match:
            try:
                data = json.loads(json_match.group(0))
                if 'formality' in data:
                    score = float(data['formality'])
                    score = min(max(score, 0.0), 1.0)
                    words = data.get('important_words', [])
                    return score, words
            except (json.JSONDecodeError, ValueError) as e:
                print(f"JSON parse error: {e}")
        
        # Fallback
        numbers = re.findall(r'(\d+\.?\d*)', response)
        if numbers:
            score = float(numbers[0])
            if score > 1.0:
                score = score / 100.0
            return min(max(score, 0.0), 1.0), []
        
        return 0.5, []
    def prompt(self,text):
        got_valid_r=False
        invalid_responses=0
        while(not got_valid_r):
            

            self.last_response=self.score_formality(text)
            #data = json.loads(self.last_response)
            #word[1]=(word[1]-0.5)*2
            try:   
                data = json.loads(self.last_response)
                test = data["important_words"]
                for word in data["important_words"]:
                    word[1]=(word[1]-0.5)*2

                got_valid_r=True
            except Exception:
                invalid_responses+=1 
            if(invalid_responses>=5):
                data= json.loads('{"formality": 0.5, "important_words": [["encountered", -1.0], ["an", 0.0], ["error", 1.0]]}')
                got_valid_r=True
            
        self.loaded_data= data
        return self.last_response

    def predict(self,compatarg):
      if(self.loaded_data['formality']>0.5):
        return 1
      return -1
    def predict_proba(self,compatarg):
        return [1-self.loaded_data['formality'],self.loaded_data['formality']]

    def __getstate__(self):
        """Custom pickle: save everything EXCEPT the actual model"""
        state = self.__dict__.copy()
        # Remove heavy model objects before pickling
        state['model'] = None
        state['tokenizer'] = None
        state['_is_loaded'] = False
        return state
    
    def __setstate__(self, state):
        """Custom unpickle: restore state but mark model as not loaded"""
        self.__dict__.update(state)
        # Model will be loaded on first use

if __name__ == '__main__': 
 # import pickle

  # Save your scorer
  scorer = FormalityScorer()
  print(scorer.score_formality("Please review and thank you for your regards"))
  print(scorer.score_formality(" hey bro this is gonna be awesome!"))
  print(scorer.score_formality(" This sentence has neutral wording"))

  with open('Small_Language_Model_(SLM)_English.pkl', 'wb') as f:
    pickle.dump(scorer, f)
