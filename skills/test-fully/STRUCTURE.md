# Test-Fully Skill Structure

## Overview

This document explains the architecture, design decisions, and implementation details of the test-fully skill.

---

## Directory Layout

```
test-fully/
│
├── README.md              # Main user documentation
├── QUICK_START.md         # 5-minute getting started guide
├── INSTALLATION.md        # Detailed installation instructions
├── STRUCTURE.md           # This file - architecture documentation
├── .claude.example        # Example configuration template
│
└── SKILL.md               # 🎯 CORE SKILL LOGIC
    ├── Framework detection
    ├── Test generation strategies
    ├── Pattern library
    ├── Best practices
    └── Anti-patterns to avoid
```

**Total Size:** ~15KB
**Lines of Knowledge:** ~1500 lines

---

## How It Works

### 1. Skill Invocation Flow

```
User: /test-fully src/utils/validator.js
           │
           ├─→ Claude Code loads SKILL.md
           │
           ├─→ Code Analysis Phase
           │   ├─ Read target file(s)
           │   ├─ Understand code structure
           │   ├─ Identify functions/classes
           │   └─ Map dependencies
           │
           ├─→ Framework Detection Phase
           │   ├─ Check package.json (JavaScript)
           │   ├─ Check pytest.ini (Python)
           │   ├─ Check pom.xml (Java)
           │   ├─ Detect test file patterns
           │   └─ Select appropriate framework
           │
           ├─→ Test Strategy Planning
           │   ├─ Determine test types needed
           │   ├─ Identify critical paths
           │   ├─ Note mocking requirements
           │   └─ Plan test structure
           │
           ├─→ Test Generation Phase
           │   ├─ Generate unit tests
           │   ├─ Generate integration tests
           │   ├─ Generate E2E tests (if needed)
           │   ├─ Add setup/teardown
           │   └─ Include documentation
           │
           └─→ Output & Instructions
               ├─ Complete test files
               ├─ Installation commands
               ├─ Execution commands
               └─ Coverage report
```

---

## Core Components

### 1. Framework Detection Logic

**JavaScript/TypeScript Detection:**
```javascript
// Algorithm:
1. Check package.json for test scripts
   - "test": "jest" → Jest
   - "test": "vitest" → Vitest
   - "test": "mocha" → Mocha

2. Check for config files
   - jest.config.js → Jest
   - vitest.config.ts → Vitest
   - .mocharc.json → Mocha

3. Check test file patterns
   - *.test.js → Jest/Vitest
   - *.spec.js → Jasmine/Mocha
```

**Python Detection:**
```python
# Algorithm:
1. Check for config files
   - pytest.ini → pytest
   - nose2.cfg → nose2
   - No config → unittest (standard library)

2. Check existing test files
   - test_*.py with pytest imports → pytest
   - test_*.py with unittest.TestCase → unittest
```

**Java Detection:**
```java
// Algorithm:
1. Check pom.xml or build.gradle
   - junit-jupiter → JUnit 5
   - junit-vintage → JUnit 4
   - testng → TestNG

2. Check annotations in existing tests
   - @Test from org.junit.jupiter → JUnit 5
   - @Test from org.junit → JUnit 4
```

### 2. Test Generation Strategy

**Unit Test Generation:**
```
For each function/method:
  1. Analyze function signature
     - Parameters and types
     - Return type
     - Throws/raises declarations

  2. Generate happy path tests
     - Valid inputs
     - Expected outputs

  3. Generate edge case tests
     - Empty/null/undefined values
     - Boundary conditions
     - Special characters

  4. Generate error tests
     - Invalid inputs
     - Type errors
     - Expected exceptions

  5. Add documentation
     - Test descriptions
     - Explanation comments
```

**Integration Test Generation:**
```
For each integration point:
  1. Identify dependencies
     - Databases
     - External APIs
     - File systems
     - Other services

  2. Plan test setup
     - Test databases
     - Mock servers
     - Fixtures

  3. Generate test scenarios
     - Success paths
     - Error handling
     - Transaction handling

  4. Add cleanup
     - Teardown code
     - Resource cleanup
```

**E2E Test Generation:**
```
For each user workflow:
  1. Map user journey
     - Entry point
     - Actions/interactions
     - Expected outcomes

  2. Generate test steps
     - Navigation
     - Form filling
     - Button clicks
     - Assertions

  3. Add wait conditions
     - Element visibility
     - Network requests
     - State changes

  4. Include error cases
     - Validation errors
     - Network failures
     - Timeout handling
```

