# GuardSQL Test Queries

This document contains test queries to validate GuardSQL functionality.

## Database Schema

### Tables
- **customers**: customer_id, first_name, last_name, email, city, state, country, created_at
- **products**: product_id, product_name, category, price, stock_quantity, created_at
- **orders**: order_id, customer_id, order_date, total_amount, status
- **order_items**: order_item_id, order_id, product_id, quantity, unit_price

---

## ✅ Valid Test Queries (Should Work)

### Basic Queries

1. **List all customers**
   ```
   Show me all customers
   ```

2. **List all products**
   ```
   Show me all products
   ```

3. **Count customers**
   ```
   How many customers do we have?
   ```

4. **Count orders**
   ```
   How many orders are there?
   ```

### Filter Queries

5. **Customers by state**
   ```
   Show me all customers from Texas
   ```

6. **Customers from California**
   ```
   List customers from CA
   ```

7. **Products under $100**
   ```
   Show me products under $100
   ```

8. **Products over $500**
   ```
   List products priced above $500
   ```

9. **Electronics products**
   ```
   Show me all electronics products
   ```

10. **Furniture category**
    ```
    List all furniture items
    ```

### Sorting Queries

11. **Most expensive products**
    ```
    Show top 5 most expensive products
    ```

12. **Cheapest products**
    ```
    Show me the 5 cheapest products
    ```

13. **Recent orders**
    ```
    Show me the last 10 orders
    ```

14. **Customers alphabetically**
    ```
    List customers sorted by last name
    ```

### Status Queries

15. **Completed orders**
    ```
    How many orders are completed?
    ```

16. **Pending orders**
    ```
    Show me all pending orders
    ```

17. **Shipped orders**
    ```
    List all shipped orders
    ```

### Aggregation Queries

18. **Total revenue**
    ```
    What is the total revenue from all orders?
    ```

19. **Average order value**
    ```
    What is the average order amount?
    ```

20. **Products by category count**
    ```
    How many products are in each category?
    ```

21. **Orders by status**
    ```
    Count orders grouped by status
    ```

### Join Queries

22. **Customer orders**
    ```
    Show me customers with their order totals
    ```

23. **Order details**
    ```
    Show order details with customer names
    ```

24. **Product sales**
    ```
    Which products have been ordered?
    ```

25. **Customer from specific city with orders**
    ```
    Show customers from New York with their orders
    ```

### Range Queries

26. **Price range**
    ```
    Show products between $50 and $200
    ```

27. **Date range**
    ```
    Show orders from January 2024
    ```

28. **Stock level**
    ```
    Show products with stock less than 50
    ```

### Complex Queries

29. **Top customers by spending**
    ```
    Show top 5 customers by total spending
    ```

30. **Products never ordered**
    ```
    Which products have never been ordered?
    ```

31. **Average product price by category**
    ```
    What is the average price per category?
    ```

32. **Customer order count**
    ```
    Show customers with more than 1 order
    ```

---

## ❌ Invalid Test Queries (Should Fail)

### Security Tests

33. **INSERT attempt**
    ```
    INSERT INTO customers VALUES (...)
    ```
    Expected: "Forbidden keyword: INSERT"

34. **UPDATE attempt**
    ```
    UPDATE products SET price = 0
    ```
    Expected: "Forbidden keyword: UPDATE"

35. **DELETE attempt**
    ```
    DELETE FROM orders
    ```
    Expected: "Forbidden keyword: DELETE"

36. **DROP attempt**
    ```
    DROP TABLE customers
    ```
    Expected: "Forbidden keyword: DROP"

37. **Multiple statements**
    ```
    SELECT * FROM customers; DROP TABLE customers;
    ```
    Expected: "Multiple statements not allowed"

38. **System table access**
    ```
    Show me pg_tables
    ```
    Expected: "Access to system tables not allowed"

---

## 🧪 Edge Cases

39. **Empty result**
    ```
    Show customers from Antarctica
    ```
    Expected: Valid query, 0 results

40. **Case sensitivity**
    ```
    Show customers from TEXAS
    ```
    Expected: Should work (case-insensitive)

41. **Special characters in search**
    ```
    Show products with name containing "27""
    ```
    Expected: Should handle quotes properly

42. **Very specific filter**
    ```
    Show products priced exactly at $29.99
    ```
    Expected: Should return Wireless Mouse

---

## 📊 Expected Results (Sample)

### Query: "Show me all customers from Texas"
Expected SQL:
```sql
SELECT * FROM customers WHERE state = 'TX' LIMIT 100
```
Expected Results: 2 rows (Alice Williams, David Miller)

### Query: "Show top 5 most expensive products"
Expected SQL:
```sql
SELECT * FROM products ORDER BY price DESC LIMIT 5
```
Expected Results: Laptop Pro 15, Standing Desk, Monitor 27", etc.

### Query: "How many orders are completed?"
Expected SQL:
```sql
SELECT COUNT(*) FROM orders WHERE status = 'completed' LIMIT 100
```
Expected Results: Count of completed orders

---

## 🚀 Testing Workflow

1. Start with basic queries (#1-4)
2. Test filtering (#5-10)
3. Test sorting (#11-14)
4. Test aggregations (#18-21)
5. Test joins (#22-25)
6. Test security (#33-38)
7. Test edge cases (#39-42)

---

## 📝 Notes

- All queries automatically get `LIMIT 100` appended
- Only SELECT queries are allowed
- System tables (pg_*, information_schema) are blocked
- Multiple statements separated by `;` are blocked
- Forbidden keywords: INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE, GRANT, REVOKE, EXEC, EXECUTE, CALL

---

## ✅ Success Criteria

- ✅ Valid queries return results
- ✅ Invalid queries show appropriate error messages
- ✅ No security bypasses possible
- ✅ LLM generates correct SQL from natural language
- ✅ Results display properly in UI
- ✅ Query logs are recorded

---

## 🐛 Troubleshooting

If queries fail:
1. Check backend logs: `tail -f app.log`
2. Verify Ollama is running: `ollama list`
3. Check database connection: `psql -U readonly_user -d guardsql_db -h localhost`
4. Review query_logs table: `SELECT * FROM query_logs ORDER BY created_at DESC LIMIT 5;`
