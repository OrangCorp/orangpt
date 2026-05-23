"""Formality classification logic."""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
import joblib
import random
from lime.lime_text import LimeTextExplainer

def create_classifier(selected_language, selected_model, save_model=False):
    model_path = f'ai/models/{selected_model}_{selected_language}.pkl'
    print('loading csv')
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
    
    print('training')
    #clf = SVC(kernel='linear') #slow to generate
    #clf = RandomForestClassifier(n_estimators=100, max_features='sqrt') #slow to generate
    clf1 = SGDClassifier(loss='log_loss', penalty='l2', max_iter=1000, tol=1e-3)
    clf2 = LogisticRegression(max_iter=1000, solver='liblinear')
    clf3 = MultinomialNB()
    

    clf = VotingClassifier(
        estimators=[
            ('Stochastic Gradient Descent', clf1),
            ('Logistic Regression', clf2),
            ('Multinomial Naive Bayes', clf3)
        ],
        voting='soft'
    )

    param_grid = {
        'vectorizer__max_df': [0.7, 0.8, 0.9],
        'vectorizer__ngram_range': [(1, 1), (1, 2), (1, 3)],
        'classifier__Stochastic Gradient Descent__alpha': [0.00001, 0.0001, 0.001, 0.01],
        'classifier__Logistic Regression__C': [0.1, 1.0, 10.0, 100.0],
        'classifier__Multinomial Naive Bayes__alpha': [0.0001, 0.001, 0.01, 0.1, 1.0]
    }

    # Create pipeline
    pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer()),
        ('classifier', clf)  # Your VotingClassifier
    ])

    # Run grid search
    grid_search = GridSearchCV(
        pipeline, 
        param_grid, 
        cv=3,  # 3-fold cross-validation
        scoring='accuracy',
        n_jobs=-3,
        verbose=3 
    )
    grid_search.fit(X_train, y_train)

    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Best score: {grid_search.best_score_}")

    # Get best model
    best_model = grid_search.best_estimator_

    #clf.fit(X_train, y_train)
    
    y_pred = best_model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    print(f'Accuracy: {accuracy:.4f}')
    print('Classification Report:')
    print(report)
    
    if save_model:
        # Save both the model and vectorizer together
        joblib.dump(best_model, model_path)
        print(f'Model saved to {model_path}')
        
        # Save metadata separately (optional, human-readable)
        with open(f'ai/models/{selected_model}_{selected_language}_info.txt', 'w') as f:
            f.write(f"Best parameters: {grid_search.best_params_}")
            f.write(f'Model saved: {model_path}\n')
            f.write(f'Accuracy: {accuracy:.4f}\n')
            f.write(f'Training samples: {X_train.shape[0]}\n')
            f.write(f'Features: {best_model.named_steps['vectorizer'].get_feature_names_out().shape[0]}\n')
            f.write(f'Random State: {seed}\n')
            f.write('Classification Report:\n')
            f.write(report)
    
    return best_model


def load_model(selected_language, selected_model):
    """Load the saved model and vectorizer"""
    selected_model = selected_model.replace(" ", "_")
    model_path = f'ai/models/{selected_model}_{selected_language}.pkl'
    try:
        clf = joblib.load(model_path)
        print(f'Model loaded from {model_path}')
        return clf
    except FileNotFoundError:
        print(f'Error: Model file {model_path} not found')
        if selected_model == "Standard_Classifier":
            clf = create_classifier(selected_language, selected_model, True)
            return clf
        else:
            raise NotImplementedError


def classify_tone(text: str, selected_language: str, selected_model: str) -> str:
    clf = load_model(selected_language, selected_model)
    """Make predictions on new text"""
    if clf is NotImplemented:
        print("Error: Model not loaded")
        return None
    
    # Transform the text using the SAME vectorizer
    prediction = clf.predict([text])[0]
    
    # Get probability scores if you want confidence
    
    confidence = max(clf.predict_proba([text])[0])

    print(f'Prediction: {prediction}, Confidence: {confidence}')
    if prediction == -1:
        return 'informal', confidence
    return 'formal', confidence

def get_highlighted_words(text, selected_language, selected_model, fraction_of_words=0.33, min_number_of_words=1, max_number_of_words=10):
    clf = load_model(selected_language, selected_model)
    def predict_proba_for_lime(input_text):
        return clf.predict_proba(input_text)

    # Create the LIME explainer
    # class_names should match your target: ['informal', 'formal']
    explainer = LimeTextExplainer(class_names=["informal", "formal"])

    number_of_words = len(text.split())
    number_of_words = max(min_number_of_words, int(number_of_words*fraction_of_words))
    number_of_words = min(number_of_words, max_number_of_words)

    # Generate the explanation
    exp = explainer.explain_instance(
        text,
        predict_proba_for_lime,
        num_features=number_of_words  # Show top 5 contributing words
    )

    # list [(word,value)]
    return exp.as_list()