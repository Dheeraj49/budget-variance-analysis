# Budget vs Actual Variance Analysis

**Tools:** Excel (Power Query, Tables, XLOOKUP, SUMIFS, IF, data validation, pivot tables, conditional formatting, charts), Power BI, DAX, Python (data generation)

> **Note:** The data in this project is **simulated** for a fictional company, "Brightline Retail Ltd". Real company budgets are confidential, so the dataset was generated with a short Python script (`5_SCRIPTS/generate_budget_data.py`) that includes realistic business patterns to investigate.

## Business problem

Brightline Retail Ltd planned a **€156,000 profit** for 2025. At year end, finance needs to know:

- Did the company hit its budget?
- Which departments and cost categories caused the difference?
- When did the problems happen, and are they one-offs or ongoing?
- What should change in next year's budget?

## Dataset

`1_DATA/budget_vs_actual_2025.csv`: 216 rows, one per department, category and month (January to December 2025).

| Column | Description |
|---|---|
| Month | 2025-01 to 2025-12 |
| Department | Sales, Marketing, Operations, IT, HR, Finance |
| Category | 18 lines, for example Product Revenue, Advertising, Salaries |
| Type | Revenue or Expense |
| Budget | Planned amount (€) |
| Actual | Actual amount (€) |

`1_DATA/department_owners.csv`: a small lookup file with each department's budget owner, cost centre and email (fictional names). Like many real exports, it arrived slightly messy: extra spaces around some department names and a blank row.

## Approach

### 0. Import the owners file with Power Query (`Owners` sheet, table `tblOwners`)

| Applied step | Why |
|---|---|
| Use First Row as Headers | The file's first row holds the column names |
| Remove Blank Rows | The export ended with an empty row |
| Trim (Department) | "  Marketing", "IT " and "Finance " had extra spaces, so lookups failed |
| Changed Type (Text) | Makes sure every column is read as text |

If the owners file changes, **Data > Refresh All** re-runs every step automatically.

### 1. Data sheet (Excel Table `tblData`)

Added four calculated columns:

| Column | Formula | Purpose |
|---|---|---|
| Variance | `=[@Actual]-[@Budget]` | Difference in € |
| Variance % | `=IF([@Budget]=0,0,[@Variance]/[@Budget])` | Difference as % of budget |
| Status | `=IF([@Type]="Revenue",IF([@Variance]>=0,"Favourable","Adverse"),IF([@Variance]<=0,"Favourable","Adverse"))` | Good or bad for profit |
| Quarter | `="Q"&ROUNDUP(VALUE(RIGHT([@Month],2))/3,0)` | Q1 to Q4 |
| Budget Owner | `=XLOOKUP([@Department],tblOwners[Department],tblOwners[Budget Owner],"Not found")` | Who is accountable for each line |

**Key rule:** the same variance can be good or bad. Revenue above budget is **Favourable**, but spending above budget is **Adverse**.

### 2. Summary sheet

- A company profit and loss summary built with `SUMIFS` (revenue, expenses and profit: budget vs actual).
- An expense variance table by department, with conditional formatting and data bars.
- Monthly revenue: budget vs actual.
- Three charts.
- **Department lookup:** pick a department from a dropdown (data validation). `XLOOKUP` returns its budget owner, cost centre, expense variance and status. For example, Marketing returns Liam O'Connor, CC-200, +€39,060, Adverse.

### 3. Pivot sheet

- **Pivot 1:** Type > Department > Category, with budget, actual and variance. Revenue and expenses are kept in separate blocks so they're never added together.
- **Pivot 2:** variance by category and quarter, to show *when* each variance happened.

### 4. Power BI (`3_DASHBOARD/budget_variance.pbix`)

DAX measures (`SUM`, `DIVIDE`, `CALCULATE`), KPI cards, a monthly revenue chart, a department variance chart, a matrix and a quarter slicer.

## Key findings

### Headline: a planned €156K profit became a €13K loss

