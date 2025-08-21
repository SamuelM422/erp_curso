from rest_framework.views import APIView
from companies.utils.exceptions import NotFoundTask, NotFoundGroup, NotFoundEmployee, NotFoundTaskStatus
from companies.models import Employee, Enterprise, Task, TaskStatus
from accounts.models import Group

class Base(APIView):

    @staticmethod
    def get_enterprise_id(user_id):
        employee = Employee.objects.filter(user_id=user_id).first()

        if employee: return employee.enterprise.id

        enterprise = Enterprise.objects.filter(owner_id=user_id).first()

        return enterprise.pk

    def get_employee(self, employee_id, user_id):
        enterprise_id = self.get_enterprise_id(user_id)

        employee = Employee.objects.filter(id=employee_id, enterprise_id=enterprise_id).first()

        if not employee:
            raise NotFoundEmployee

        return employee

    @staticmethod
    def get_group(group_id, enterprise_id):
        group = Group.objects.values('name').filter(id=group_id, enterprise_id=enterprise_id).first()

        if not group:
            raise NotFoundGroup

        return group

    @staticmethod
    def get_status(status_id):
        status = TaskStatus.objects.filter(id=status_id).first()

        if not status:
            raise NotFoundTaskStatus

        return status

    @staticmethod
    def get_task(task_id, enterprise_id):
        task = Task.objects.filter(id=task_id, enterprise_id=enterprise_id).first()

        if not task:
            raise NotFoundTask

        return task