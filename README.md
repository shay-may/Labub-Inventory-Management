# Labubu Inventory Manager (Pastel GUI)

A clean, pastel-themed Python + Tkinter inventory app for tracking
collectible items (Labubu or anything similar). It supports full
customization per item (series, generation, color, special edition,
price, quantity), plus filtering, sorting, and low-stock checks.

This project is intentionally built as a strong "intro-to-systems" style
application: it uses structured data, input validation, and event-driven
GUI logic. It is also easy to expand into budgeting, profit tracking,
forecasting, and analytics.

------------------------------------------------------------------------

## Features

-   Pastel GUI (pink, yellow, sky blue)
-   Add new items with full custom fields
-   Update existing items
-   Remove items
-   View everything in a table
-   Filter by any keyword
-   Special-only toggle
-   Sort by name, series, generation, color, price, quantity, or special
-   Low stock checker using a threshold
-   Live status summary

------------------------------------------------------------------------

## Finance Applications

This inventory system models real business inventory tracking.

### Inventory Valuation

Total Inventory Value = Σ(price × quantity)

### Budgeting

Low stock thresholds help model reorder planning.

### Profit Tracking

Can be expanded to include cost and resale price.

### Forecasting

With timestamps, demand forecasting is possible.

------------------------------------------------------------------------

## Coding Applications

-   Dictionary-based data modeling
-   Input validation
-   GUI event handling
-   Sorting and filtering logic

------------------------------------------------------------------------

## Math Applications

-   Aggregation and summation
-   Inequality checks
-   Ordered statistics
-   Ratio and profit formulas

------------------------------------------------------------------------

## How to Run

``` bash
python labubu_inventory_gui.py
```

------------------------------------------------------------------------

## Data Model

Each item is stored as:

``` python
inventory["Name"] = {
  "series": "...",
  "generation": "...",
  "color": "...",
  "price": 0.0,
  "quantity": 0,
  "special": False
}
```

------------------------------------------------------------------------

## Function Guide

### normalize_name

Cleans extra spaces from names.

### safe_float

Validates price input.

### safe_int

Validates quantity input.

### safe_generation

Ensures generation is not empty.

### safe_text

Validates required fields.

### upsert_item

Creates or updates records.

### refresh_table

Rebuilds table with sorting and filtering.

### update_status

Updates summary metrics.

### clear_form

Resets input fields.

### load_selected_into_form

Loads selected item into editor.

### add_item

Adds new inventory items.

### update_item

Edits existing items.

### remove_item

Deletes selected items.

### check_low_stock

Finds items below threshold.

### on_filter_change / on_sort_change

Refresh display automatically.

------------------------------------------------------------------------

## Expansion Ideas

### Finance

-   Profit margins
-   ROI tracking
-   Export to Excel

### Coding

-   File saving
-   Database backend
-   Unit tests

### Analytics

-   Sales trends
-   Forecast models
-   Charts

------------------------------------------------------------------------

## License

MIT
