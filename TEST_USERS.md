# FarmFlow Test Users - Role-Based Dashboard Testing

## Test User Credentials

All passwords are simple for testing purposes only. Change them in production!

### 1. FARMER (farmer_john)
- **Email:** farmer@farmflow.com
- **Password:** farmer123
- **Role:** Farmer
- **Dashboard Features:**
  - View own crops and livestock
  - Manage personal finances
  - View and complete assigned tasks
  - Log farm activities
  - Basic inventory management

### 2. MANAGER (manager_mary)
- **Email:** manager@farmflow.com
- **Password:** manager123
- **Role:** Farm Manager
- **Dashboard Features:**
  - Farm-wide analytics and statistics
  - Team task assignment and monitoring
  - Resource and inventory management
  - Performance metrics
  - Financial trends and reports
  - Full analytics access

### 3. WORKER (worker_peter)
- **Email:** worker@farmflow.com
- **Password:** worker123
- **Role:** Worker
- **Dashboard Features:**
  - View assigned tasks only
  - Log activities for completed work
  - Track personal task completion rate
  - Limited access (no financial or inventory data)

### 4. CONSULTANT (consultant_sarah)
- **Email:** consultant@farmflow.com
- **Password:** consultant123
- **Role:** Agricultural Consultant
- **Dashboard Features:**
  - Comprehensive crop performance analysis
  - Livestock health monitoring
  - Financial analysis with profitability ratios
  - Agricultural recommendations
  - Advisory insights and best practices
  - Full analytics and reporting

### 5. ADMIN (admin)
- **Email:** admin@farmflow.com
- **Password:** admin123
- **Role:** Manager (with Superuser privileges)
- **Dashboard Features:**
  - All Manager features
  - Admin Panel access (Superuser only)
  - User role management
  - System-wide control
  - Can assign/change user roles

---

## Testing Instructions

1. **Start the development server:**
   ```
   python manage.py runserver
   ```

2. **Login at:** http://127.0.0.1:8000/login/

3. **Test each role:**
   - Log in with each user to see their specific dashboard
   - Verify role-based navigation (sidebar items)
   - Test creating/editing data based on permissions

4. **Admin Panel Access:**
   - Login as 'admin' user
   - Navigate to Admin Panel from sidebar
   - Test changing user roles

---

## Navigation Permissions by Role

| Menu Item  | Farmer | Manager | Worker | Consultant |
|------------|--------|---------|--------|------------|
| Dashboard  | ✓      | ✓       | ✓      | ✓          |
| Crops      | ✓      | ✓       | ✗      | ✓          |
| Livestock  | ✓      | ✓       | ✗      | ✓          |
| Inventory  | ✓      | ✓       | ✗      | ✗          |
| Finance    | ✓      | ✓       | ✗      | ✓          |
| Tasks      | ✓      | ✓       | ✓      | ✓          |
| Activities | ✓      | ✓       | ✓      | ✓          |
| Analytics  | ✗      | ✓       | ✗      | ✓          |
| Admin      | ✗      | ✗*      | ✗      | ✗          |

*Only visible if user.is_superuser = True (Admin account only)

---

## Quick Access URLs

- **Login:** http://127.0.0.1:8000/login/
- **Dashboard:** http://127.0.0.1:8000/dashboard/
- **Admin Panel:** http://127.0.0.1:8000/admin-dashboard/
- **User Management:** http://127.0.0.1:8000/admin/users/

---

## Notes

- Each user profile has sample data (farm name, location, etc.)
- Workers have no crops/livestock/finances by default (limited role)
- Admin user has both Manager role and Superuser privileges for full access
- **Only superuser (admin) can access the Admin Panel** - regular users won't see this menu
- To change a user's role, log in as admin and go to Admin Panel > User Management
