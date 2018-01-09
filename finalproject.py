from flask import Flask
app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/')
def show_restaurants():
    return 'This will show all my Restaurants'


@app.route('/restaurant/new/')
def new_restaurant():
    return 'This will create a new Restaurant'


@app.route('/restaurant/<int:restaurant_id>/edit/')
def edit_restaurant(restaurant_id):
    return 'This page will be for editing restaurant %s' % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/delete/')
def delete_restaurant(restaurant_id):
    return 'This page will be for deleting restaurant %s' % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def show_menu(restaurant_id):
    return 'This page is the menu for restaurant %s' % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/menu/new')
def new_menu_item(restaurant_id):
    return 'This page is for creating new menu item for restaurant %s' % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def edit_menu_item(restaurant_id, menu_id):
    return 'This page is for editing menu item {} in restaurant {}'.format(menu_id, restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def delete_menu_item(restaurant_id, menu_id):
    return 'This page is for deleting menu item {} in restaurant {}'.format(menu_id, restaurant_id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)