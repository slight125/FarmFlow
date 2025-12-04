# 🧪 FarmFlow CRUD Testing Checklist

Use this checklist to manually verify CRUD operations through the web interface.

---

## ⚙️ Setup

- [ ] Server is running: `python manage.py runserver`
- [ ] Browser open at: http://127.0.0.1:8000/
- [ ] Logged in as: `farmer_john` (or any test user)

---

## 🌾 CROPS MODULE

### CREATE (Add New Crop)
- [ ] Navigate to http://127.0.0.1:8000/crops/
- [ ] Click "Add New Crop" button
- [ ] Fill in form:
  - [ ] Name: "Test Tomatoes"
  - [ ] Variety: "Roma"
  - [ ] Area: 1.5 acres
  - [ ] Planting date: Today's date
  - [ ] Expected harvest date: 90 days from today
  - [ ] Status: "Planted"
- [ ] Click "Save"
- [ ] ✅ Success message appears
- [ ] ✅ New crop appears in list

### READ (View Crops)
- [ ] View crops list at http://127.0.0.1:8000/crops/
- [ ] ✅ All crops are displayed
- [ ] Click on a crop to view details
- [ ] ✅ Full crop information shown
- [ ] ✅ Related activities and tasks visible

### UPDATE (Edit Crop)
- [ ] From crop detail page, click "Edit"
- [ ] Change status to "Growing"
- [ ] Add notes: "Watered regularly, good growth"
- [ ] Click "Update"
- [ ] ✅ Success message appears
- [ ] ✅ Changes are visible in detail view

### DELETE (Remove Crop)
- [ ] From crop detail page, click "Delete"
- [ ] ✅ Confirmation page appears
- [ ] Click "Confirm Delete"
- [ ] ✅ Success message appears
- [ ] ✅ Crop no longer in list

---

## 🐄 LIVESTOCK MODULE

### CREATE (Add New Livestock)
- [ ] Navigate to http://127.0.0.1:8000/livestock/
- [ ] Click "Add New Livestock" button
- [ ] Fill in form:
  - [ ] Type: "Cattle"
  - [ ] Breed: "Holstein"
  - [ ] Tag Number: "TEST-001"
  - [ ] Date Acquired: Today's date
  - [ ] Gender: "Female"
  - [ ] Status: "Healthy"
  - [ ] Weight: 400 kg
- [ ] Click "Save"
- [ ] ✅ Success message appears
- [ ] ✅ New animal appears in list

### READ (View Livestock)
- [ ] View livestock list at http://127.0.0.1:8000/livestock/
- [ ] ✅ All animals displayed
- [ ] Click on an animal
- [ ] ✅ Full details shown
- [ ] ✅ Related activities visible

### UPDATE (Edit Livestock)
- [ ] From livestock detail page, click "Edit"
- [ ] Update weight to 420 kg
- [ ] Change status to "Pregnant"
- [ ] Click "Update"
- [ ] ✅ Success message appears
- [ ] ✅ Changes visible

### DELETE (Remove Livestock)
- [ ] From livestock detail page, click "Delete"
- [ ] ✅ Confirmation page appears
- [ ] Confirm deletion
- [ ] ✅ Success message appears
- [ ] ✅ Animal no longer in list

---

## 📦 INVENTORY MODULE

### CREATE (Add Inventory Item)
- [ ] Navigate to http://127.0.0.1:8000/inventory/
- [ ] Click "Add Inventory Item" button
- [ ] Fill in form:
  - [ ] Name: "Test Fertilizer"
  - [ ] Category: "Fertilizer"
  - [ ] Quantity: 100
  - [ ] Unit: "Bags"
  - [ ] Reorder Level: 20
  - [ ] Cost per Unit: 2500
- [ ] Click "Save"
- [ ] ✅ Success message appears
- [ ] ✅ Item appears in inventory list
- [ ] ✅ Total value calculated correctly (100 × 2500)

### READ (View Inventory)
- [ ] View inventory list at http://127.0.0.1:8000/inventory/
- [ ] ✅ All items displayed
- [ ] Click on an item
- [ ] ✅ Full details shown
- [ ] ✅ Total value visible

### UPDATE (Edit Inventory)
- [ ] From inventory detail page, click "Edit"
- [ ] Change quantity to 90
- [ ] Add supplier: "AgriSupplies Ltd"
- [ ] Click "Update"
- [ ] ✅ Success message appears
- [ ] ✅ Total value recalculated (90 × 2500)