---

## Pattern Library

### Pattern 1: Arrange-Act-Assert (AAA)

**Structure:**
```javascript
test('description', () => {
  // Arrange: Setup test data and conditions
  const input = 'test data';
  const expected = 'expected result';

  // Act: Execute the function
  const actual = functionUnderTest(input);

  // Assert: Verify the result
  expect(actual).toBe(expected);
});
```

**Why:** Provides clear test structure, easy to read and maintain.

### Pattern 2: Test Fixtures

**JavaScript (Jest):**
```javascript
describe('UserService', () => {
  let userService;
  let mockDatabase;

  beforeEach(() => {
    mockDatabase = createMockDatabase();
    userService = new UserService(mockDatabase);
  });

  afterEach(() => {
    mockDatabase.cleanup();
  });

  test('should create user', () => {
    // Test uses userService and mockDatabase
  });
});
```

**Python (pytest):**
```python
@pytest.fixture
def user_service(db):
    """Create user service with test database"""
    return UserService(db)

def test_create_user(user_service):
    """Test uses user_service fixture"""
    pass
```

**Why:** Reduces duplication, ensures consistent setup/cleanup.

### Pattern 3: Parameterized Tests

**JavaScript (Jest):**
```javascript
describe.each([
  ['valid@email.com', true],
  ['invalid', false],
  ['@example.com', false],
])('validateEmail(%s)', (email, expected) => {
  test(`should return ${expected}`, () => {
    expect(validateEmail(email)).toBe(expected);
  });
});
```

**Python (pytest):**
```python
@pytest.mark.parametrize('email,expected', [
    ('valid@email.com', True),
    ('invalid', False),
    ('@example.com', False),
])
def test_validate_email(email, expected):
    assert validate_email(email) == expected
```

**Why:** Tests multiple inputs without duplication.

### Pattern 4: Mocking External Dependencies

**JavaScript:**
```javascript
jest.mock('../services/api');

test('should fetch user data', async () => {
  const mockUser = { id: 1, name: 'Test' };
  api.fetchUser.mockResolvedValue(mockUser);

  const result = await getUserData(1);

  expect(result).toEqual(mockUser);
  expect(api.fetchUser).toHaveBeenCalledWith(1);
});
```

**Python:**
```python
@patch('app.services.api.fetch_user')
def test_get_user_data(mock_fetch):
    mock_fetch.return_value = {'id': 1, 'name': 'Test'}

    result = get_user_data(1)

    assert result == {'id': 1, 'name': 'Test'}
    mock_fetch.assert_called_once_with(1)
```

**Why:** Isolates code under test, enables testing without external dependencies.

---

## Test Quality Metrics

The skill ensures generated tests meet these criteria:

### 1. Independence
- ✅ Each test runs in isolation
- ✅ No shared state between tests
- ✅ Tests can run in any order
- ✅ No test depends on another

**Implementation:**
```javascript
// Good: Independent tests
beforeEach(() => {
  resetState();
});

test('test 1', () => {
  // Self-contained
});

test('test 2', () => {
  // Self-contained
});
```

### 2. Clarity
- ✅ Descriptive test names
- ✅ Clear arrange-act-assert structure
- ✅ Minimal test logic
- ✅ Obvious assertions

**Implementation:**
```javascript
// Good: Clear test name and structure
test('should return 404 when user not found', async () => {
  // Arrange
  const userId = 999;

  // Act
  const response = await getUser(userId);

  // Assert
  expect(response.status).toBe(404);
});
```

### 3. Coverage
- ✅ Happy paths tested
- ✅ Edge cases covered
- ✅ Error conditions tested
- ✅ Boundary values checked

**Implementation:**
```javascript
// Comprehensive coverage
describe('divide', () => {
  test('should divide positive numbers', () => {});
  test('should handle zero divisor', () => {});
  test('should handle negative numbers', () => {});
  test('should throw for non-numbers', () => {});
});
```

### 4. Maintainability
- ✅ DRY principle (fixtures, helpers)
- ✅ Consistent formatting
- ✅ No magic numbers
- ✅ Clear variable names

**Implementation:**
```javascript
// Good: Maintainable tests
const VALID_EMAIL = 'test@example.com';
const INVALID_EMAIL = 'invalid';

describe('validateEmail', () => {
  test('should accept valid email', () => {
    expect(validateEmail(VALID_EMAIL)).toBe(true);
  });
});
```

