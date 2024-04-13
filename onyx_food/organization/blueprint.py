from onyx_food.organization.views import *
from onyx_food.utils.helpers import register_view, create_blueprint

organization = create_blueprint('organization', __name__)


register_view(
        organization,
        routes=['/<int:organizationId>'],
        view_func=DashboardView.as_view('dashboard'))
register_view(
        organization,
        routes=['/<int:organizationId>/orders'],
        view_func=Dashboard_OrdersView.as_view('dashboard_orders'))
register_view(
        organization,
        routes=['/<int:organizationId>/menus'],
        view_func=Dashboard_MenusView.as_view('dashboard_menus'))
register_view(
        organization,
        routes=['/<int:organizationId>/statistics_btn'],
        view_func=Dashboard_StatisticsView.as_view('dashboard_statistics'))
register_view(
        organization,
        routes=['/<int:organizationId>/history'],
        view_func=Dashboard_HistoryView.as_view('dashboard_history'))
register_view(
        organization,
        routes=['/<int:organizationId>/work_hours'],
        view_func=Dashboard_WorkHoursView.as_view('dashboard_work_hours'))
register_view(
        organization,
        routes=['/<int:organizationId>/cooking_time'],
        view_func=Dashboard_CookingTimeView.as_view('dashboard_cooking_time'))

register_view(organization, routes=["/","/login"], view_func=LoginView.as_view("login"))
register_view(organization, routes=["/organization_choose"], view_func=LoginView.as_view("organization_choose"))
register_view(organization, routes=["/register"], view_func=RegisterView.as_view("register"))
register_view(organization, routes=["/logout"], view_func=LogoutView.as_view("logout"))