### DELETE (Remove Inventory Item)
- [ ] From inventory detail page, click "Delete"
- [ ] ✅ Confirmation page appears
- [ ] Confirm deletion
- [ ] ✅ Success message appears
- [ ] ✅ Item no longer in list

---

## 💰 FINANCE MODULE

### CREATE (Add Transaction)
- [ ] Navigate to http://127.0.0.1:8000/finance/
- [ ] Click "Add Transaction" button
- [ ] Fill in form:
  - [ ] Type: "Income"
  - [ ] Category: "Crop Sale"
  - [ ] Amount: 25000
  - [ ] Date: Today's date
  - [ ] Description: "Sale of tomatoes"
  - [ ] Payment Method: "M-Pesa"
- [ ] Click "Save"
- [ ] ✅ Success message appears
- [ ] ✅ Transaction appears in list
- [ ] ✅ Totals updated

### READ (View Transactions)
- [ ] View finance list at http://127.0.0.1:8000/finance/
- [ ] ✅ All transactions displayed
- [ ] ✅ Total income shown
- [ ] ✅ Total expenses shown
- [ ] ✅ Net amount calculated

### UPDATE (Edit Transaction)
- [ ] Click "Edit" on a transaction
- [ ] Change amount to 27000
- [ ] Add reference number: "REF-12345"
- [ ] Click "Update"
- [ ] ✅ Success message appears
- [ ] ✅ Changes visible
- [ ] ✅ Totals recalculated

### DELETE (Remove Transaction)
- [ ] Click "Delete" on a transaction
- [ ] ✅ Confirmation page appears
- [ ] Confirm deletion
- [ ] ✅ Success message appears
- [ ] ✅ Transaction removed
- [ ] ✅ Totals updated

---

## ✅ TASKS MODULE

### CREATE (Add Task)
- [ ] Navigate to http://127.0.0.1:8000/tasks/
- [ ] Click "Add New Task" button
- [ ] Fill in form:
  - [ ] Title: "Water greenhouse crops"
  - [ ] Description: "Water all crops in greenhouse section"
  - [ ] Priority: "High"
  - [ ] Status: "Pending"
  - [ ] Due Date: Tomorrow's date
- [ ] Click "Save"
- [ ] ✅ Success message appears
- [ ] ✅ Task appears in list

### READ (View Tasks)
- [ ] View tasks list at http://127.0.0.1:8000/tasks/
- [ ] ✅ All tasks displayed
- [ ] ✅ Overdue tasks highlighted (if any)
- [ ] ✅ Priority indicators visible

### UPDATE (Edit Task)
- [ ] Click "Edit" on a task
- [ ] Change status to "In Progress"
- [ ] Add notes: "Started at 9 AM"
- [ ] Click "Update"
- [ ] ✅ Success message appears
- [ ] ✅ Status updated

### DELETE (Remove Task)
- [ ] Click "Delete" on a task
- [ ] ✅ Confirmation page appears
- [ ] Confirm deletion
- [ ] ✅ Success message appears
- [ ] ✅ Task removed from list

---

## 📝 ACTIVITIES MODULE

### CREATE (Log Activity)
- [ ] Navigate to http://127.0.0.1:8000/activities/
- [ ] Click "Log New Activity" button
- [ ] Fill in form:
  - [ ] Activity Type: "Irrigation"
  - [ ] Title: "Watered field B"
  - [ ] Description: "Full irrigation of field B section"
  - [ ] Date: Today
  - [ ] Duration: 120 minutes
  - [ ] Labor Cost: 500
- [ ] Click "Save"
- [ ] ✅ Success message appears
- [ ] ✅ Activity logged in list

### READ (View Activities)
- [ ] View activities list at http://127.0.0.1:8000/activities/
- [ ] ✅ All activities displayed chronologically
- [ ] ✅ Activity types visible
- [ ] ✅ Costs shown

### UPDATE (Edit Activity)
- [ ] Click "Edit" on an activity
- [ ] Change duration to 150 minutes
- [ ] Add materials: "Used 500L of water"
- [ ] Click "Update"
- [ ] ✅ Success message appears
- [ ] ✅ Changes visible

