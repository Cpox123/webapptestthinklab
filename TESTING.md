# ThinkLab Sentiment Analyzer - Testing Documentation

## 1. Purpose
This document records functional testing for the **ThinkLab Sentiment Analyzer** Streamlit application.

Testing covers:
- Single review prediction
- Bulk CSV prediction
- Input validation and error handling
- Dashboard behaviour
- Light and dark theme readability
- CSV result download
- Final regression testing

## 2. Application Under Test
**Application:** ThinkLab Sentiment Analyzer  
**Final Model:** BERT  
**Sentiment Classes:** Positive, Neutral, Negative

Pages:
1. Home
2. Single Prediction
3. Bulk Prediction
4. Dashboard
5. About

## 3. Single Prediction Tests

| ID | Scenario | Input | Expected Result | Status |
|---|---|---|---|---|
| SP-01 | Positive prediction | `The dress is beautiful and I love it.` | Positive + confidence | PASS |
| SP-02 | Negative prediction | `The product is terrible and I want to return it.` | Negative + confidence | PASS |
| SP-03 | Neutral prediction | `The quality is okay.` | Neutral + confidence | PASS |
| SP-04 | Empty input | Empty text | Reject or request valid text | TO VERIFY |
| SP-05 | Punctuation | `Amazing!!! I really love this dress.` | Valid prediction | TO VERIFY |
| SP-06 | Mixed case | `THIS Product Is Very Good` | Valid prediction | TO VERIFY |
| SP-07 | Long review | Long valid review | Prediction completes without crash | TO VERIFY |

## 4. Bulk CSV Prediction Tests

| ID | Scenario | Expected Result | Status |
|---|---|---|---|
| BP-01 | Valid CSV with `Review Text` | Preview and dataset info displayed | PASS |
| BP-02 | Predict 3 reviews | Prediction returned for each valid row | PASS |
| BP-03 | Output columns | `Review Text`, `Predicted Sentiment`, `Confidence` | PASS |
| BP-04 | Three sentiment examples | Positive, Negative and Neutral returned | PASS |
| BP-05 | Download results | Result CSV downloadable | PASS |
| BP-06 | Missing review column | Clear accepted-column error | TO VERIFY |
| BP-07 | Empty CSV | Clear error and processing stopped | TO VERIFY |
| BP-08 | Invalid CSV | Invalid CSV error displayed | TO VERIFY |
| BP-09 | Blank review rows | Blank reviews handled safely | TO VERIFY |
| BP-10 | Above bulk row limit | Warning and row limit enforced | TO VERIFY |
| BP-11 | Latin-1 CSV | Encoding fallback works | TO VERIFY |

## 5. Bulk Prediction Sample

```csv
Review Text
The dress is beautiful
The product is terrible
The quality is okay
```

Observed output:

| Review Text | Predicted Sentiment | Confidence |
|---|---|---:|
| The dress is beautiful | Positive | 1.00 |
| The product is terrible | Negative | 0.92 |
| The quality is okay | Neutral | 0.62 |

## 6. Validation and Error Handling

| ID | Scenario | Expected Behaviour | Status |
|---|---|---|---|
| VH-01 | No file uploaded | Prediction does not run | PASS |
| VH-02 | Empty CSV | Error shown | TO VERIFY |
| VH-03 | Malformed CSV | Parser error shown | TO VERIFY |
| VH-04 | Missing review column | Accepted names shown | TO VERIFY |
| VH-05 | Blank review rows | Safely handled | TO VERIFY |
| VH-06 | Row limit exceeded | Warning + limit enforced | TO VERIFY |
| VH-07 | New CSV after previous results | Old state invalidated | TO VERIFY |

## 7. Dashboard Tests

| ID | Scenario | Expected Result | Status |
|---|---|---|---|
| DB-01 | Open Dashboard | Loads without error | PASS |
| DB-02 | Model comparison | Six model results shown correctly | TO VERIFY |
| DB-03 | Bulk analytics | Charts reflect current predictions | TO VERIFY |
| DB-04 | Chart readability | Labels and values visible | TO VERIFY |

## 8. Theme and UI Tests

| ID | Scenario | Expected Result | Status |
|---|---|---|---|
| UI-01 | Light mode | Readable throughout app | PASS |
| UI-02 | Dark mode | Readable throughout app | PASS |
| UI-03 | Sidebar navigation | All pages open | PASS |
| UI-04 | Shared branding | Logo and branding consistent | PASS |
| UI-05 | Footer | Displays without blocking content | TO VERIFY |
| UI-06 | Bulk layout | Upload, results and charts usable | PASS |

## 9. Model Output Consistency

| ID | Scenario | Expected Result | Status |
|---|---|---|---|
| MC-01 | Same review repeated | Consistent output | TO VERIFY |
| MC-02 | Single vs bulk | Same review gets same sentiment | TO VERIFY |
| MC-03 | Confidence | Valid probability range | PASS |
| MC-04 | Label set | Only Positive, Neutral or Negative | PASS |

## 10. Final Regression Checklist

- [✅] Open final deployed application in a fresh browser session.
- [✅] Test a positive single review.
- [✅] Test a negative single review.
- [✅] Test a neutral single review.
- [✅] Upload final sample CSV.
- [✅] Run bulk prediction.
- [✅] Verify result columns.
- [✅] Verify confidence values.
- [✅] Verify sentiment distribution charts.
- [✅] Download result CSV.
- [✅] Open Dashboard.
- [✅] Open About.
- [✅] Check light mode.
- [✅] Check dark mode.
- [✅] Confirm no visible Streamlit/Python errors.
- [✅] Capture final testing screenshots for report/Git evidence.

## 11. Known Limitations

- Training data is specific to women's e-commerce clothing reviews.
- The dataset is strongly imbalanced toward Positive reviews.
- Neutral reviews are comparatively underrepresented.
- Sarcasm, ambiguity and mixed sentiment can be difficult to classify.
- Predictions should be treated as automated estimates rather than perfect interpretations.

## 12. Testing Contribution

**Primary Testing & Documentation:** Pawan Vihanga - CIT-24-01-0459

Main testing areas:
- Single review prediction
- Bulk CSV workflow
- Input validation
- Theme/readability
- Dashboard validation
- Testing documentation
- Final regression testing


