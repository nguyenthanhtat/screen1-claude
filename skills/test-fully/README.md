# Test-Fully Skill

A comprehensive testing skill for Claude Code that generates complete test coverage for any codebase, supporting all major testing frameworks and languages.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Supported Frameworks](#supported-frameworks)
- [Test Types](#test-types)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Contributing](#contributing)

---

## Overview

Test-Fully is a Claude Code skill that helps you create thorough, production-ready test suites. It analyzes your code, detects your testing framework, and generates comprehensive tests following industry best practices.

### What It Covers

- ✅ **Unit Tests** - Individual functions/methods in isolation
- ✅ **Integration Tests** - Component interactions, API endpoints, database operations
- ✅ **End-to-End Tests** - Complete user workflows and scenarios
- ✅ **Performance Tests** - Load testing, benchmarks, resource usage
- ✅ **Error Scenarios** - Edge cases, boundary conditions, exception handling
- ✅ **Regression Prevention** - Ensure changes don't break existing functionality

---

## Features

### 🎯 Automatic Framework Detection

The skill automatically identifies your testing setup:

**JavaScript/TypeScript:**
- Jest (React, Node.js, Next.js)
- Vitest (Vite projects)
- Mocha + Chai (Traditional Node.js)
- Jasmine (Angular, legacy projects)

**Python:**
- pytest (Modern Python testing)
- unittest (Standard library)
- nose2 (Extended unittest)

**Java:**
- JUnit 5 (Jupiter)
- JUnit 4 (Vintage)
- TestNG

**Other Languages:**
- Go (testing package)
- Ruby (RSpec, Minitest)
- C# (xUnit, NUnit, MSTest)
- PHP (PHPUnit)
- Rust (built-in tests)

**E2E Frameworks:**
- Playwright (Modern, cross-browser)
- Cypress (Developer-friendly)
- Selenium (Industry standard)
- Puppeteer (Chrome automation)

### 📝 Comprehensive Coverage

- **Happy Paths** - Valid inputs and expected outputs
- **Edge Cases** - Empty values, null, undefined, special characters
- **Boundary Conditions** - Min/max values, size limits
- **Type Validation** - Wrong types, type coercion
- **Error Handling** - Exceptions, error messages, recovery
- **State Management** - Before/after conditions
- **Side Effects** - External calls, data mutations

### 🎨 Clean, Readable Tests

- Descriptive test names
- Clear arrange-act-assert structure
- Helpful comments explaining what's being tested
- Consistent formatting and conventions
- Proper use of mocks and fixtures

### 🚀 Production-Ready

- Follows framework best practices
- Includes setup/teardown code
- Provides execution instructions
- Generates coverage reports
- Identifies testing gaps

---

## Installation

### Quick Install

See [INSTALLATION.md](INSTALLATION.md) for detailed instructions.

**Global Installation (Recommended):**

```bash
# Windows PowerShell
Copy-Item -Recurse ".\screen1-claude\skills\test-fully" "$env:USERPROFILE\.claude\skills\test-fully"

# macOS/Linux
cp -r ./screen1-claude/skills/test-fully ~/.claude/skills/
```

**Project-Specific Installation:**

```bash
# Copy to project
cp -r ./screen1-claude/skills/test-fully ./skills/

# Configure
echo "skills:" > .claude
echo "  - ./skills/test-fully" >> .claude
```

**Verify Installation:**

```bash
/test-fully
# Should activate the skill
```

---

## Usage

### Basic Usage

```bash
# Test current code in context
/test-fully

# Test specific file
/test-fully path/to/file.js

# Test entire directory
/test-fully src/features/auth/
```

### Focused Testing

```bash
# Focus on unit tests only
/test-fully --focus unit

# Focus on integration tests
/test-fully --focus integration

# Focus on E2E tests
/test-fully --focus e2e

# Focus on performance tests
/test-fully --focus performance
```

### Update Existing Tests

```bash
# Add tests for new feature
/test-fully update tests for new login flow

# Improve coverage
/test-fully improve test coverage for payment.js

# Fix failing tests
/test-fully fix tests for UserProfile component
```

---

## Supported Frameworks

### JavaScript/TypeScript

#### Jest
```json
// package.json
{
  "scripts": {
    "test": "jest",
    "test:coverage": "jest --coverage"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "@testing-library/react": "^14.0.0"
  }
}
```

**Usage:**
```bash
/test-fully src/components/Button.tsx
# Generates Button.test.tsx with React Testing Library
```

#### Vitest
```typescript
// vitest.config.ts
export default {
  test: {
    globals: true,
    environment: 'jsdom'
  }
}
```

**Usage:**
```bash
/test-fully src/utils/format.ts
# Generates format.spec.ts for Vitest
```

#### Mocha + Chai
```javascript
// .mocharc.json
{
  "require": "chai/register-expect",
  "spec": "test/**/*.spec.js"
}
```

**Usage:**
```bash
/test-fully src/services/api.js
# Generates test/services/api.spec.js with Chai assertions
```

### Python

#### pytest
```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

**Usage:**
```bash
/test-fully app/services/validator.py
# Generates tests/test_validator.py
```

#### unittest
```python
# Standard library, no config needed
```

**Usage:**
```bash
/test-fully src/calculator.py
# Generates test_calculator.py with unittest.TestCase
```

### Java

#### JUnit 5
```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.9.0</version>
    <scope>test</scope>
</dependency>
```

**Usage:**
```bash
/test-fully src/main/java/com/example/UserService.java
# Generates src/test/java/com/example/UserServiceTest.java
```

### E2E Testing

#### Playwright
```typescript
// playwright.config.ts
export default {
  testDir: './e2e',
  use: {
    baseURL: 'http://localhost:3000'
  }
}
```

**Usage:**
```bash
/test-fully --focus e2e app/checkout
# Generates e2e/checkout.spec.ts
```

---

## Test Types

### 1. Unit Tests

**Purpose:** Test individual functions/methods in isolation

**When to Use:**
- Testing pure functions
- Testing utility functions
- Testing business logic
- Testing validators and formatters

**Example:**
```bash
/test-fully --focus unit src/utils/formatCurrency.js
```

**Generated:**
```javascript
describe('formatCurrency', () => {
  test('should format positive numbers', () => {
    expect(formatCurrency(1234.56)).toBe('$1,234.56');
  });

  test('should handle zero', () => {
    expect(formatCurrency(0)).toBe('$0.00');
  });

  test('should handle negative numbers', () => {
    expect(formatCurrency(-100)).toBe('-$100.00');
  });

  test('should throw for non-numbers', () => {
    expect(() => formatCurrency('invalid')).toThrow();
  });
});
```

### 2. Integration Tests

**Purpose:** Test how components work together

**When to Use:**
- Testing API endpoints
- Testing database operations
- Testing service interactions
- Testing authentication flows

**Example:**
```bash
/test-fully --focus integration src/api/users.js
```

**Generated:**
```javascript
describe('POST /api/users', () => {
  let db;

  beforeAll(async () => {
    db = await setupTestDB();
  });

  test('should create user and return 201', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', name: 'Test' })
      .expect(201);

    const user = await db.users.findByEmail('test@example.com');
    expect(user).toBeTruthy();
  });
});
```

### 3. End-to-End Tests

**Purpose:** Test complete user workflows

**When to Use:**
- Testing user registration/login
- Testing checkout processes
- Testing multi-page workflows
- Testing critical business processes

**Example:**
```bash
/test-fully --focus e2e features/checkout
```

**Generated:**
```typescript
test('should complete purchase flow', async ({ page }) => {
  await page.goto('/products');
  await page.click('[data-testid="add-to-cart"]');
  await page.click('[data-testid="checkout"]');
  await page.fill('#card-number', '4242424242424242');
  await page.click('[data-testid="place-order"]');
  await expect(page).toHaveURL(/.*order-confirmation/);
});
```

### 4. Performance Tests

**Purpose:** Test speed, scalability, resource usage

**When to Use:**
- Testing API response times
- Testing with large datasets
- Testing memory usage
- Load testing

**Example:**
```bash
/test-fully --focus performance src/services/dataProcessor.js
```

**Generated:**
```javascript
test('should process 10k records in < 1 second', () => {
  const data = generateMockData(10000);
  const start = performance.now();

  processData(data);

  const duration = performance.now() - start;
  expect(duration).toBeLessThan(1000);
});
```

---

## Examples

### Example 1: Testing a React Component

**Input:**
```bash
/test-fully src/components/LoginForm.tsx
```

**Generated Test:**
```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  test('should render email and password inputs', () => {
    render(<LoginForm onSubmit={jest.fn()} />);

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  });

  test('should call onSubmit with form data', async () => {
    const onSubmit = jest.fn();
    render(<LoginForm onSubmit={onSubmit} />);

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'user@example.com' }
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password123' }
    });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        email: 'user@example.com',
        password: 'password123'
      });
    });
  });

  test('should show validation errors for empty fields', async () => {
    render(<LoginForm onSubmit={jest.fn()} />);

    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(screen.getByText(/email is required/i)).toBeInTheDocument();
      expect(screen.getByText(/password is required/i)).toBeInTheDocument();
    });
  });
});
```

### Example 2: Testing a Python API

**Input:**
```bash
/test-fully --focus integration app/api/products.py
```

**Generated Test:**
```python
import pytest
from app import create_app, db
from app.models import Product

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