| Line | Budget | Actual | Variance | Variance % |
|---|---|---|---|---|
| Revenue | €5,808,000 | €5,700,474 | -€107,526 | -1.9% |
| Expenses | €5,652,000 | €5,713,733 | +€61,733 | +1.1% |
| **Profit** | **€156,000** | **-€13,259** | **-€169,259** | |

Revenue came in €108K short **and** costs ran €62K over budget.

### Expense variance by department

| Department | Variance | Variance % | Status |
|---|---|---|---|
| Marketing | +€39,060 | +3.8% | Adverse |
| Operations | +€29,914 | +1.5% | Adverse |
| IT | +€22,878 | +3.1% | Adverse |
| HR | +€6,173 | +1.7% | Adverse |
| Finance | -€119 | 0.0% | Favourable |
| Sales | -€36,173 | -3.1% | Favourable |

### What caused it (variance by category and quarter)

| Category | Q1 | Q2 | Q3 | Q4 | Full year |
|---|---|---|---|---|---|
| Product Revenue | -€7,140 | **-€151,158** | +€36,783 | +€11,958 | -€109,557 |
| Advertising | -€2,023 | -€1,915 | +€1,087 | **+€47,033** | +€44,183 |
| Software Licences | +€1,613 | -€95 | **+€13,067** | **+€12,471** | +€27,056 |
| Logistics | -€358 | +€3,595 | -€1,559 | **+€24,525** | +€26,204 |
| Travel | -€10,663 | -€8,435 | -€8,870 | -€8,056 | -€36,023 |
| Recruitment | +€3,442 | -€185 | +€3,089 | -€16 | +€6,330 |

1. **A weak Q2 explains most of the profit miss.** Product revenue was €151K below budget from April to June, around 9 to 12% short every month. Revenue recovered from July but never made up the gap.
2. **The Q4 advertising campaign overspent by €47K** (about 35% over budget in October to December).
3. **Software licence costs rose permanently from July**, about 25% over budget every month. This is an ongoing cost, not a one-off.
4. **Christmas delivery costs** pushed Logistics €25K over budget in Q4.
5. **Travel was under budget every quarter** (about 25% below, €36K for the year). That suggests the travel budget is set too high.
6. **Two hiring drives** (March and September) pushed Recruitment 9% over budget.

## Recommendations

1. **Investigate the Q2 sales drop** (pricing, competition, stock issues) and set up a monthly revenue alert when actuals fall more than 5% below budget.
2. **Require sign-off for campaign spend above budget**, and measure the Q4 campaign's return before repeating it.
3. **Add the new software licences to the 2026 budget**, since the cost is permanent.
4. **Plan for seasonal logistics costs** in Q4 rather than budgeting the same amount every month.
5. **Cut the travel budget by about 25%** and reallocate around €36K to areas that are under pressure.
6. **Budget for planned hiring drives** in the months they happen.

## Limitations

- The data is simulated, so the findings show the method, not a real company's results.
- Monthly budgets for expense lines are flat. Real budgets usually include seasonality.
- The dataset has no headcount or volume figures, so variances can't be split into price and volume effects.

## Repository structure

```
1_DATA/      budget_vs_actual_2025.csv (simulated), department_owners.csv (lookup)
2_EXCEL/     budget_variance_analysis.xlsx (Data, Owners, Summary and Pivot sheets)
3_DASHBOARD/ budget_variance.pbix
4_IMAGE/     Screenshots
5_SCRIPTS/   generate_budget_data.py
```

## How to reproduce

1. Optional: run `python 5_SCRIPTS/generate_budget_data.py` to recreate the dataset. It uses a fixed seed, so the numbers are identical.
2. Open `2_EXCEL/budget_variance_analysis.xlsx` to see all formulas, pivots and charts. To refresh the Power Query, point it at your copy of `department_owners.csv` (**Data > Get Data > Data Source Settings > Change Source**), then click **Refresh All**.
3. Open `3_DASHBOARD/budget_variance.pbix` in Power BI Desktop.

## Author

Dheeraj | [GitHub](https://github.com/Dheeraj49)
