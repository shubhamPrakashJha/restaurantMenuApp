from flask import Flask, render_template, flash, url_for, redirect, request

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind =  engine

DBSession  = sessionmaker(bind=engine)
session = DBSession()



# # Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
# restaurants = [
#     {'name': 'The CRUDdy Crab', 'id': '1'},
#     {'name': 'Blue Burgers', 'id': '2'},
#     {'name': 'Taco Hut', 'id': '3'}]
#
# # print restaurants[1]
#
# # Fake Menu Items
# items = [
#     {'name': 'Cheese Pizza', 'description': 'made with fresh cheese', 'price': '$5.99', 'course': 'Entree', 'id': '1'},
#     {'name': 'Chocolate Cake', 'description': 'made with Dutch Chocolate', 'price': '$3.99', 'course': 'Dessert',
#      'id': '2'},
#     {'name': 'Caesar Salad', 'description': 'with fresh organic vegetables', 'price': '$5.99', 'course': 'Entree',
#      'id': '3'},
#     {'name': 'Iced Tea', 'description': 'with lemon', 'price': '$.99', 'course': 'Beverage', 'id': '4'},
#     {'name': 'Spinach Dip', 'description': 'creamy dip with fresh spinach', 'price': '$1.99', 'course': 'Appetizer',
#      'id': '5'}]
#
# # stores courses in the menu
# courses = []
# for i in items:
#     if i['course'] not in courses:
#         courses.append(i['course'])
# courses.sort()
# # print courses
#
# item = {'name': 'Cheese Pizza', 'description': 'made with fresh cheese', 'price': '$5.99', 'course': 'Entree'}


# show all restaurants
@app.route('/')
@app.route('/restaurants/')
def show_restaurants():
    # return 'This will show all my Restaurants'
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new/')
def new_restaurant():
    # return 'This will create a new Restaurant'
    return render_template('newRestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit/')
def edit_restaurant(restaurant_id):
    # return 'This page will be for editing restaurant %s' % restaurant_id
    return render_template('editRestaurant.html', restaurant_id=restaurant_id, restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete/')
def delete_restaurant(restaurant_id):
    # return 'This page will be for deleting restaurant %s' % restaurant_id
    for hotel in restaurants:
        if int(hotel['id']) == restaurant_id:
            res = hotel
    return render_template('deleteRestaurant.html', restaurant_id=restaurant_id, restaurant=res)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def show_menu(restaurant_id):
    # return 'This page is the menu for restaurant %s' % restaurant_id
    res = {}
    for hotel in restaurants:
        if int(hotel['id']) == restaurant_id:
            res = hotel
    if restaurant_id == 1:
        i = items
        c = courses
    else:
        i = []
        c = []
        flash('sorry for inconvienence, new restaurant')
    return render_template('menu.html', restaurant_id=restaurant_id, restaurant=res, items=i,
                           courses=c)


@app.route('/restaurant/<int:restaurant_id>/menu/new')
def new_menu_item(restaurant_id):
    return render_template('newMenuItem.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def edit_menu_item(restaurant_id, menu_id):
    return render_template('editMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def delete_menu_item(restaurant_id, menu_id):
    return render_template('deleteMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=item)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
