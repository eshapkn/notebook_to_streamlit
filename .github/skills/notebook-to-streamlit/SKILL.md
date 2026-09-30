# notebook-to-streamlit

Use this skill when developing or reviewing the local Streamlit app that converts the Rosa delivery-promise notebook into an interactive application.

## Scope

All changes belong in the local `notebook_to_streamlit` repository. The Git dependency `git+https://github.com/zhouy185/rosa-starter.git` is read-only. Never modify, fork, or push changes to that repository.

## Notebook API

Import the public API from the installed package using:

```python
from starter import COSTS, TIME_BLOCKS, ZONES, delivery_times
```

`delivery_times(zone, time_block, promised_delivery_time)` returns simulated delivery times for one zone and time block. `ZONES` and `TIME_BLOCKS` provide the supported values. The UI may add the special value `"all"`, which means expand across every supported value and aggregate the results.

## Business logic

For each candidate promise:

1. Count delayed orders where the simulated delivery time is greater than the promised time.
2. Count on-time orders as total orders minus delayed orders.
3. Calculate the opportunity as `total_orders * margin`.
4. Calculate late costs as `(delayed_orders * refund) + (delayed_orders * churn_orders * margin)`.
5. Calculate net profit as opportunity minus late costs.

`best_promise` must evaluate every candidate and every expanded zone/time-block pair, then select the row with the highest net profit. Use `extend()` when adding the list returned by `impact_of_delay`; using `append(*results)` breaks when an `"all"` selection returns multiple rows.

## Streamlit behavior

- Provide dropdowns for zone and time block.
- Provide controls for minimum promise, maximum promise, and step.
- Provide controls for margin, estimated churn per late order, and refund cost per late order.
- Do not calculate until the user clicks the recommendation button.
- Display the recommended promise and a readable table of all candidates explored.
- Validate that the minimum is not greater than the maximum and that at least one candidate exists.
- Keep the app entry point in `app.py` and preserve importable calculation functions for testing.
- Explain that each result is a simulation when the delivery model is randomized.

## Validation

Check syntax and editor diagnostics, then exercise a specific zone/time block and the `"all"`/`"all"` case. Also test custom costs and an invalid promise range. Do not use or require edits to the external `rosa-starter` repository.