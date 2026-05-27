import allure

from conftest import attach_json

pytestmark = [
    allure.parent_suite("EasyBank API"),
    allure.suite("Students / Employees"),
    allure.sub_suite("Employee CRUD")
]

def employee_payload():
    return {
          "email": "employee.demo@demobank.local",
          "full_name": "Daniil Nikolaev",
          "password": "employee123"
        }

def test_student_can_manage_employee(api_client):
    created_employee_id = None
    create_payload = employee_payload()

    with allure.step("Create employee POST /students/employees"):
        attach_json('create-employee-request', create_payload)
        response = api_client.post(
            f'{api_client.base_url}/students/employees',
            json=create_payload,
            timeout=10
        )
        attach_json('create-employee-response', response.json())
        assert response.status_code == 200
        created_employee = response.json()
        created_employee_id = created_employee['id']
        created_employee_uuid = created_employee['uuid']

        assert created_employee['email'] == create_payload['email']
        assert created_employee['full_name'] == create_payload['full_name']

    with allure.step("Check employee GET /students/employees/{employee_id}"):
        response = api_client.get(
            f'{api_client.base_url}/students/employees/{created_employee_id}',
            timeout=10
        )
        assert response.status_code == 200
        assert response.json()['id'] == created_employee_id

    with allure.step("Update employee PATCH /students/employees/{employee_id}"):
        update_payload = {
          "email": "update.employee.demo@demobank.local",
          "full_name": "UpdateDaniil Nikolaev"
        }
        attach_json(
            "update-employee-request",
            update_payload
        )
        response = api_client.patch(
            f'{api_client.base_url}/students/employees/{created_employee_id}',
            json=update_payload,
            timeout=10
        )
        attach_json(
            "update-employee-response",
            response.json()
        )
        assert response.status_code == 200
        assert response.json()['email'] == update_payload['email']
        assert response.json()['full_name'] == update_payload['full_name']

    with allure.step("Delete employee DELETE students/employees/{created_employee_id}"):
        response = api_client.delete(
            f'{api_client.base_url}/students/employees/{created_employee_id}',
            timeout=10
        )
        attach_json(
            'delete-employee-response',
            response.json()
        )

        assert response.status_code == 200