### DELETE (Remove Activity)
- [ ] Click "Delete" on an activity
- [ ] ✅ Confirmation page appears
- [ ] Confirm deletion
- [ ] ✅ Success message appears
- [ ] ✅ Activity removed

---

## 🎯 FILTERING AND SEARCH

### Crops Filtering
- [ ] Go to crops list
- [ ] Use status filter
- [ ] ✅ Only filtered crops shown

### Livestock Filtering
- [ ] Go to livestock list
- [ ] Use type filter
- [ ] ✅ Only filtered animals shown

### Inventory Filtering
- [ ] Go to inventory list
- [ ] Use category filter
- [ ] ✅ Only filtered items shown
- [ ] Try "Low Stock" filter
- [ ] ✅ Only low stock items shown

### Finance Filtering
- [ ] Go to finance list
- [ ] Filter by Income
- [ ] ✅ Only income transactions shown
- [ ] Filter by Expense
- [ ] ✅ Only expense transactions shown

### Tasks Filtering
- [ ] Go to tasks list
- [ ] Filter by status
- [ ] ✅ Filtered tasks shown
- [ ] Filter by priority
- [ ] ✅ Priority filtered correctly

### Activities Filtering
- [ ] Go to activities list
- [ ] Filter by activity type
- [ ] ✅ Filtered activities shown

---

## 👤 PROFILE MODULE

### VIEW PROFILE
- [ ] Navigate to http://127.0.0.1:8000/profile/
- [ ] ✅ User information displayed
- [ ] ✅ Farm details visible

### UPDATE PROFILE
- [ ] Click edit or modify profile
- [ ] Change phone number
- [ ] Change farm name
- [ ] Update location
- [ ] Upload avatar (optional)
- [ ] Click "Save"
- [ ] ✅ Success message appears
- [ ] ✅ Changes visible

---

## 🔐 SECURITY TESTS

### Authentication
- [ ] Try accessing /crops/ without login
- [ ] ✅ Redirected to login page
- [ ] Log in successfully
- [ ] ✅ Can access crops page

### Data Isolation
- [ ] Login as farmer_john
- [ ] Note number of crops
- [ ] Logout
- [ ] Login as different user
- [ ] ✅ Different crops shown (user-specific data)

### Admin Access
- [ ] Try accessing /admin-dashboard/ as regular user
- [ ] ✅ Access denied or redirected
- [ ] Login as superuser
- [ ] ✅ Can access admin dashboard

---

## 📊 DASHBOARD TESTS

### View Dashboard
- [ ] Navigate to http://127.0.0.1:8000/dashboard/
- [ ] ✅ Role-based dashboard displayed
- [ ] ✅ Statistics shown
- [ ] ✅ Recent activities visible
- [ ] ✅ Upcoming tasks displayed
- [ ] ✅ Charts/graphs rendering

---

## 🎉 FINAL CHECK

### Overall Functionality
- [ ] ✅ All CREATE operations work
- [ ] ✅ All READ operations work
- [ ] ✅ All UPDATE operations work
- [ ] ✅ All DELETE operations work
- [ ] ✅ All filters work
- [ ] ✅ All forms validate properly
- [ ] ✅ All success messages display
- [ ] ✅ All error messages display
- [ ] ✅ All redirects work correctly
- [ ] ✅ Navigation is smooth

### Data Integrity
- [ ] ✅ No orphaned records
- [ ] ✅ Related data updates correctly
- [ ] ✅ Deletion cascades properly
- [ ] ✅ Calculations are accurate

### User Experience
- [ ] ✅ Forms are intuitive
- [ ] ✅ Buttons are clear
- [ ] ✅ Messages are helpful
- [ ] ✅ Navigation is logical
- [ ] ✅ Page loads are fast

---

## 📝 Notes Section

**Issues Found:**
_List any issues you encounter during testing_

---

**Testing Completed By**: ___________________  
**Date**: ___________________  
**Overall Result**: ⬜ PASS  ⬜ FAIL

---

**Legend:**
- [ ] Not tested
- [x] Tested and working
- ❌ Failed test
- ⚠️ Warning/Issue

---

**Run Automated Tests:**
```bash
python test_crud.py
```

**Check System:**
```bash
python manage.py check
```

---

## ✅ Completion Status

When all checkboxes are marked:
🎉 **CRUD OPERATIONS FULLY VERIFIED!**
