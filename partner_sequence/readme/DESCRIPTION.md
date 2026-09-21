This module assigns unique sequence IDs to Partners (Customers and
Vendors) and Employees. It automatically generates identifiers based on
customizable sequences (res.partner.customer, res.partner.vendor,
hr.employee.custom) when a partner or employee is created or modified.

**Use Cases / Benefits:**
* Standardize identifiers for integrations with third-party systems (ERPs, Payroll).
* Provide a clear, human-readable reference number for auditing or accounting.
* Eliminate dependency on `id` which can differ across databases.

It also enforces uniqueness of Tax Identification Numbers (TIN) across
all partners to prevent duplicate records.
