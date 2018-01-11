from flask import Flask, render_template, flash, url_for, redirect, request

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind =  engine

DBSession  = sessionmaker(bind=engine)
session = DBSession()



# Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
restaurants = [
    {'name': 'The CRUDdy Crab', 'id': '1'},
    {'name': 'Blue Burgers', 'id': '2'},
    {'name': 'Taco Hut', 'id': '3'}]

# print restaurants[1]

# Fake Menu Items
items = [
    {'name': 'Cheese Pizza', 'description': 'made with fresh cheese', 'price': '$5.99', 'course': 'Entree', 'id': '1'},
    {'name': 'Chocolate Cake', 'description': 'made with Dutch Chocolate', 'price': '$3.99', 'course': 'Dessert',
     'id': '2'},
    {'name': 'Caesar Salad', 'description': 'with fresh organic vegetables', 'price': '$5.99', 'course': 'Entree',
     'id': '3'},
    {'name': 'Iced Tea', 'description': 'with lemon', 'price': '$.99', 'course': 'Beverage', 'id': '4'},
    {'name': 'Spinach Dip', 'description': 'creamy dip with fresh spinach', 'price': '$1.99', 'course': 'Appetizer',
     'id': '5'}]

# stores courses in the menu
courses = []
for i in items:
    if i['course'] not in courses:
        courses.append(i['course'])
courses.sort()
# print courses

item = {'name': 'Cheese Pizza', 'description': 'made with fresh cheese', 'price': '$5.99', 'course': 'Entree'}


# show all restaurants
@app.route('/')
@app.route('/restaurants/')
def show_restaurants():
    # return 'This will show all my Restaurants'
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new/', methods=['GET','POST'])
def new_restaurant():
    # return 'This will create a new Restaurant'
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('newRestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET','POST'])
def edit_restaurant(restaurant_id):
    # return 'This page will be for editing restaurant %s' % restaurant_id
    editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
        session.add(editedRestaurant)
        session.commit()
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('editRestaurant.html', restaurant_id=restaurant_id, restaurant=editedRestaurant)


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET','POST'])
def delete_restaurant(restaurant_id):
    # return 'This page will be for deleting restaurant %s' % restaurant_id
    deletedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(deletedRestaurant)
        session.commit()
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant_id=restaurant_id, restaurant=deletedRestaurant)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/',methods=['POST','GET'])
def show_menu(restaurant_id):
    # return 'This page is the menu for restaurant %s' % restaurant_id
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    courses = session.query(MenuItem.course).distinct()
    if len(menu) == 0:
        flash(" The Restaurant will Open Soon, Sorry For inconvenience")
    return render_template('menu.html', restaurant_id=restaurant_id, restaurant=restaurant, items=menu,
                           courses=courses)


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
