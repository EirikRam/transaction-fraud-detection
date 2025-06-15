from src.simulator.simulator import FraudDataSimulator

if __name__ == "__main__":
    simulator = FraudDataSimulator()
    simulator.save_to_csv()
