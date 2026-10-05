-- ================================================================
-- SQL INSIGHT QUERIES — Bank Loan Prediction Mini Project
-- ================================================================

-- 1. Feature table used for ML model (customer + account + transaction + loan joined)
SELECT 
    l.LOAN_ID,
    l.CUSTOMER_ID,
    l.PRINCIPAL,
    l.INTEREST_RATE,
    l.TERM_MONTHS,
    l.EMI_AMOUNT,
    (l.EMI_AMOUNT / l.PRINCIPAL) AS emi_to_principal_ratio,
    c.GENDER,
    MONTHS_BETWEEN(SYSDATE, c.DATEOFBIRTH)/12 AS age,
    MONTHS_BETWEEN(SYSDATE, c.CREATEDDATE) AS tenure_months,
    a.BALANCE,
    (l.EMI_AMOUNT / a.BALANCE) AS emi_to_balance_ratio,
    NVL(t.txn_count, 0) AS txn_count,
    NVL(t.avg_txn_amount, 0) AS avg_txn_amount,
    l.LOAN_STATUS
FROM loans l
JOIN customers c ON l.CUSTOMER_ID = c.CUSTOMERID
JOIN accounts a ON a.CUSID = c.CUSTOMERID
LEFT JOIN (
    SELECT ACCOUNTID, COUNT(*) AS txn_count, AVG(ABS(AMOUNT)) AS avg_txn_amount
    FROM transactions
    GROUP BY ACCOUNTID
) t ON t.ACCOUNTID = a.CUSID;


-- 2. Loan status distribution overall
SELECT LOAN_STATUS, COUNT(*) AS num_loans,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct
FROM loans
GROUP BY LOAN_STATUS;


-- 3. Average balance and loan status split by branch
SELECT 
    a.BRANCHID,
    COUNT(DISTINCT c.CUSTOMERID) AS num_customers,
    ROUND(AVG(a.BALANCE), 2) AS avg_balance,
    SUM(CASE WHEN l.LOAN_STATUS = 'CLOSED' THEN 1 ELSE 0 END) AS closed_loans,
    SUM(CASE WHEN l.LOAN_STATUS = 'ACTIVE' THEN 1 ELSE 0 END) AS active_loans
FROM customers c
JOIN accounts a ON a.CUSID = c.CUSTOMERID
LEFT JOIN loans l ON l.CUSTOMER_ID = c.CUSTOMERID
GROUP BY a.BRANCHID
ORDER BY a.BRANCHID;


-- 4. Customers with high EMI burden (EMI > 15% of their account balance) — potential risk list
SELECT 
    c.CUSTOMERID,
    c.FIRSTNAME || ' ' || c.LASTNAME AS customer_name,
    a.BALANCE,
    l.EMI_AMOUNT,
    ROUND((l.EMI_AMOUNT / a.BALANCE) * 100, 1) AS emi_pct_of_balance,
    l.LOAN_STATUS
FROM customers c
JOIN accounts a ON a.CUSID = c.CUSTOMERID
JOIN loans l ON l.CUSTOMER_ID = c.CUSTOMERID
WHERE (l.EMI_AMOUNT / a.BALANCE) > 0.15
ORDER BY emi_pct_of_balance DESC;


-- 5. Top 10 most financially active customers (by transaction count)
SELECT 
    c.CUSTOMERID,
    c.FIRSTNAME || ' ' || c.LASTNAME AS customer_name,
    COUNT(t.TRANSACTIONID) AS txn_count,
    ROUND(AVG(ABS(t.AMOUNT)), 2) AS avg_txn_amount,
    ROUND(SUM(CASE WHEN t.AMOUNT > 0 THEN t.AMOUNT ELSE 0 END), 2) AS total_deposits,
    ROUND(SUM(CASE WHEN t.AMOUNT < 0 THEN ABS(t.AMOUNT) ELSE 0 END), 2) AS total_withdrawals
FROM customers c
JOIN transactions t ON t.ACCOUNTID = c.CUSTOMERID
GROUP BY c.CUSTOMERID, c.FIRSTNAME, c.LASTNAME
ORDER BY txn_count DESC
FETCH FIRST 10 ROWS ONLY;


-- 6. Loan status distribution by term length (does loan duration affect closure?)
SELECT 
    TERM_MONTHS,
    COUNT(*) AS num_loans,
    SUM(CASE WHEN LOAN_STATUS = 'CLOSED' THEN 1 ELSE 0 END) AS closed,
    SUM(CASE WHEN LOAN_STATUS = 'ACTIVE' THEN 1 ELSE 0 END) AS active,
    ROUND(SUM(CASE WHEN LOAN_STATUS = 'CLOSED' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS pct_closed
FROM loans
GROUP BY TERM_MONTHS
ORDER BY TERM_MONTHS;


-- 7. Average customer age and tenure by loan status
SELECT 
    l.LOAN_STATUS,
    ROUND(AVG(MONTHS_BETWEEN(SYSDATE, c.DATEOFBIRTH)/12), 1) AS avg_age,
    ROUND(AVG(MONTHS_BETWEEN(SYSDATE, c.CREATEDDATE)), 1) AS avg_tenure_months,
    ROUND(AVG(a.BALANCE), 2) AS avg_balance
FROM loans l
JOIN customers c ON l.CUSTOMER_ID = c.CUSTOMERID
JOIN accounts a ON a.CUSID = c.CUSTOMERID
GROUP BY l.LOAN_STATUS;


-- 8. Gender-wise loan status breakdown
SELECT 
    c.GENDER,
    l.LOAN_STATUS,
    COUNT(*) AS num_loans
FROM loans l
JOIN customers c ON l.CUSTOMER_ID = c.CUSTOMERID
GROUP BY c.GENDER, l.LOAN_STATUS
ORDER BY c.GENDER, l.LOAN_STATUS;


-- 9. State-wise average balance and total loan principal outstanding (ACTIVE only)
SELECT 
    c.STATE,
    COUNT(DISTINCT c.CUSTOMERID) AS num_customers,
    ROUND(AVG(a.BALANCE), 2) AS avg_balance,
    ROUND(SUM(CASE WHEN l.LOAN_STATUS = 'ACTIVE' THEN l.PRINCIPAL ELSE 0 END), 2) AS active_loan_exposure
FROM customers c
JOIN accounts a ON a.CUSID = c.CUSTOMERID
LEFT JOIN loans l ON l.CUSTOMER_ID = c.CUSTOMERID
GROUP BY c.STATE
ORDER BY active_loan_exposure DESC;


-- 10. Dormant / low-activity accounts (fewer than 3 transactions) — candidates for engagement
SELECT 
    c.CUSTOMERID,
    c.FIRSTNAME || ' ' || c.LASTNAME AS customer_name,
    NVL(t.txn_count, 0) AS txn_count,
    a.BALANCE
FROM customers c
JOIN accounts a ON a.CUSID = c.CUSTOMERID
LEFT JOIN (
    SELECT ACCOUNTID, COUNT(*) AS txn_count
    FROM transactions
    GROUP BY ACCOUNTID
) t ON t.ACCOUNTID = c.CUSTOMERID
WHERE NVL(t.txn_count, 0) < 3
ORDER BY txn_count ASC;
