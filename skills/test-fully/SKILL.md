# Test Fully - Comprehensive Testing Skill

## Version
- **Version:** 1.0.0
- **Last Updated:** 2025-02-10
- **Compatibility:** All major testing frameworks

## Purpose
Generate comprehensive test suites covering unit, integration, E2E, and performance testing for any codebase. Automatically detects testing frameworks and follows language-specific best practices.

---

## How to Use This Skill

### Quick Usage
```bash
# Test specific file
/test-fully src/utils/validator.js

# Test with focus on specific type
/test-fully --focus unit
/test-fully --focus integration
/test-fully --focus e2e
/test-fully --focus performance

# Test entire module
/test-fully src/features/auth/

# Update existing tests
/test-fully update tests for payment.js
```

---

## Testing Strategy

When this skill is invoked, I will:

### 1. **Code Analysis Phase**
- Read and understand the codebase structure
- Identify all functions, methods, and components
- Map dependencies and integration points
- Detect existing patterns and conventions

### 2. **Framework Detection Phase**
Automatically identify the testing framework in use:

**JavaScript/TypeScript:**
- Jest (check for jest.config.js, package.json scripts)
- Vitest (check for vitest.config.ts)
- Mocha + Chai (check for .mocharc.json)
- Jasmine (check for jasmine.json)

**Python:**
- pytest (check for pytest.ini, conftest.py)
- unittest (check for test_*.py pattern)
- nose2 (check for nose2.cfg)

**Java:**
- JUnit 5 (check for @Test annotations, pom.xml)
- JUnit 4 (check for older @Test imports)
- TestNG (check for testng.xml)

**Other Languages:**
- Go: `testing` package
- Ruby: RSpec or Minitest
- C#: xUnit, NUnit, or MSTest
- PHP: PHPUnit
- Rust: Built-in test framework

**E2E Frameworks:**
- Playwright
- Cypress
- Selenium
- Puppeteer

### 3. **Test Generation Phase**

Create tests covering:

#### A. Unit Tests
**Focus:** Individual functions/methods in isolation

**Coverage Areas:**
- ✅ Happy path (valid inputs, expected outputs)
- ✅ Edge cases (empty strings, null, undefined, zero, negative numbers)
- ✅ Boundary conditions (min/max values, limits)
- ✅ Type validation (wrong types, type coercion)
- ✅ Error handling (exceptions, error messages)
- ✅ State management (before/after state changes)
- ✅ Side effects (external calls, mutations)

**Example Patterns:**

**JavaScript (Jest):**
```javascript
describe('validateEmail', () => {
  // Happy path
  test('should return true for valid email', () => {
    expect(validateEmail('user@example.com')).toBe(true);
  });

  // Edge cases
  test('should return false for empty string', () => {
    expect(validateEmail('')).toBe(false);
  });

  test('should return false for null', () => {
    expect(validateEmail(null)).toBe(false);
  });

  // Boundary conditions
  test('should handle very long email addresses', () => {
    const longEmail = 'a'.repeat(100) + '@example.com';
    expect(validateEmail(longEmail)).toBe(true);
  });

  // Format validation
  test('should reject email without @', () => {
    expect(validateEmail('userexample.com')).toBe(false);
  });

  test('should reject email without domain', () => {
    expect(validateEmail('user@')).toBe(false);
  });
});
```

**Python (pytest):**
```python
class TestValidateEmail:
    """Test email validation function"""

    # Happy path
    def test_valid_email(self):
        assert validate_email('user@example.com') is True

    # Edge cases
    def test_empty_string(self):
        assert validate_email('') is False

    def test_none_value(self):
        assert validate_email(None) is False

    # Boundary conditions
    def test_long_email(self):
        long_email = 'a' * 100 + '@example.com'
        assert validate_email(long_email) is True

    # Format validation
    @pytest.mark.parametrize('invalid_email', [
        'userexample.com',
        'user@',
        '@example.com',
        'user @example.com',
    ])
    def test_invalid_formats(self, invalid_email):
        assert validate_email(invalid_email) is False
```

#### B. Integration Tests
**Focus:** How components work together

**Coverage Areas:**
- ✅ API endpoints with database
- ✅ Service-to-service communication
- ✅ Data flow between modules
- ✅ External API integrations
- ✅ Authentication flows
- ✅ Transaction handling

**Example Patterns:**

