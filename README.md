### Baseline Model Summary

- **Model**: XGBoostClassifier
- **Data**: 100k simulated transactions with 3 injected fraud patterns
- **Features**: amount, location, hour, user_avg_amount (safe), is_amount_high_for_user (safe)
- **Threshold**: 0.7
- **Performance**:
  - Precision (fraud): 0.54
  - Recall (fraud): 0.28
  - F1 Score (fraud): 0.37

This version serves as a benchmark before implementing more advanced features or ensemble models.