---

## Framework-Specific Adaptations

### Jest (JavaScript/TypeScript)

**Test File Structure:**
```javascript
// Import dependencies
import { functionToTest } from '../src/module';

// Group related tests
describe('Module Name', () => {
  // Setup/teardown
  beforeEach(() => {});
  afterEach(() => {});

  // Test cases
  test('should ...', () => {});
  test('should ...', () => {});
});
```

**Assertions:**
- `expect(value).toBe(expected)` - Strict equality
- `expect(value).toEqual(expected)` - Deep equality
- `expect(array).toContain(item)` - Array contains
- `expect(fn).toThrow()` - Throws exception

### pytest (Python)

**Test File Structure:**
```python
# Import dependencies
import pytest
from app.module import function_to_test

# Group with class (optional)
class TestModuleName:
    # Setup/teardown
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    # Test cases
    def test_should_do_something(self):
        pass
```

**Assertions:**
- `assert value == expected` - Equality
- `assert value in collection` - Contains
- `with pytest.raises(Exception):` - Raises exception
- `assert value is True` - Boolean check

### JUnit 5 (Java)

**Test File Structure:**
```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Module Name Tests")
class ModuleNameTest {

    @BeforeEach
    void setUp() {}

    @AfterEach
    void tearDown() {}

    @Test
    @DisplayName("Should do something")
    void testShouldDoSomething() {
        // Test logic
    }
}
```

**Assertions:**
- `assertEquals(expected, actual)` - Equality
- `assertTrue(condition)` - Boolean check
- `assertThrows(Exception.class, () -> {})` - Exception
- `assertNotNull(value)` - Not null check

---

## Design Decisions

### Decision 1: Single Skill vs. Sub-Skills

**Chosen:** Single comprehensive skill

**Rationale:**
- Testing types are interrelated (unit → integration → e2e)
- Users typically need multiple test types for one feature
- Simpler to use one command with `--focus` flag
- Easier to maintain single SKILL.md

**Alternative Considered:**
```
test-fully/
├── SKILL.md (router)
├── unit/SKILL.md
├── integration/SKILL.md
└── e2e/SKILL.md
```

**Why Not:** Overhead of routing, complexity for users.

### Decision 2: Framework Auto-Detection vs. Manual

**Chosen:** Auto-detection with manual override

**Rationale:**
- Better user experience (just works)
- Fewer configuration steps
- Adapts to project setup
- Users can override if needed: `/test-fully --framework pytest`

### Decision 3: Test Generation Approach

**Chosen:** Pattern-based generation with examples

**Rationale:**
- Claude excels at pattern matching
- Examples ensure consistency
- Easy to customize patterns
- Produces idiomatic code

**Alternative Considered:**
- Template-based generation
- AST parsing and generation

**Why Not:** Less flexible, harder to maintain.

---

## Extension Points

### Adding New Framework Support

To add a new testing framework:

1. **Add detection logic:**
```markdown
## Framework Detection

### NewFramework (Language)
- Check for: config-file.ext
- Check for: test pattern
- Import signature: import { test } from 'newframework'
```

2. **Add test patterns:**
```markdown
## Test Patterns

### NewFramework

**Basic Test:**
\```language
test('description', () => {
  // Test code
});
\```
```

3. **Add examples:**
```markdown
## Examples

### NewFramework Example
\```language
// Complete example
\```
```

### Adding New Test Type

To add a new test type (e.g., "security tests"):

1. **Add to testing strategy:**
```markdown
### 5. Security Tests

**Focus:** Security vulnerabilities

**Coverage:**
- SQL injection
- XSS attacks
- Authentication bypass
```

2. **Add patterns:**
```markdown
## Security Test Patterns

**SQL Injection Test:**
\```javascript
test('should prevent SQL injection', () => {
  const maliciousInput = "'; DROP TABLE users--";
  expect(() => query(maliciousInput)).not.toThrow();
});
\```
```

3. **Update usage:**
```bash
/test-fully --focus security
```

---

## Performance Considerations

### Test Generation Speed

**Optimization:**
- Load SKILL.md once (cached by Claude)
- Batch file reads
- Generate tests in single pass

**Typical Performance:**
- Small file (< 100 lines): < 5 seconds
- Medium file (100-500 lines): 5-15 seconds
- Large file (> 500 lines): 15-30 seconds