**JavaScript (Jest + Supertest):**
```javascript
describe('POST /api/users', () => {
  let db;

  beforeAll(async () => {
    db = await setupTestDatabase();
  });

  afterAll(async () => {
    await db.close();
  });

  beforeEach(async () => {
    await db.clear('users');
  });

  test('should create user and return 201', async () => {
    const userData = {
      email: 'test@example.com',
      name: 'Test User'
    };

    const response = await request(app)
      .post('/api/users')
      .send(userData)
      .expect(201);

    expect(response.body).toMatchObject({
      id: expect.any(String),
      email: userData.email,
      name: userData.name
    });

    // Verify database state
    const user = await db.findUserByEmail(userData.email);
    expect(user).toBeTruthy();
    expect(user.name).toBe(userData.name);
  });

  test('should return 400 for duplicate email', async () => {
    const userData = { email: 'test@example.com', name: 'User' };

    // Create first user
    await request(app).post('/api/users').send(userData);

    // Attempt duplicate
    const response = await request(app)
      .post('/api/users')
      .send(userData)
      .expect(400);

    expect(response.body.error).toContain('already exists');
  });
});
```

**Python (pytest + Flask):**
```python
class TestUserAPI:
    @pytest.fixture(autouse=True)
    def setup(self, client, db):
        """Setup test database before each test"""
        self.client = client
        self.db = db
        db.clear_users()

    def test_create_user_success(self):
        """Should create user and return 201"""
        user_data = {
            'email': 'test@example.com',
            'name': 'Test User'
        }

        response = self.client.post('/api/users', json=user_data)

        assert response.status_code == 201
        data = response.get_json()
        assert 'id' in data
        assert data['email'] == user_data['email']

        # Verify database state
        user = self.db.find_user_by_email(user_data['email'])
        assert user is not None
        assert user.name == user_data['name']

    def test_create_user_duplicate_email(self):
        """Should return 400 for duplicate email"""
        user_data = {'email': 'test@example.com', 'name': 'User'}

        # Create first user
        self.client.post('/api/users', json=user_data)

        # Attempt duplicate
        response = self.client.post('/api/users', json=user_data)

        assert response.status_code == 400
        assert 'already exists' in response.get_json()['error']
```

#### C. End-to-End Tests
**Focus:** Complete user workflows

**Coverage Areas:**
- ✅ User authentication flows
- ✅ Multi-step processes (checkout, registration)
- ✅ Form submissions
- ✅ Navigation flows
- ✅ Cross-page interactions

**Example Patterns:**

**Playwright (TypeScript):**
```typescript
import { test, expect } from '@playwright/test';

test.describe('User Registration Flow', () => {
  test('should complete full registration process', async ({ page }) => {
    // Navigate to registration
    await page.goto('/register');

    // Fill registration form
    await page.fill('[data-testid="email-input"]', 'newuser@example.com');
    await page.fill('[data-testid="password-input"]', 'SecurePass123!');
    await page.fill('[data-testid="confirm-password"]', 'SecurePass123!');
    await page.fill('[data-testid="name-input"]', 'John Doe');

    // Submit form
    await page.click('[data-testid="submit-button"]');

    // Verify confirmation page
    await expect(page).toHaveURL(/.*\/welcome/);
    await expect(page.locator('h1')).toContainText('Welcome, John Doe');

    // Verify email sent (check for confirmation message)
    await expect(page.locator('.success-message')).toContainText(
      'verification email sent'
    );

    // Test logout
    await page.click('[data-testid="logout-button"]');
    await expect(page).toHaveURL('/login');
  });

  test('should show validation errors for invalid input', async ({ page }) => {
    await page.goto('/register');

    // Submit empty form
    await page.click('[data-testid="submit-button"]');

    // Check for validation errors
    await expect(page.locator('.error-email')).toBeVisible();
    await expect(page.locator('.error-password')).toBeVisible();
  });
});
```

**Cypress (JavaScript):**
```javascript
describe('E-commerce Checkout Flow', () => {
  beforeEach(() => {
    cy.login('customer@example.com', 'password');
  });

  it('should complete purchase successfully', () => {
    // Add item to cart
    cy.visit('/products');
    cy.get('[data-testid="product-1"]').click();
    cy.get('[data-testid="add-to-cart"]').click();

    // Verify cart
    cy.get('[data-testid="cart-badge"]').should('contain', '1');

    // Go to checkout
    cy.get('[data-testid="cart-icon"]').click();
    cy.get('[data-testid="checkout-button"]').click();

    // Fill shipping information
    cy.get('#address').type('123 Main St');
    cy.get('#city').type('New York');
    cy.get('#zip').type('10001');

    // Continue to payment
    cy.get('[data-testid="continue-to-payment"]').click();

    // Fill payment (use test card)
    cy.get('#card-number').type('4242424242424242');
    cy.get('#expiry').type('12/25');
    cy.get('#cvv').type('123');

    // Submit order
    cy.get('[data-testid="place-order"]').click();

    // Verify success
    cy.url().should('include', '/order-confirmation');
    cy.get('[data-testid="order-number"]').should('be.visible');
    cy.get('.success-message').should('contain', 'Order placed successfully');
  });
});
```

#### D. Performance Tests
**Focus:** Speed, scalability, resource usage