class TestProductAPI:
    def test_get_products(self, client):
        """Should return list of products"""
        # Create test products
        product1 = Product(name='Product 1', price=10.00)
        product2 = Product(name='Product 2', price=20.00)
        db.session.add_all([product1, product2])
        db.session.commit()

        response = client.get('/api/products')

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        assert data[0]['name'] == 'Product 1'

    def test_create_product(self, client):
        """Should create new product"""
        product_data = {
            'name': 'New Product',
            'price': 15.99,
            'description': 'Test product'
        }

        response = client.post('/api/products', json=product_data)

        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == 'New Product'
        assert data['price'] == 15.99

        # Verify in database
        product = Product.query.filter_by(name='New Product').first()
        assert product is not None
```

### Example 3: Testing a Java Service

**Input:**
```bash
/test-fully src/main/java/com/example/OrderService.java
```

**Generated Test:**
```java
import org.junit.jupiter.api.*;
import org.mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@DisplayName("Order Service Tests")
class OrderServiceTest {

    @Mock
    private OrderRepository orderRepository;

    @Mock
    private PaymentService paymentService;

    @InjectMocks
    private OrderService orderService;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    @DisplayName("Should create order successfully")
    void testCreateOrder() {
        // Arrange
        Order order = new Order("user123", 99.99);
        when(orderRepository.save(any(Order.class))).thenReturn(order);
        when(paymentService.processPayment(anyDouble())).thenReturn(true);

        // Act
        Order result = orderService.createOrder("user123", 99.99);

        // Assert
        assertNotNull(result);
        assertEquals("user123", result.getUserId());
        assertEquals(99.99, result.getAmount());
        verify(orderRepository).save(any(Order.class));
        verify(paymentService).processPayment(99.99);
    }

