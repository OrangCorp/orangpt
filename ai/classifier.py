"""Formality classification logic."""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import joblib

def create_classifier(save_model=False, model_path='ai/models/formality_classifier.pkl'):
    print('loading csv')
    df = pd.read_csv('extracted_data/en_formal.csv.gz', compression='gzip')
    df_temp = pd.read_csv('extracted_data/en_informal.csv.gz', compression='gzip')
    df = pd.concat([df, df_temp])
    
    # Sample for testing
    samples_per_class = 20000  # Adjust as needed
    df = df.groupby('formality', group_keys=False).apply(
        lambda x: x.sample(min(len(x), samples_per_class), random_state=42)
    )
    print(f'Using {len(df)} samples')
    
    print('vectorizing')
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
    X = vectorizer.fit_transform(df['text'])
    y = df['formality']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    print('training')
    clf = SVC(kernel='linear')
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    print(f'Accuracy: {accuracy:.4f}')
    print('Classification Report:')
    print(report)
    
    if save_model:
        # Save both the model and vectorizer together
        model_data = {
            'classifier': clf,
            'vectorizer': vectorizer,
            'accuracy': accuracy
        }
        joblib.dump(model_data, model_path)
        print(f'Model saved to {model_path}')
        
        # Save metadata separately (optional, human-readable)
        with open('ai/models/model_info.txt', 'w') as f:
            f.write(f'Model saved: {model_path}\n')
            f.write(f'Accuracy: {accuracy:.4f}\n')
            f.write(f'Training samples: {X_train.shape[0]}\n')
            f.write(f'Features: {X_train.shape[1]}\n')
            f.write('Classification Report:\n')
            f.write(report)
    
    return clf, vectorizer


def load_model(model_path='ai/models/formality_classifier.pkl'):
    """Load the saved model and vectorizer"""
    try:
        model_data = joblib.load(model_path)
        print(f'Model loaded from {model_path}')
        print(f'Model accuracy (from training): {model_data["accuracy"]:.4f}')
        return model_data['classifier'], model_data['vectorizer']
    except FileNotFoundError:
        print(f'Error: Model file {model_path} not found')
        clf, vectorizer = create_classifier(True, model_path)
        return clf, vectorizer


def classify_tone(text: str) -> str:
    clf, vectorizer = load_model()
    """Make predictions on new text"""
    if clf is None or vectorizer is None:
        print("Error: Model not loaded")
        return None
    
    # Transform the text using the SAME vectorizer
    text_vectorized = vectorizer.transform([text])
    prediction = clf.predict(text_vectorized)[0]
    
    # Get probability scores if you want confidence
    if hasattr(clf, 'decision_function'):
        confidence = clf.decision_function(text_vectorized)[0]
        print(f'Prediction: {prediction}, Confidence: {abs(confidence):.4f}')
    if prediction == -1:
        return 'informal'
    return 'formal'