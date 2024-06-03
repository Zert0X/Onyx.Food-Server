from onyx_food.organization.views import *
from onyx_food.utils.helpers import register_view, create_blueprint

organization = create_blueprint('organization', __name__)


register_view(
        organization,
        routes=['/<int:organizationID>'],
        view_func=DashboardView.as_view('dashboard'))


register_view(
        organization,
        routes=['/<int:organizationID>/orders'],
        view_func=Dashboard_OrdersView.as_view('dashboard_orders'))

register_view(
        organization,
        routes=['/<int:organizationID>/orders/<int:orderID>/info'],
        view_func=Dashboard_OrderInfo.as_view('dashboard_order_info'))

register_view(
        organization,
        routes=['/<int:organizationID>/menu'],
        view_func=Dashboard_MenusView.as_view('dashboard_menus'))
register_view(
        organization,
        routes=['/<int:organizationID>/menu/<int:categoryID>/info'],
        view_func=Dashboard_MenuInfo.as_view('dashboard_menu_info'))
register_view(
        organization,
        routes=['/<int:organizationID>/menu/add_category'],
        view_func=Dashboard_MenuAddCategory.as_view('dashboard_menu_add_category'))

register_view(
        organization,
        routes=['/<int:organizationID>/statistics_btn'],
        view_func=Dashboard_StatisticsView.as_view('dashboard_statistics'))
register_view(
        organization,
        routes=['/<int:organizationID>/history'],
        view_func=Dashboard_HistoryView.as_view('dashboard_history'))
register_view(
        organization,
        routes=['/<int:organizationID>/work_hours'],
        view_func=Dashboard_WorkHoursView.as_view('dashboard_work_hours'))
register_view(
        organization,
        routes=['/<int:organizationID>/cooking_time'],
        view_func=Dashboard_CookingTimeView.as_view('dashboard_cooking_time'))

register_view(
        organization,
        routes=['/<int:organizationID>/restaurant_add'],
        view_func=RestaurantAdd.as_view('restaurant_add'))

register_view(
        organization,
        routes=['/<int:organizationID>/restaurant/<int:restaurantID>'],
        view_func=RestaurantDashboard.as_view('restaurant_dashboard'))

register_view(
        organization,
        routes=['/<int:organizationID>/restaurant/<int:restaurantID>/reviews'],
        view_func=RestaurantReviews.as_view('restaurant_reviews'))

register_view(
        organization,
        routes=['/<int:organizationID>/restaurant/<int:restaurantID>/info'],
        view_func=RestaurantInfo.as_view('restaurant_info'))
register_view(
        organization,
        routes=['/<int:organizationID>/restaurant/<int:restaurantID>/disable'],
        view_func=RestaurantDisable.as_view('restaurant_disable'))

register_view(organization, routes=["/","/login"], view_func=LoginView.as_view("login"))
register_view(organization, routes=["/organization_choose"], view_func=OrganizationChooseView.as_view("organization_choose"))
register_view(organization, routes=["/register"], view_func=RegisterView.as_view("register"))
register_view(organization, routes=["/logout"], view_func=LogoutView.as_view("logout"))