**Coverage Areas:**
- ✅ Load testing (concurrent users)
- ✅ Stress testing (breaking points)
- ✅ Response time benchmarks
- ✅ Memory usage
- ✅ Database query performance
- ✅ API rate limits

**Example Patterns:**

**JavaScript (Jest Performance):**
```javascript
describe('Performance Tests', () => {
  test('should process 10,000 records in under 1 second', () => {
    const records = generateMockRecords(10000);

    const startTime = performance.now();
    const result = processRecords(records);
    const endTime = performance.now();

    const duration = endTime - startTime;

    expect(result).toHaveLength(10000);
    expect(duration).toBeLessThan(1000); // Less than 1 second
  });

  test('should not leak memory', () => {
    const memBefore = process.memoryUsage().heapUsed;

    // Perform operation 1000 times
    for (let i = 0; i < 1000; i++) {
      processData(generateMockData());
    }

    // Force garbage collection if available
    if (global.gc) global.gc();

    const memAfter = process.memoryUsage().heapUsed;
    const memIncrease = memAfter - memBefore;

    // Memory increase should be minimal (< 10MB)
    expect(memIncrease).toBeLessThan(10 * 1024 * 1024);
  });
});
```

**Python (pytest + locust for load testing):**
```python
from locust import HttpUser, task, between

class APILoadTest(HttpUser):
    wait_time = between(1, 3)

    @task(3)  # Weight: 3x more frequent
    def get_users(self):
        """Test GET /api/users endpoint"""
        self.client.get("/api/users")

    @task(1)
    def create_user(self):
        """Test POST /api/users endpoint"""
        self.client.post("/api/users", json={
            "email": f"user{random.randint(1, 10000)}@example.com",
            "name": "Test User"
        })

    @task(2)
    def search_users(self):
        """Test search functionality"""
        self.client.get(f"/api/users/search?q=test")

# Run with: locust -f test_load.py --users 100 --spawn-rate 10
```

---

## Framework-Specific Best Practices

### Jest (JavaScript/TypeScript)

**Test Organization:**
```javascript
// src/utils/__tests__/validator.test.js
// or
// src/utils/validator.spec.js

// Use describe blocks for grouping
describe('Module: validator', () => {
  describe('Function: validateEmail', () => {
    test('should ...', () => {});
  });

  describe('Function: validatePhone', () => {
    test('should ...', () => {});
  });
});
```

**Common Patterns:**
- Use `beforeEach`/`afterEach` for setup/cleanup
- Use `jest.mock()` for mocking modules
- Use `jest.fn()` for spy functions
- Use `.toMatchSnapshot()` for component testing
- Use `.toMatchObject()` for partial matching

### pytest (Python)

**Test Organization:**
```python
# tests/test_validator.py
# or
# tests/unit/test_validator.py

class TestValidateEmail:
    """Group related tests in classes"""

    @pytest.fixture
    def sample_email(self):
        """Reusable test data"""
        return "test@example.com"

    def test_valid_email(self, sample_email):
        """Test description"""
        assert validate_email(sample_email) is True
```

**Common Patterns:**
- Use fixtures for reusable setup
- Use `@pytest.mark.parametrize` for multiple inputs
- Use `pytest.raises()` for exception testing
- Use `monkeypatch` for mocking
- Use `pytest-cov` for coverage reports

### JUnit (Java)

**Test Organization:**
```java
// src/test/java/com/example/ValidatorTest.java

@DisplayName("Email Validator Tests")
class ValidatorTest {

    @BeforeEach
    void setUp() {
        // Setup before each test
    }

    @Test
    @DisplayName("Should return true for valid email")
    void testValidEmail() {
        assertTrue(Validator.validateEmail("user@example.com"));
    }

    @ParameterizedTest
    @ValueSource(strings = {"invalid", "@example.com", "user@"})
    @DisplayName("Should return false for invalid emails")
    void testInvalidEmails(String email) {
        assertFalse(Validator.validateEmail(email));
    }
}
```

---

## Test Quality Checklist

When generating tests, ensure:

### ✅ Test Independence
- Each test can run alone
- Tests don't depend on execution order
- Proper cleanup in afterEach/teardown

### ✅ Clear Naming
- Test names describe what they test
- Use "should" statements
- Include expected behavior

**Good:**
```javascript
test('should return 404 when user not found', () => {});
test('should throw ValidationError for negative amounts', () => {});
```

**Bad:**
```javascript
test('test1', () => {});
test('user test', () => {});
```

### ✅ Arrange-Act-Assert Pattern
```javascript
test('should calculate discount correctly', () => {
  // Arrange: Setup test data
  const price = 100;
  const discountPercent = 10;

  // Act: Execute the function
  const result = calculateDiscount(price, discountPercent);

  // Assert: Verify the result
  expect(result).toBe(90);
});
```

