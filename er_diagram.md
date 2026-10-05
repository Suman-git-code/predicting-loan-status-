# ER Diagram — Bank Loan Prediction Mini Project

```mermaid
erDiagram
    CUSTOMERS ||--o{ ACCOUNTS : "has"
    CUSTOMERS ||--o{ LOANS : "takes"
    ACCOUNTS ||--o{ TRANSACTIONS : "records"

    CUSTOMERS {
        NUMBER CUSTOMERID PK
        VARCHAR2 FIRSTNAME
        VARCHAR2 LASTNAME
        DATE DATEOFBIRTH
        VARCHAR2 GENDER
        VARCHAR2 EMAIL
        VARCHAR2 PHONE
        VARCHAR2 ADDRESS
        VARCHAR2 CITY
        VARCHAR2 STATE
        VARCHAR2 POSTALCODE
        VARCHAR2 ACCOUNTNUMBER
        VARCHAR2 ACCOUNTTYPE
        NUMBER BALANCE
        NUMBER BRANCHID
        DATE CREATEDDATE
        VARCHAR2 STATUS
    }

    ACCOUNTS {
        NUMBER ACCOUNTID PK
        NUMBER CUSID FK
        VARCHAR2 ACCOUNTNUMBER
        VARCHAR2 ACCOUNTTYPE
        NUMBER BRANCHID
        NUMBER BALANCE
        VARCHAR2 STATUS
    }

    TRANSACTIONS {
        NUMBER TRANSACTIONID PK
        NUMBER ACCOUNTID FK
        NUMBER AMOUNT
        VARCHAR2 TRANSACTIONTYPE
        DATE TXTDATE
    }

    LOANS {
        NUMBER LOAN_ID PK
        NUMBER CUSTOMER_ID FK
        NUMBER PRINCIPAL
        NUMBER INTEREST_RATE
        NUMBER TERM_MONTHS
        NUMBER EMI_AMOUNT
        VARCHAR2 LOAN_STATUS
    }
```

## Relationship summary
- **CUSTOMERS → ACCOUNTS**: one-to-many (one customer can hold multiple accounts; in this project, 1 account per customer)
- **CUSTOMERS → LOANS**: one-to-many (one customer can take multiple loans; in this project, 1 loan per customer)
- **ACCOUNTS → TRANSACTIONS**: one-to-many (each account has many transaction records over time)

## Notes on schema design
- `ACCOUNTS.CUSID` is the foreign key referencing `CUSTOMERS.CUSTOMERID`
- `LOANS.CUSTOMER_ID` is the foreign key referencing `CUSTOMERS.CUSTOMERID`
- `TRANSACTIONS.ACCOUNTID` is the foreign key referencing `ACCOUNTS.ACCOUNTID`
- `CUSTOMERS` and `ACCOUNTS` both carry `ACCOUNTNUMBER`, `ACCOUNTTYPE`, and `BALANCE` — a denormalization worth mentioning in your report as an area for schema improvement (in a fully normalized design, these would live only in `ACCOUNTS`)
