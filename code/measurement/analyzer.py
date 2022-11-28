from sys import path
# adding shared folder to the system path
path.append("../shared")
from serial import Serial
from utility import dec, enc
from numpy import std, sqrt, mean
import scipy.stats as st
from random import choices
from string import ascii_lowercase
from time import sleep, time_ns
import csv

class Analyzer():

    def __init__(self, serial: Serial, payload_size: int, distance: int, measurement_time: int):
        self.serial = serial
        self.payload_size = payload_size
        self.distance = distance
        self.measurement_time = measurement_time
        self.measurement_time_ns = measurement_time * 1_000_000_000
        self.sent_payloads = 0
        self.ack_payloads = 0
        self.delays = []
        self.elapsed_time_ns = 0

    def receive(self):
        input = dec(self.serial.read_until()).strip()
        # Mesasge received and acknowledged (ACK)
        if (input == "m[R,A]"):
            self.ack_payloads += 1
        return input

    def measure(self):
        payload_str = "".join(choices(ascii_lowercase, k=self.payload_size))
        bytes_to_send = enc(f"m[{payload_str}\0,AB]\n")

        while self.sent_payloads < 30 and self.elapsed_time_ns < self.measurement_time_ns:
            sleep(0.01)
            t0 = time_ns()
            self.serial.write(bytes_to_send)
            while self.receive() != "m[D]":
                pass
            t1 = time_ns()
            t = t1 - t0
            self.elapsed_time_ns += t
            self.sent_payloads += 1
            self.delays.append(t)
        # Wait for last ACK
        while self.receive() != "":
            pass

    def save_results(self):
        standard_deviation = std(self.delays) / 1_000_000_000
        mean_packet_delay = mean(self.delays) / 1_000_000_000
        confidence_interval = st.t.interval(alpha=0.95, df=self.sent_payloads-1, loc=mean_packet_delay, scale=standard_deviation / sqrt(self.sent_payloads))
        data_throughput = self.ack_payloads * self.payload_size / self.measurement_time

        print("\n")
        print(f"Payload size: {self.payload_size} byte")
        print(f"Distance: {self.distance} cm")
        print(f"Running time: {self.elapsed_time_ns / 1_000_000_000} s")
        print(f"Standard deviation: {standard_deviation} s")
        print(f"95% confidence interval: {confidence_interval}")
        print(f"Data throughput: {data_throughput} B/s")
        print(f"Mean packet delay: {mean_packet_delay} s")

        success_rate = self.ack_payloads / self.sent_payloads

        print(f"Acknowledged {self.ack_payloads} / {self.sent_payloads} payloads")
        print(f"Success rate: {success_rate * 100}%")

         # open the file in the write mode
        with open(f"results/{self.payload_size}B-{self.distance}cm.csv", "w+") as f:
            (cl, cr) = confidence_interval
            # write to the csv file
            f.write(", ".join([str(i) for i in [standard_deviation, data_throughput, mean_packet_delay, success_rate, cl, cr]]))
            f.write(", ".join([str(i) for i in self.delays]))
