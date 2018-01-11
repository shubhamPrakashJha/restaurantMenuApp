from flask import Flask, render_template, flash, url_for, redirect, request

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind =  engine

DBSession  = sessionmaker(bind=engine)
session = DBSession()


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
        flash('New restraunt created!')
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
        flash('Restaurant name updated')
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
        flash('Restaurant deleted!')
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant_id=restaurant_id, restaurant=deletedRestaurant)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def show_menu(restaurant_id):
    # return 'This page is the menu for restaurant %s' % restaurant_id
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    courses = session.query(MenuItem.course).distinct()
    if len(menu) == 0:
        flash(" The Restaurant will Open Soon, Sorry For inconvenience")
    return render_template('menu.html', restaurant_id=restaurant_id, restaurant=restaurant, items=menu,
                           courses=courses)


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET','POST'] )
def new_menu_item(restaurant_id):
    if request.method == 'POST':
        newMenuItem = MenuItem(name=request.form['name'], description=request.form['description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newMenuItem)
        session.commit()
        flash('New Item Created!')
        return redirect(url_for('show_menu', restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET','POST'])
def edit_menu_item(restaurant_id, menu_id):
    editedMenuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedMenuItem.name = request.form['name']
        if request.form['description']:
            editedMenuItem.description = request.form['description']
        if request.form['price']:
            editedMenuItem.price = request.form['price']
        if request.form['course']:
            editedMenuItem.course = request.form['course']
        session.add(editedMenuItem)
        session.commit()
        flash('Menu item Updated')
        return redirect(url_for('show_menu', restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedMenuItem)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET','POST'])
def delete_menu_item(restaurant_id, menu_id):
    deletedMenuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deletedMenuItem)
        session.commit()
        flash('Menu item deleted')
        return redirect(url_for('show_menu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=deletedMenuItem)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
