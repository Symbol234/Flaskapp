from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Create seats: A to U and 1 to 43
named_seats = {chr(c): None for c in range(ord('A'), ord('U') + 1)}  # A to U
numbered_seats = {str(i): None for i in range(1, 44)}                # 1 to 43
seats = {**named_seats, **numbered_seats}  # Combine dictionaries

@app.route('/')
def home():
    return render_template('index.html', seats=seats)

@app.route('/reserve', methods=['POST'])
def reserve():
    seat_id = request.form['seat_id']
    name = request.form['name']
    if seat_id in seats and not seats[seat_id]:
        seats[seat_id] = name
        return jsonify({'success': True, 'message': f"Seat {seat_id} reserved by {name}"})
    return jsonify({'success': False, 'message': f"Seat {seat_id} is already reserved"})

@app.route('/reset', methods=['POST'])
def reset():
    seat_id = request.form['seat_id']
    if seat_id in seats:
        seats[seat_id] = None
        return jsonify({'success': True, 'message': f"Seat {seat_id} has been reset"})
    return jsonify({'success': False, 'message': "Seat ID not found"})

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')

