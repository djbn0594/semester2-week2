"""
This is where you should write your code and this is what you need to upload to Gradescope for autograding.

You must NOT change the function definitions (names, arguments).

You can run the functions you define in this file by using test.py (python test.py)
Please do not add any additional code underneath these functions.
"""

import sqlite3


def customer_tickets(conn, customer_id):
    """
    Return a list of tuples:
    (film_title, screen, price)

    Include only tickets purchased by the given customer_id.
    Order results by film title alphabetically.
    """

    query = '''
    SELECT F.title, S.screen, T.Price
    FROM customers C JOIN tickets T ON C.customer_id = T.customer_id
    JOIN screenings S ON T.screening_id = S.screening_id
    JOIN films F ON S.film_id = F.film_id
    WHERE C.customer_id = ?
    ORDER BY F.title
    '''

    cursor = conn.cursor()
    cursor.execute(query, (customer_id,))

    return cursor.fetchall()


def screening_sales(conn):
    """
    Return a list of tuples:
    (screening_id, film_title, tickets_sold)

    Include all screenings, even if tickets_sold is 0.
    Order results by tickets_sold descending.
    """

    query = '''
    SELECT S.screening_id, F.title, Count(T.ticket_id) AS tickets_sold
    FROM screenings S JOIN films F ON S.film_id = F.film_id
    LEFT JOIN tickets T ON T.screening_id = S.screening_id
    GROUP BY S.screening_id, F.title
    ORDER BY tickets_sold DESC
    '''
    
    cursor = conn.cursor()
    cursor.execute(query,)

    return cursor.fetchall()


def top_customers_by_spend(conn, limit):
    """
    Return a list of tuples:
    (customer_name, total_spent)

    total_spent is the sum of ticket prices per customer.
    Only include customers who have bought at least one ticket.
    Order by total_spent descending.
    Limit the number of rows returned to `limit`.
    """

    query = '''
    SELECT C.customer_name, SUM(T.price) AS total_spent
    FROM customers C JOIN tickets T ON C.customer_id = T.customer_id
    GROUP BY C.customer_name
    ORDER BY total_spent DESC LIMIT ?
    '''

    cursor = conn.cursor()
    cursor.execute(query, (limit,))

    return cursor.fetchall()