### ✅ Comprehensive Coverage
- Test happy paths
- Test error paths
- Test edge cases
- Test boundary conditions

### ✅ Appropriate Mocking
- Mock external dependencies (APIs, databases)
- Don't mock everything (test real code when possible)
- Verify mock interactions when needed

### ✅ Meaningful Assertions
```javascript
// Good: Specific assertions
expect(user.email).toBe('test@example.com');
expect(response.status).toBe(200);

// Bad: Vague assertions
expect(user).toBeTruthy();
expect(response).toBeDefined();
```

---

## Common Testing Patterns

### Pattern 1: Testing Async Code

**JavaScript (Jest):**
```javascript
test('should fetch user data', async () => {
  const data = await fetchUser(123);
  expect(data.name).toBe('John Doe');
});

test('should handle fetch errors', async () => {
  await expect(fetchUser(999)).rejects.toThrow('User not found');
});
```

### Pattern 2: Testing with Mocks

**JavaScript (Jest):**
```javascript
// Mock external API
jest.mock('../services/api');

test('should call API with correct parameters', async () => {
  const mockFetch = api.fetchData.mockResolvedValue({ data: 'test' });

  await getData('users');

  expect(mockFetch).toHaveBeenCalledWith('users');
  expect(mockFetch).toHaveBeenCalledTimes(1);
});
```

### Pattern 3: Testing React Components

**JavaScript (React Testing Library):**
```javascript
import { render, screen, fireEvent } from '@testing-library/react';

test('should update count when button clicked', () => {
  render(<Counter />);

  const button = screen.getByRole('button', { name: /increment/i });
  const count = screen.getByTestId('count');

  expect(count).toHaveTextContent('0');

  fireEvent.click(button);

  expect(count).toHaveTextContent('1');
});
```

### Pattern 4: Testing with Database

**Python (pytest + SQLAlchemy):**
```python
@pytest.fixture
def db_session():
    """Create test database session"""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()

def test_create_user(db_session):
    """Should create user in database"""
    user = User(email='test@example.com', name='Test')
    db_session.add(user)
    db_session.commit()

    saved_user = db_session.query(User).filter_by(email='test@example.com').first()
    assert saved_user is not None
    assert saved_user.name == 'Test'
```

---

## Output Format

When generating tests, provide:

### 1. Test Files
```
tests/
├── unit/
│   ├── test_validator.py
│   └── test_calculator.py
├── integration/
│   └── test_api.py
└── e2e/
    └── test_user_flow.spec.ts
```

### 2. Test Code
- Complete, runnable test files
- Proper imports and setup
- Clear test names and descriptions
- Helpful comments

### 3. Setup Instructions
```bash
# Install dependencies
npm install --save-dev jest @testing-library/react

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test -- validator.test.js
```

### 4. Coverage Report
```
File              | % Stmts | % Branch | % Funcs | % Lines
------------------|---------|----------|---------|--------
validator.js      |   95.0  |   88.0   |  100.0  |   95.0
calculator.js     |   80.0  |   75.0   |   80.0  |   80.0
```

### 5. Coverage Gaps
Identify untested areas:
- Missing error handling tests
- Uncovered edge cases
- Integration points without tests

---

## Anti-Patterns to Avoid

### ❌ Testing Implementation Details
```javascript
// Bad: Testing internal state
expect(component.state.count).toBe(1);

// Good: Testing behavior
expect(screen.getByText('Count: 1')).toBeInTheDocument();
```

### ❌ Overly Brittle Tests
```javascript
// Bad: Exact string matching
expect(message).toBe('Error: User john@example.com not found in database table users');

// Good: Flexible matching
expect(message).toContain('not found');
```

### ❌ Testing Too Much at Once
```javascript
// Bad: One giant test
test('should handle entire user lifecycle', () => {
  // 100 lines of test code...
});

// Good: Split into focused tests
test('should create user', () => {});
test('should update user', () => {});
test('should delete user', () => {});
```

---

## Instructions

When this skill is invoked:

1. **Analyze the code**
   - Read the file(s) provided
   - Understand the logic and dependencies
   - Identify testing framework in use

2. **Plan the test strategy**
   - Determine which test types are needed (unit/integration/e2e)
   - Identify critical paths to test
   - Note external dependencies to mock

3. **Generate comprehensive tests**
   - Follow the framework's best practices
   - Use patterns from this skill document
   - Cover happy paths, edge cases, and errors
   - Add clear descriptions and comments

4. **Provide execution instructions**
   - Show how to install test dependencies
   - Provide commands to run tests
   - Explain how to check coverage

5. **Report gaps**
   - Identify areas that need additional testing
   - Suggest improvements to test coverage
   - Note any limitations or assumptions

---

Now, please help me test the following code comprehensively:
