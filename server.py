import lgpio as GPIO
import time
import socket

# Set the GPIO pins used for the ultrasonic sensor
TRIG = 3  # Pin to send ultrasonic pulse
ECHO = 2  # Pin to receive the reflected pulse

# Initialize GPIO chip (0 is the default on many systems)
h = GPIO.gpiochip_open(0)

# Configure TRIG pin as output, starting low
GPIO.gpio_claim_output(h, TRIG, 0)

# Configure ECHO pin as input
GPIO.gpio_claim_input(h, ECHO)

# Set up a UDP server socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("127.0.0.1", 5000))  # Bind to localhost on port 5000


def get_distance():
    # Ensure the TRIG pin is low before sending a new pulse
    GPIO.gpio_write(h, TRIG, 0)
    time.sleep(0.002)  # Short delay to stabilize the sensor

    # Send a 10 microsecond pulse to trigger the sensor
    GPIO.gpio_write(h, TRIG, 1)
    time.sleep(0.00001)
    GPIO.gpio_write(h, TRIG, 0)

    # Record the start time
    pulse_start = pulse_end = time.time()
    timeout = time.time() + 1  # Set a 1-second timeout for safety

    # Wait for ECHO pin to go high (start of echo pulse)
    while GPIO.gpio_read(h, ECHO) == 0 and time.time() < timeout:
        pulse_start = time.time()

    # Reset timeout for second while loop
    timeout = time.time() + 1

    # Wait for ECHO pin to go low (end of echo pulse)
    while GPIO.gpio_read(h, ECHO) == 1 and time.time() < timeout:
        pulse_end = time.time()

    # Calculate the pulse duration
    pulse_duration = pulse_end - pulse_start

    # Convert time to distance in centimeters (Speed of sound = 34300 cm/s)
    distance = pulse_duration * 17150

    return round(distance, 2)  # Round to two decimal places


if __name__ == "_main_":
    try:
        print("Server is running...")
        while True:
            # Measure distance using ultrasonic sensor
            dist = get_distance()
            print(f"Measured Distance = {dist:.2f} cm")  # You can change to mm if needed

            # Wait for incoming message from a client
            data, clientAddress = server.recvfrom(1024)
            message = data.decode("utf-8")
            print(f"Received from {clientAddress}: {message}")

            # Send the measured distance back to the client
            server.sendto(f"Distance: {dist:.2f} cm".encode(), clientAddress)  # Update unit if needed

            time.sleep(1)  # Optional delay before the next measurement

    except KeyboardInterrupt:
        print("Server shutting down...")  # Graceful shutdown on Ctrl+C

    finally:
        # Clean up GPIO and close server socket
        GPIO.gpiochip_close(h)
        server.close()