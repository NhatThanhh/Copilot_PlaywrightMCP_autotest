Objective:
Create a fully functional Playwright Python test automation framework using Playwright MCP Server, following best practices such as Page Object Model, pytest fixtures, and JSON test data. Follow the current project structure and update only the necessary files. Do not recreate the project from scratch.

Step 1: Setup MCP Server
Launch Playwright MCP Server.
Navigate to the base url in conftest.py file through Playwright MCP Server.
Ensure all browser automation runs only via MCP Server — no static simulation or bypassing.
Use data-test html property primarily to locate elements.
Use codegen tool provided with Playwright MCP Server to generate all the code first.
Step 2: Test Scenarios to Validate

Scenario 1: DK_01 - Register with valid information
Test data:
* Email: "thanhblink01@gmail.com"
* Password: "Th@nh2004"
* Phone number: "0376704109"
* Full name: "Nguyễn Nhật Thanh"
* Date of birth: "20/08/2004"
* Gender: "Nam"
Test steps:
1. On the base url page, click the "Đăng ký" button/link.
2. Enter valid data into all required fields.
3. Tick the checkbox "Tôi trên 16 tuổi và đồng ý với Điều khoản và Điều kiện".
4. Click the "Tạo Tài Khoản Mới" button.

Verify:
* Registration is successful.
* A confirmation dialog is displayed with the message:
  "thanhblink@gmail.com
  Chúng tôi đã gửi email xác nhận kèm theo liên kết.
  Vui lòng kiểm tra email của bạn để kích hoạt tài khoản."

Scenario 2: DK_02 - Register with an existing email
Test data:
* Email: "thanhblink@gmail.com"
* Password: "Th@nh2004"
* Phone number: "0376704109"
* Full name: "Nguyễn Nhật Thanh"
* Date of birth: "20/08/2004"
* Gender: "Nam"
Test steps:
1. On the base url page, click the "Đăng ký" button/link.
2. Enter valid data into all required fields.
3. Tick the checkbox "Tôi trên 16 tuổi và đồng ý với Điều khoản và Điều kiện".
4. Click the "Tạo Tài Khoản Mới" button.
Verify:
* Registration fails.
* The message "Địa chỉ email đã tồn tại. Vui lòng đăng nhập để tiếp tục." is displayed.

Note:
All scenarios must be validated independently.
Only after Step 1 and Step 2 are completed, and the code is generated using Playwright MCP Server codegen, proceed to Step 3 to build the framework using the generated code.

All scenarios should be validated independently.
Once Step 1 and Step 2 are completed, and code is generate using codegen, then only proceed furhter with Step 3 to create framework using generated code.

Step 3: Framework Development Guidelines
Use Playwright MCP Server code generation to generate initial code.
Convert generated code into a Pytest Playwright Test runner framework.
Implement Page Object Model (POM) for all pages follow the current project structure.
Use Fixtures with POM also use fixtures instead of beforeEach and afterEach hooks where appropriate.
Store test data in a JSON file and read dynamically.
Keep tests independent — no inter-test dependencies.
Assertions must be in test scripts, not in POM methods.
Add Allure epic, story, tittle and severity for test case reigister
