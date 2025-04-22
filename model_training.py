import numpy as np
from sklearn.linear_model import LogisticRegression
import joblib

# Sample training data (expected vs actual marks)
X_train = np.array([[20, 22], [30, 30], [50, 48], [40, 45]])  # [expected, actual]
y_train = np.array([1, 0, 1, 1])  # 0 = Correct, 1 = Error

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save trained model
joblib.dump(model, "mark_validation_model.pkl")
print("✅ Model trained & saved!")
