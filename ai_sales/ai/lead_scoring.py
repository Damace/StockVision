import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib


def train_lead_scoring_model():
    from customers.models import Customer  # Move the import here

    # Collect historical data
    data = []
    customers = Customer.objects.all()
    
    for customer in customers:
        total_orders = Order.objects.filter(customer=customer).count()
        total_spent = Order.objects.filter(customer=customer).aggregate(models.Sum('total_amount'))['total_amount__sum'] or 0
        data.append([total_orders, total_spent])

    if not data:
        return

    df = pd.DataFrame(data, columns=['total_orders', 'total_spent'])
    df['converted'] = np.random.randint(0, 2, df.shape[0])  # Fake conversion labels for training

    X = df[['total_orders', 'total_spent']]
    y = df['converted']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save the trained model
    joblib.dump(model, 'ai/lead_scoring_model.pkl')
    print("Lead scoring model trained and saved.")