    @Test
    @DisplayName("Should throw exception when payment fails")
    void testCreateOrderPaymentFails() {
        // Arrange
        when(paymentService.processPayment(anyDouble())).thenReturn(false);

        // Act & Assert
        assertThrows(PaymentFailedException.class, () -> {
            orderService.createOrder("user123", 99.99);
        });
    }
}
```

---

## Configuration

### .claude File

```yaml
# .claude
skills:
  - ./skills/test-fully

# Optional: Custom commands
commands:
  test: "Use /test-fully for comprehensive testing"
  unit: "Use /test-fully --focus unit"
  integration: "Use /test-fully --focus integration"
  e2e: "Use /test-fully --focus e2e"
  perf: "Use /test-fully --focus performance"

# Optional: Test preferences
testPreferences:
  framework: jest  # or pytest, junit, etc.
  coverage: true
  verbose: true
```

### Framework Configuration

**Jest (package.json):**
```json
{
  "jest": {
    "testEnvironment": "jsdom",
    "coverageThreshold": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

**pytest (pytest.ini):**
```ini
[pytest]
testpaths = tests
addopts =
    --cov=app
    --cov-report=html
    --cov-report=term
    --cov-fail-under=80
```

---

## Best Practices

### 1. Test Organization

**Organize by feature:**
```
tests/
├── unit/
│   ├── utils/
│   │   ├── test_validator.py
│   │   └── test_formatter.py
│   └── services/
│       └── test_auth.py
├── integration/
│   └── test_api.py
└── e2e/
    └── test_checkout_flow.spec.ts
```

### 2. Naming Conventions

**Good test names:**
- `should return true for valid email`
- `should throw ValidationError for negative amount`
- `should create user and send welcome email`

**Bad test names:**
- `test1`
- `user test`
- `it works`

### 3. Test Independence

Each test should:
- Run independently
- Not rely on other tests
- Clean up after itself
- Not affect global state

### 4. Use Appropriate Mocks

**Mock external dependencies:**
- APIs
- Databases (for unit tests)
- File system
- Date/time
- Random generators

**Don't mock:**
- Internal functions you're testing
- Simple utility functions
- Test helpers

### 5. Meaningful Assertions

```javascript
// Good: Specific assertions
expect(user.email).toBe('test@example.com');
expect(response.status).toBe(201);
expect(errors).toHaveLength(2);

// Bad: Vague assertions
expect(user).toBeTruthy();
expect(response).toBeDefined();
expect(errors).toBeTruthy();
```

---

## Troubleshooting

### Tests Not Running

**Check test framework installation:**
```bash
# JavaScript
npm list jest

# Python
pip show pytest

# Java
mvn dependency:tree | grep junit
```

**Verify test scripts:**
```json
// package.json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch"
  }
}
```

### Low Coverage

**Identify untested code:**
```bash
# JavaScript (Jest)
npm test -- --coverage

# Python (pytest)
pytest --cov=app --cov-report=html

# Open coverage report
open coverage/index.html
```

### Slow Tests

**Profile test execution:**
```bash
# Jest
npm test -- --verbose

# pytest
pytest --durations=10
```

**Optimize:**
- Reduce database queries
- Use in-memory databases for tests
- Parallelize test execution
- Mock heavy operations

### Flaky Tests

**Common causes:**
- Race conditions in async code
- Timing dependencies
- Shared state between tests
- External dependencies

**Solutions:**
```javascript
// Bad: Timing-dependent
setTimeout(() => expect(value).toBe(5), 100);

// Good: Wait for condition
await waitFor(() => expect(value).toBe(5));
```

---

## FAQ

### Q: Which test type should I use?

**A:** Use all of them, but prioritize:
1. **Unit tests** for business logic (70%)
2. **Integration tests** for critical paths (20%)
3. **E2E tests** for key workflows (10%)

### Q: How much coverage is enough?

**A:** Aim for:
- **80-90%** line coverage overall
- **100%** coverage for critical business logic
- **Focus on quality** over quantity

### Q: Should I test private methods?

**A:** No, test through public interfaces. Private methods are implementation details.

### Q: How do I test async code?

**A:** Use async/await or return promises:
```javascript
// Method 1: async/await
test('async test', async () => {
  const result = await fetchData();
  expect(result).toBe('data');
});

// Method 2: return promise
test('async test', () => {
  return fetchData().then(result => {
    expect(result).toBe('data');
  });
});
```

### Q: How do I test React hooks?

**A:** Use @testing-library/react-hooks:
```javascript
import { renderHook, act } from '@testing-library/react-hooks';

test('should increment counter', () => {
  const { result } = renderHook(() => useCounter());

  act(() => {
    result.current.increment();
  });

  expect(result.current.count).toBe(1);
});
```

---

## Contributing

### Customizing the Skill

Edit `SKILL.md` to add:
- Team-specific testing patterns
- Custom framework configurations
- Project-specific test utilities
- Company testing standards

### Sharing Improvements

If you enhance the skill:
1. Document your changes
2. Add examples
3. Submit a pull request to the repository
4. Share with your team

---

## Additional Resources

- [QUICK_START.md](QUICK_START.md) - Get started in 5 minutes
- [INSTALLATION.md](INSTALLATION.md) - Detailed installation guide
- [STRUCTURE.md](STRUCTURE.md) - How the skill works
- [SKILL.md](SKILL.md) - Complete skill documentation

---

## Version

- **Version:** 1.0.0
- **Last Updated:** 2025-02-10
- **Maintainer:** screen1-claude team

---

**Happy Testing! 🚀**
