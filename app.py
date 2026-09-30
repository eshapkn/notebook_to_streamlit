import pandas as pd
import streamlit as st
from starter import COSTS, TIME_BLOCKS, ZONES, delivery_times


def zone_time_combinations(zone, time_block):
  zones = ZONES if zone == "all" else [zone]
  time_blocks = TIME_BLOCKS if time_block == "all" else [time_block]
  return [(selected_zone, selected_time_block)
      for selected_zone in zones
      for selected_time_block in time_blocks]


def impact_of_delay(promised_delivery_time, zone, time_block, costs):
  results = []
  for selected_zone, selected_time_block in zone_time_combinations(zone, time_block):
    times = delivery_times(
      selected_zone,
      selected_time_block,
      promised_delivery_time,
    )
    total_orders = len(times)
    total_delayed_orders = sum(
      delivery_time > promised_delivery_time for delivery_time in times
    )
    total_on_time_orders = total_orders - total_delayed_orders
    profit_opportunity = total_orders * costs["margin"]
    total_cost_of_delay = (
      total_delayed_orders * costs["refund"]
      + total_delayed_orders * costs["churn_orders"] * costs["margin"]
    )
    net_profit = profit_opportunity - total_cost_of_delay
    results.append((
      promised_delivery_time,
      selected_zone,
      selected_time_block,
      total_orders,
      total_on_time_orders,
      total_delayed_orders,
      round(float(total_cost_of_delay), 2),
      round(float(net_profit), 2),
    ))
  return results


def best_promise(zone, time_block, promised_delivery_times, costs):
  results = []
  for promised_delivery_time in promised_delivery_times:
    results.extend(impact_of_delay(
      promised_delivery_time,
      zone,
      time_block,
      costs,
    ))
  if not results:
    raise ValueError("promised_delivery_times must contain at least one value")
  results.sort(key=lambda result: result[7], reverse=True)
  return results[0], results


def results_dataframe(results):
  return pd.DataFrame(results, columns=[
    "Promised time (min)",
    "Zone",
    "Time block",
    "Total orders",
    "On-time orders",
    "Delayed orders",
    "Cost of delay ($)",
    "Net profit ($)",
  ])


st.set_page_config(page_title="Rosa's Delivery Promise", page_icon="🍕")
st.title("Rosa's Delivery Promise")
st.write("Use simulated delivery performance to choose a profitable promise time.")

with st.sidebar:
  st.header("Scenario")
  selected_zone = st.selectbox("Zone", ["all", *ZONES])
  selected_time_block = st.selectbox("Time block", ["all", *TIME_BLOCKS])

  st.header("Promise range")
  minimum_promise = st.number_input("Minimum time (minutes)", min_value=1, value=5, step=1)
  maximum_promise = st.number_input("Maximum time (minutes)", min_value=1, value=75, step=1)
  promise_step = st.number_input("Step (minutes)", min_value=1, value=5, step=1)

  st.header("Costs")
  margin = st.number_input("Profit margin per order ($)", min_value=0.0, value=float(COSTS["margin"]), step=0.5)
  churn_orders = st.number_input("Estimated churn per late order", min_value=0.0, value=float(COSTS["churn_orders"]), step=0.01)
  refund = st.number_input("Refund per late order ($)", min_value=0.0, value=float(COSTS["refund"]), step=0.5)

costs = {"margin": margin, "churn_orders": churn_orders, "refund": refund}

if st.button("Find best promised time", type="primary"):
  if minimum_promise > maximum_promise:
    st.error("The minimum promise must be less than or equal to the maximum promise.")
  else:
    promise_times = list(range(int(minimum_promise), int(maximum_promise) + 1, int(promise_step)))
    best_result, all_results = best_promise(
      selected_zone,
      selected_time_block,
      promise_times,
      costs,
    )
    st.subheader("Recommendation")
    metric_columns = st.columns(4)
    metric_columns[0].metric("Promised time", f"{best_result[0]} min")
    metric_columns[1].metric("Net profit", f"${best_result[7]:,.2f}")
    metric_columns[2].metric("Delayed orders", best_result[5])
    metric_columns[3].metric("Cost of delay", f"${best_result[6]:,.2f}")
    st.caption("Each calculation uses a fresh simulation from the notebook's delivery-time model.")

    st.subheader("Promise options explored")
    st.dataframe(
      results_dataframe(all_results),
      use_container_width=True,
      hide_index=True,
    )
