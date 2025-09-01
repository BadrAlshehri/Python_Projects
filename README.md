# S&P500 predictor


Badr Alshehri Project S&P500 predictor:


**Overview:**
A Python project that uses the **Yfinance API** to analyze and predict monthly movements in the **S\&P 500** (via the SPY ETF).

**How It Works:**

* The program pulls daily stock data (open and close prices) starting from **2015** (or any user-specified date).
* For each day:

  * If the **closing price is higher** than the **opening**, it's marked as **+1**.
  * If lower, it's marked as **-1**.
* These daily values are stored in a new **column** in the dataset.
* Each **month** is assigned a **Monthly Split**, which is simply the sum of the +1/-1 values for that month.
* The script looks for **past months with the same Monthly Split** (called “matching months”).
* It then checks what happened in the month **after each match**, calculating the **probability** of the market going **up or down**.
* When you run the script:

  * You input a **target month and year**.
  * It predicts the likely direction (up or down) for that month.
  * A **plot** shows the Monthly Splits for the entire target year for visualization.

**Goal:**
To predict the likelihood of a monthly market increase or decrease by comparing it with historically similar months.

