import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai.classifier import TextClassifier 
from ai.slmclass import FormalityScorer
import pandas as pd
import joblib
import random
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
#self.slm_model_polish=self.load_model("English","Small Language Model (SLM)")
 #       self.slm_model_english=self.load_model("Polish","Small Language Model (SLM)")
       
def test_slm(selected_language, save_model=False):
    model_path = f'ai/models/Small_Language_Model_(SLM)_{selected_language}.pkl' 
    print('loading csv')
    clf = joblib.load(model_path)
    if selected_language == 'Polish':
        df = pd.read_csv('extracted_data/pl_formal.csv.gz', compression='gzip')
        df_temp = pd.read_csv('extracted_data/pl_informal.csv.gz', compression='gzip')
    else:
        df = pd.read_csv('extracted_data/en_formal.csv.gz', compression='gzip')
        df_temp = pd.read_csv('extracted_data/en_informal.csv.gz', compression='gzip')
    df = pd.concat([df, df_temp])
    print(f'loaded {len(df)} values')
    
    # Sample for testing
    seed = random.randint(0, 2**32 - 1)
    samples_per_class = 100000  # Adjust as needed
    df = df.groupby('formality', group_keys=False).apply(
        lambda x: x.sample(min(len(x), samples_per_class), random_state=seed)
    )
    print(f'Using {len(df)} samples')
    
    X = df['text']
    y = df['formality']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=seed, stratify=y
    )
    
    X_test = X_test[0:100]
    y_test=y_test[0:100]
    y_pred=[]
    for text in X_test:
        print("xtest prompt")
        print(text)
        clf.prompt([text]) 
        prediction = clf.predict([text])
        y_pred.append(prediction)



    #clf.fit(X_train, y_train)
    
    #y_pred = best_model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    print(f'Accuracy: {accuracy:.4f}')
    print('Classification Report:')
    print(report)
       
if __name__=="__main__":
    test_slm("Polish")