### Test Execution Speed

**Best Practices Generated:**
- Use in-memory databases for tests
- Mock slow operations
- Parallelize independent tests
- Minimize setup/teardown

**Example:**
```javascript
// Fast: In-memory database
const db = new InMemoryDatabase();

// Slow: Real database
const db = new PostgreSQL('localhost:5432');
```

---

## Maintenance Guidelines

### Updating Patterns

When updating test patterns:

1. **Test with multiple languages:**
   - JavaScript/TypeScript
   - Python
   - Java

2. **Verify framework compatibility:**
   - Jest, Vitest, Mocha
   - pytest, unittest
   - JUnit 5, JUnit 4

3. **Check edge cases:**
   - Async code
   - Promises
   - Callbacks
   - Generators

4. **Update examples:**
   - Keep examples current
   - Use modern syntax
   - Include comments

### Version Management

**Versioning Scheme:** Semantic Versioning (MAJOR.MINOR.PATCH)

- **MAJOR:** Breaking changes (new skill structure, removed patterns)
- **MINOR:** New features (new framework support, new test types)
- **PATCH:** Bug fixes, documentation updates

**Current Version:** 1.0.0

---

## Integration with Other Skills

### With BigQuery Skill

```yaml
# .claude
skills:
  - ./skills/bigquery
  - ./skills/test-fully

# Use together
commands:
  test-bq: "Use /test-fully to test BigQuery queries, then /bigquery to optimize"
```

**Example Workflow:**
1. Write BigQuery query
2. `/test-fully query.sql` - Generate data quality tests
3. `/bigquery/query-optimization` - Optimize query
4. Run tests to verify optimization didn't break logic

### With Other Testing Tools

**Combine with:**
- Linting skills (ESLint, Pylint)
- Code review skills
- Documentation skills

**Example:**
```bash
# Complete quality workflow
/test-fully src/module.js
/lint src/module.js
/document src/module.js
/review src/module.js
```

---

## Future Enhancements

### Potential Additions

1. **Visual Regression Testing:**
   - Playwright screenshots
   - Image diffing
   - Component visual tests

2. **Mutation Testing:**
   - Detect weak tests
   - Suggest improvements
   - Calculate mutation coverage

3. **Contract Testing:**
   - API contract tests
   - Schema validation
   - Pact integration

4. **Chaos Testing:**
   - Random failure injection
   - Network latency simulation
   - Resource exhaustion tests

5. **Property-Based Testing:**
   - QuickCheck patterns
   - Hypothesis (Python)
   - Fast-check (JavaScript)

---

## Key Concepts

### 1. Tests Are Documentation

Generated tests serve as:
- Usage examples
- API documentation
- Behavior specification
- Regression prevention

### 2. Quality Over Quantity

Focus on:
- Meaningful assertions
- Real-world scenarios
- Edge cases that matter
- Not just line coverage

### 3. Tests Should Be Fast

Optimizations:
- Mock slow operations
- Use in-memory databases
- Parallelize when possible
- Skip unnecessary setup

### 4. Tests Should Be Reliable

Avoid:
- Timing dependencies
- Random data without seeds
- External dependencies
- Shared state

---

## Troubleshooting Guide

### Issue: Wrong Framework Detected

**Cause:** Multiple frameworks present or unclear config

**Solution:**
```bash
# Specify framework explicitly
/test-fully --framework jest src/module.js
```

### Issue: Tests Too Generic

**Cause:** Limited code context

**Solution:**
```bash
# Provide more context files
/test-fully src/module.js src/types.ts src/utils.js
```

### Issue: Missing Edge Cases

**Cause:** Unclear requirements

**Solution:**
- Add comments describing edge cases
- Provide example inputs/outputs
- Mention specific scenarios to test

---

## Summary

The test-fully skill is a comprehensive, framework-agnostic testing solution that:

✅ **Detects** testing frameworks automatically
✅ **Generates** production-ready tests
✅ **Follows** language-specific best practices
✅ **Covers** unit, integration, E2E, and performance testing
✅ **Provides** clear documentation and instructions
✅ **Maintains** high quality standards

**Total Knowledge:** ~1500 lines of testing expertise across multiple languages and frameworks.

**Philosophy:** Generate tests that you would write yourself—clear, comprehensive, and maintainable.

---

*Version: 1.0.0*
*Last Updated: 2025-02-10*
